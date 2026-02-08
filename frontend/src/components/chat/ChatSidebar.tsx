import { Plus, MessageSquare, Trash2 } from "lucide-react";
import { Conversation } from "@/types/chat";
import { cn } from "@/lib/utils";

interface ChatSidebarProps {
  conversations: Conversation[];
  activeId: string;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

export function ChatSidebar({
  conversations,
  activeId,
  onSelect,
  onNew,
  onDelete,
  isOpen,
  onClose,
}: ChatSidebarProps) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={onClose}
        />
      )}
      <aside
        className={cn(
          "fixed md:relative z-50 md:z-auto flex flex-col w-72 h-full bg-sidebar border-r border-sidebar-border transition-transform duration-300",
          isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        )}
      >
        <div className="p-3">
          <button
            onClick={onNew}
            className="flex items-center gap-2 w-full px-3 py-2.5 rounded-lg border border-border text-sm text-foreground hover:bg-sidebar-accent transition-colors"
          >
            <Plus size={16} />
            Nouvelle discussion
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto scrollbar-thin px-2 pb-4">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              className={cn(
                "group flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-colors mb-0.5",
                conv.id === activeId
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-sidebar-foreground hover:bg-sidebar-accent/50"
              )}
              onClick={() => {
                onSelect(conv.id);
                onClose();
              }}
            >
              <MessageSquare size={14} className="shrink-0 opacity-50" />
              <span className="truncate flex-1">{conv.title}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(conv.id);
                }}
                className="opacity-0 group-hover:opacity-100 p-1 hover:text-destructive transition-all"
              >
                <Trash2 size={13} />
              </button>
            </div>
          ))}
        </nav>
      </aside>
    </>
  );
}
