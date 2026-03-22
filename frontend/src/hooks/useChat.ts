import { Conversation, Message, ToolCall } from "@/types/chat";
import { useCallback, useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";
const STORAGE_KEY = "jarvis_conversations";

const generateId = () => Math.random().toString(36).substring(2, 15);

const createConversation = (title = "Nouvelle discussion"): Conversation => ({
  id: generateId(),
  title,
  messages: [],
  createdAt: new Date(),
  updatedAt: new Date(),
});

type ApiHistoryMessage = {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
};

type StoredConversation = {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
};

const toStored = (conversation: Conversation): StoredConversation => ({
  id: conversation.id,
  title: conversation.title,
  createdAt: conversation.createdAt.toISOString(),
  updatedAt: conversation.updatedAt.toISOString(),
});

const fromStored = (stored: StoredConversation): Conversation => ({
  id: stored.id,
  title: stored.title,
  messages: [],
  createdAt: new Date(stored.createdAt),
  updatedAt: new Date(stored.updatedAt),
});

const readStoredConversations = (): Conversation[] => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as StoredConversation[];
    if (!Array.isArray(parsed)) return [];
    return parsed.map(fromStored);
  } catch {
    return [];
  }
};

const saveStoredConversations = (conversations: Conversation[]) => {
  const value = JSON.stringify(conversations.map(toStored));
  localStorage.setItem(STORAGE_KEY, value);
};

const toUiMessage = (message: ApiHistoryMessage): Message => ({
  id: generateId(),
  role: message.role,
  content: message.content,
  timestamp: new Date(message.timestamp),
});

const buildInitialState = (): {
  conversations: Conversation[];
  activeConversationId: string;
} => {
  const stored = readStoredConversations();
  if (stored.length > 0) {
    return {
      conversations: stored,
      activeConversationId: stored[0].id,
    };
  }

  const first = createConversation("Première discussion");
  return {
    conversations: [first],
    activeConversationId: first.id,
  };
};

