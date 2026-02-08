import { Bot } from "lucide-react";
import { motion } from "framer-motion";

export function EmptyState() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="flex flex-col items-center justify-center h-full gap-4 px-4"
    >
      <div className="w-14 h-14 rounded-2xl bg-primary/15 flex items-center justify-center">
        <Bot size={28} className="text-primary" />
      </div>
      <h2 className="text-xl font-semibold text-foreground">
        Comment puis-je vous aider ?
      </h2>
      <p className="text-sm text-muted-foreground text-center max-w-sm">
        Commencez une conversation avec J4RVIS en écrivant un message
        ci-dessous.
      </p>
    </motion.div>
  );
}
