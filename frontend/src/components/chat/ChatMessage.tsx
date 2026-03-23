import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";
import { TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Message } from "@/types/chat";
import { motion } from "framer-motion";
import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const toolCalls = message.toolCalls ?? [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex gap-4 px-4 py-6 max-w-3xl mx-auto"
    >
      <div
        className={`shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
          isUser ? "bg-user-bubble" : "bg-primary/20"
        }`}
      >
        {isUser ? (
          <User size={16} className="text-foreground" />
        ) : (
          <Bot size={16} className="text-primary" />
        )}
      </div>
      <div className="flex-1 min-w-0 pt-0.5">
        <p className="text-xs font-medium text-muted-foreground mb-1.5">
          {isUser ? "Vous" : "Assistant"}
        </p>
        <div className="prose prose-invert prose-sm max-w-none text-foreground leading-relaxed [&_p]:mb-3 [&_code]:bg-secondary [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-primary [&_pre]:bg-secondary [&_pre]:rounded-lg [&_pre]:p-4">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              table: ({ node, ...props }) => (
                <div className="my-4 w-full overflow-y-auto rounded-lg border bg-card text-card-foreground">
                  <table className="w-full caption-bottom text-sm" {...props} />
                </div>
              ),
              thead: ({ node, ...props }) => <TableHeader {...props} />,
              tbody: ({ node, ...props }) => <TableBody {...props} />,
              tr: ({ node, ...props }) => <TableRow {...props} />,
              th: ({ node, ...props }) => <TableHead {...props} />,
              td: ({ node, ...props }) => <TableCell {...props} />,
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        {!isUser && toolCalls.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            {toolCalls.map((tool) => {
              const badgeClass =
                tool.status === "error"
                  ? "bg-red-500/20 text-red-200"
                  : tool.status === "success"
                  ? "bg-emerald-500/20 text-emerald-200"
                  : "bg-secondary text-foreground";

              return (
                <HoverCard key={tool.id}>
                  <HoverCardTrigger asChild>
                    <span
                      className={`inline-flex items-center gap-2 rounded-full px-2.5 py-1 ${badgeClass}`}
                    >
                      {tool.name} · {tool.status}
                    </span>
                  </HoverCardTrigger>
                  <HoverCardContent align="start" className="w-80">
                    <div className="space-y-2">
                      <div>
                        <p className="text-xs uppercase tracking-wide text-muted-foreground">Tool</p>
                        <p className="text-sm font-semibold text-foreground">{tool.name}</p>
                      </div>
                      <div className="flex items-center gap-2 text-xs">
                        <span className="uppercase tracking-wide text-muted-foreground">Status</span>
                        <span className="text-foreground">{tool.status}</span>
                      </div>
                      {tool.input && (
                        <div>
                          <p className="text-xs uppercase tracking-wide text-muted-foreground">Input</p>
                          <pre className="mt-1 max-h-40 overflow-auto rounded-md bg-secondary/60 p-2 text-xs text-foreground">
                            {tool.input}
                          </pre>
                        </div>
                      )}
                      {tool.output && (
                        <div>
                          <p className="text-xs uppercase tracking-wide text-muted-foreground">Output</p>
                          <pre className="mt-1 max-h-40 overflow-auto rounded-md bg-secondary/60 p-2 text-xs text-foreground">
                            {tool.output}
                          </pre>
                        </div>
                      )}
                      {tool.error && (
                        <div>
                          <p className="text-xs uppercase tracking-wide text-red-300">Error</p>
                          <pre className="mt-1 max-h-40 overflow-auto rounded-md bg-red-500/10 p-2 text-xs text-red-100">
                            {tool.error}
                          </pre>
                        </div>
                      )}
                    </div>
                  </HoverCardContent>
                </HoverCard>
              );
            })}
          </div>
        )}
      </div>
    </motion.div>
  );
}
