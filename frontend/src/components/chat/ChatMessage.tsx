import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";
import { ChartSpec, Message } from "@/types/chat";
import { motion } from "framer-motion";
import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";

interface ChatMessageProps {
  message: Message;
}

function ToolChart({ chart }: { chart: ChartSpec }) {
  const metric = chart.y_keys[0];
  const chartConfig: ChartConfig = {
    [metric]: {
      label: metric,
      color: "hsl(var(--primary))",
    },
  };

  if (!chart.points?.length || !metric) {
    return (
      <div className="mt-2 rounded-lg border border-border bg-secondary/30 p-3 text-xs text-muted-foreground">
        Impossible d'afficher le graphique: spec invalide ou vide.
      </div>
    );
  }

  return (
    <div className="mt-3 rounded-xl border border-border/60 bg-secondary/20 p-3">
      <p className="mb-2 text-xs font-medium text-foreground">{chart.title}</p>
      <ChartContainer config={chartConfig} className="h-56 w-full">
        <LineChart data={chart.points} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
          <CartesianGrid vertical={false} />
          <XAxis
            dataKey={chart.x_key}
            tickLine={false}
            axisLine={false}
            minTickGap={40}
            tickFormatter={(value: string) => {
              if (typeof value !== "string") return "";
              return value.slice(5, 16).replace("T", " ");
            }}
          />
          <YAxis tickLine={false} axisLine={false} width={42} />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Line
            type="monotone"
            dataKey={metric}
            stroke={`var(--color-${metric})`}
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ChartContainer>
      {chart.metadata?.aggregation && (
        <p className="mt-2 text-[11px] text-muted-foreground">
          agrégation: {chart.metadata.aggregation}
        </p>
      )}
    </div>
  );
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const toolCalls = message.toolCalls ?? [];
  const chartPayload = toolCalls.find((tool) => tool.payload?.type === "chart")?.payload;

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
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
        {!isUser && chartPayload?.type === "chart" && <ToolChart chart={chartPayload.chart} />}
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
                      className={`inline-flex items-center gap-2 rounded-full px-2.5 py-1 transition-colors duration-300 ${badgeClass} ${tool.status === "running" ? "animate-pulse" : ""}`}
                    >
                      {tool.status === "running" && (
                        <span className="inline-block h-2 w-2 rounded-full bg-current animate-pulse" />
                      )}
                      {tool.name} · {tool.status === "running" ? "en cours..." : tool.status}
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
