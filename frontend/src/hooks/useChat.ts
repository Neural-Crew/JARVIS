import { Conversation, Message, ToolCall, ToolPayload } from "@/types/chat";
import { useCallback, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

const generateId = () => Math.random().toString(36).substring(2, 15);

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null;

const isChartToolPayload = (value: unknown): value is ToolPayload => {
  if (!isRecord(value)) return false;
  return value.type === "chart" && value.chart !== undefined;
};

const hasChartPayloadEnvelope = (
  value: unknown
): value is { payload: ToolPayload } => {
  if (!isRecord(value) || !("payload" in value)) return false;
  return isChartToolPayload(value.payload);
};

const parseToolPayload = (rawOutput: string): ToolPayload | undefined => {
  if (!rawOutput) return undefined;

  const extractPayload = (candidate: unknown): ToolPayload | undefined => {
    if (!hasChartPayloadEnvelope(candidate)) return undefined;
    return candidate.payload;
  };

  try {
    const parsed = JSON.parse(rawOutput);
    const payload = extractPayload(parsed);
    if (payload) return payload;
  } catch {
    // ignore and try fallback extraction below
  }

  const firstBrace = rawOutput.indexOf("{");
  const lastBrace = rawOutput.lastIndexOf("}");
  if (firstBrace >= 0 && lastBrace > firstBrace) {
    const candidate = rawOutput.slice(firstBrace, lastBrace + 1);
    try {
      const parsed = JSON.parse(candidate);
      const payload = extractPayload(parsed);
      if (payload) return payload;
    } catch {
      return undefined;
    }
  }

  return undefined;
};

const createConversation = (title = "Nouvelle discussion"): Conversation => ({
  id: generateId(),
  title,
  messages: [],
  createdAt: new Date(),
  updatedAt: new Date(),
});

export function useChat() {
  const [conversations, setConversations] = useState<Conversation[]>([
    createConversation("Première discussion"),
  ]);
  const [activeConversationId, setActiveConversationId] = useState<string>(
    conversations[0].id
  );
  const [isLoading, setIsLoading] = useState(false);

  const activeConversation = conversations.find(
    (c) => c.id === activeConversationId
  );

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

      // Build message history for the API
      const currentConv = conversations.find(
        (c) => c.id === activeConversationId
      );
      const apiMessages = [
        ...(currentConv?.messages.map((m) => ({
          role: m.role,
          content: m.content,
        })) || []),
        { role: "user" as const, content: content.trim() },
      ];

      // Add user message and empty assistant message
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
          body: JSON.stringify({ messages: apiMessages }),
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
        const toolStartTimes: Record<string, number> = {};
        const MIN_RUNNING_MS = 500;

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
                toolStartTimes[toolId] = Date.now();
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
                const output = evt.output ?? "";
                const elapsed = Date.now() - (toolStartTimes[toolId] ?? 0);
                const delay = Math.max(0, MIN_RUNNING_MS - elapsed);

                const applyEnd = () => {
                  upsertToolCall({
                    id: toolId,
                    name: evt.name ?? existing?.name ?? "tool",
                    status: "success",
                    input: existing?.input ?? "",
                    output,
                    payload: parseToolPayload(output),
                  });
                  updateAssistantMessage();
                };

                if (delay > 0) {
                  setTimeout(applyEnd, delay);
                } else {
                  applyEnd();
                }
                continue;
              }

              if (evt.type === "tool_error") {
                const existing = toolCalls.find((t) => t.id === toolId);
                const elapsed = Date.now() - (toolStartTimes[toolId] ?? 0);
                const delay = Math.max(0, MIN_RUNNING_MS - elapsed);

                const applyError = () => {
                  upsertToolCall({
                    id: toolId,
                    name: evt.name ?? existing?.name ?? "tool",
                    status: "error",
                    input: existing?.input ?? "",
                    error: evt.error ?? "",
                  });
                  updateAssistantMessage();
                };

                if (delay > 0) {
                  setTimeout(applyError, delay);
                } else {
                  applyError();
                }
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
    [activeConversationId, isLoading, conversations]
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
