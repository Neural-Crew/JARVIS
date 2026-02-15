import { Bot } from "lucide-react";

export function TypingIndicator() {
  return (
    <div className="flex gap-4 px-4 py-6 max-w-3xl mx-auto">
      <div className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center bg-primary/20">
        <Bot size={16} className="text-primary" />
      </div>
      <div className="flex items-center gap-1.5 pt-2">
        <span className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse-dot" />
        <span className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse-dot [animation-delay:0.2s]" />
        <span className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse-dot [animation-delay:0.4s]" />
      </div>
    </div>
  );
}
