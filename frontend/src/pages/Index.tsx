import { useState, useRef, useEffect } from "react";
import { Menu } from "lucide-react";
import { useChat } from "@/hooks/useChat";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatMessage } from "@/components/chat/ChatMessage";
import { ChatInput } from "@/components/chat/ChatInput";
import { TypingIndicator } from "@/components/chat/TypingIndicator";
import { EmptyState } from "@/components/chat/EmptyState";

const Index = () => {
  const {
    conversations,
    activeConversation,
    activeConversationId,
    setActiveConversationId,
    addMessage,
    newConversation,
    deleteConversation,
    isLoading,
  } = useChat();

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeConversation?.messages, isLoading]);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <ChatSidebar
        conversations={conversations}
        activeId={activeConversationId}
        onSelect={setActiveConversationId}
        onNew={newConversation}
        onDelete={deleteConversation}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <main className="flex flex-col flex-1 min-w-0">
        {/* Header */}
        <header className="flex items-center gap-3 px-4 py-3 border-b border-border bg-background/80 backdrop-blur-sm">
          <button
            onClick={() => setSidebarOpen(true)}
            className="md:hidden p-1.5 rounded-lg hover:bg-secondary transition-colors"
          >
            <Menu size={20} />
          </button>
          <h1 className="text-sm font-medium text-foreground truncate">
            {activeConversation?.title || "Nouvelle discussion"}
          </h1>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto scrollbar-thin">
          {activeConversation?.messages.length === 0 ? (
            <EmptyState />
          ) : (
            <div className="divide-y divide-border/30">
              {activeConversation?.messages.map((msg) => (
                <ChatMessage key={msg.id} message={msg} />
              ))}
              {isLoading && <TypingIndicator />}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <ChatInput onSend={addMessage} disabled={isLoading} />
      </main>
    </div>
  );
};

export default Index;