export function useChat() {
  const [initial] = useState(buildInitialState);
  const [conversations, setConversations] = useState<Conversation[]>(
    initial.conversations
  );
  const [activeConversationId, setActiveConversationId] = useState<string>(
    initial.activeConversationId
  );
  const [isLoading, setIsLoading] = useState(false);

  const activeConversation = conversations.find(
    (c) => c.id === activeConversationId
  );

  useEffect(() => {
    saveStoredConversations(conversations);
  }, [conversations]);

  useEffect(() => {
    if (!activeConversation) return;

    let cancelled = false;

    const loadHistory = async () => {
      try {
        const response = await fetch(
          `${API_BASE}/chat/${activeConversation.id}/messages`
        );
        if (!response.ok) return;
        const data = (await response.json()) as ApiHistoryMessage[];
        if (cancelled) return;

        setConversations((prev) =>
          prev.map((conversation) =>
            conversation.id === activeConversation.id
              ? {
                  ...conversation,
                  messages: data.map(toUiMessage),
                  updatedAt:
                    data.length > 0
                      ? new Date(data[data.length - 1].timestamp)
                      : conversation.updatedAt,
                }
              : conversation
          )
        );
      } catch {
        // Keep local state if backend is unavailable.
      }
    };

    loadHistory();

    return () => {
      cancelled = true;
    };
  }, [activeConversation?.id]);

  const addMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      const userMessage: Message = {
        id: generateId(),
        role: "user",
        content: content.trim(),
        timestamp: new Date(),
      };

      const assistantMessageId = generateId();

      // Add user message and empty assistant message immediately.
      setConversations((prev) =>
        prev.map((c) => {
          if (c.id !== activeConversationId) return c;
          const isFirst = c.messages.length === 0;
          return {
            ...c,
            title: isFirst ? content.trim().slice(0, 40) : c.title,
            messages: [
              ...c.messages,
              userMessage,
              {
                id: assistantMessageId,
                role: "assistant" as const,
                content: "",
                timestamp: new Date(),
                toolCalls: [],
              },
            ],
            updatedAt: new Date(),
          };
        })
      );

      setIsLoading(true);

      try {
        const response = await fetch(`${API_BASE}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: activeConversationId,
            message: content.trim(),
          }),
        });

        if (!response.ok) {
          throw new Error(`Erreur serveur : ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) throw new Error("Aucun corps de réponse");

        let accumulated = "";
        let assistantText = "";
        let toolCalls: ToolCall[] = [];

        const updateAssistantMessage = () => {
          setConversations((prev) =>
            prev.map((c) =>
              c.id === activeConversationId
                ? {
                    ...c,
                    messages: c.messages.map((m) =>
                      m.id === assistantMessageId
                        ? { ...m, content: assistantText, toolCalls }
                        : m
                    ),
                  }
                : c
            )
          );
        };

        const upsertToolCall = (next: ToolCall) => {
          const index = toolCalls.findIndex((t) => t.id === next.id);
          if (index === -1) {
            toolCalls = [...toolCalls, next];
          } else {
            toolCalls = toolCalls.map((t, i) => (i === index ? next : t));
          }
        };

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          accumulated += decoder.decode(value, { stream: true });

          let newlineIndex = accumulated.indexOf("\n");
          while (newlineIndex !== -1) {
            const line = accumulated.slice(0, newlineIndex).trim();
            accumulated = accumulated.slice(newlineIndex + 1);
            newlineIndex = accumulated.indexOf("\n");

            if (!line) continue;

            try {
              const evt = JSON.parse(line);
              if (evt.type === "token") {
                assistantText += evt.content ?? "";
                updateAssistantMessage();
                continue;
              }

              const toolId = evt.run_id ?? generateId();
              if (evt.type === "tool_start") {
                upsertToolCall({
                  id: toolId,
                  name: evt.name ?? "tool",
                  status: "running",
                  input: evt.input ?? "",
                });
                updateAssistantMessage();
                continue;
              }

              if (evt.type === "tool_end") {
                const existing = toolCalls.find((t) => t.id === toolId);
                upsertToolCall({
                  id: toolId,
                  name: evt.name ?? existing?.name ?? "tool",
                  status: "success",
                  input: existing?.input ?? "",
                  output: evt.output ?? "",
                });
                updateAssistantMessage();
                continue;
              }

              if (evt.type === "tool_error") {
                const existing = toolCalls.find((t) => t.id === toolId);
                upsertToolCall({
                  id: toolId,
                  name: evt.name ?? existing?.name ?? "tool",
                  status: "error",
                  input: existing?.input ?? "",
                  error: evt.error ?? "",
                });
                updateAssistantMessage();
                continue;
              }
            } catch {
              assistantText += line;
              updateAssistantMessage();
            }
          }
        }
      } catch (error) {
        const errMsg =
          error instanceof Error ? error.message : "Une erreur est survenue";
        setConversations((prev) =>
          prev.map((c) =>
            c.id === activeConversationId
              ? {
                  ...c,
                  messages: c.messages.map((m) =>
                    m.id === assistantMessageId
                      ? {
                          ...m,
                          content: `Erreur : ${errMsg}\n\nAssurez-vous que votre backend est en cours d'exécution sur \`${API_BASE}\`.`,
                        }
                      : m
                  ),
                }
              : c
          )
        );
      } finally {
        setIsLoading(false);
      }
    },
    [activeConversationId, isLoading]
  );

  const newConversation = useCallback(() => {
    const conv = createConversation();
    setConversations((prev) => [conv, ...prev]);
    setActiveConversationId(conv.id);
  }, []);

  const deleteConversation = useCallback(
    (id: string) => {
      setConversations((prev) => {
        const filtered = prev.filter((c) => c.id !== id);
        if (filtered.length === 0) {
          const conv = createConversation();
          setActiveConversationId(conv.id);
          return [conv];
        }
        if (id === activeConversationId) {
          setActiveConversationId(filtered[0].id);
        }
        return filtered;
      });
    },
    [activeConversationId]
  );

  return {
    conversations,
    activeConversation,
    activeConversationId,
    setActiveConversationId,
    addMessage,
    newConversation,
    deleteConversation,
    isLoading,
  };
}
