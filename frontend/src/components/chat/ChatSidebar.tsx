import { Plus, MessageSquare, Trash2 } from "lucide-react";
import { Conversation } from "@/types/chat";
import { cn } from "@/lib/utils";

/**
 * Propriétés du composant ChatSidebar.
 * @typedef {Object} ChatSidebarProps
 * @property {Conversation[]} conversations - Liste de toutes les discussions.
 * @property {string} activeId - Identifiant de la discussion active.
 * @property {function(string): void} onSelect - Callback lors du changement de discussion.
 * @property {function(): void} onNew - Callback pour créer une nouvelle discussion.
 * @property {function(string): void} onDelete - Callback pour supprimer une discussion.
 * @property {boolean} isOpen - État d'ouverture du menu (mobile).
 * @property {function(): void} onClose - Callback pour fermer le menu (mobile).
 */
interface ChatSidebarProps {
  conversations: Conversation[];
  activeId: string;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Barre latérale gérant l'historique des conversations.
 * Permet de naviguer entre les discussions, d'en créer de nouvelles ou d'en supprimer.
 * @param {ChatSidebarProps} props - Les propriétés du composant.
 * @returns {JSX.Element} La barre latérale rendue.
 */
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
