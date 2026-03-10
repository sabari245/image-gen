import { useEffect } from "react";
import { Clock, Trash2, PanelLeftClose, PanelLeft } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useGenerationStore } from "@/store/generation";
import { getHistory, deleteGeneration, getImageUrl } from "@/api/client";

interface HistorySidebarProps {
  onSelect: (id: number) => void;
  currentId: number | null;
}

export function HistorySidebar({ onSelect, currentId }: HistorySidebarProps) {
  const {
    history,
    setHistory,
    removeFromHistory,
    isSidebarOpen,
    setSidebarOpen,
  } = useGenerationStore();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getHistory();
        setHistory(data.items, data.total, data.page);
      } catch (error) {
        console.error("Failed to fetch history:", error);
      }
    };
    fetchHistory();
  }, []);

  const handleDelete = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    try {
      await deleteGeneration(id);
      removeFromHistory(id);
    } catch (error) {
      console.error("Failed to delete generation:", error);
    }
  };

  if (!isSidebarOpen) {
    return (
      <Button
        variant="ghost"
        size="icon"
        className="fixed left-4 top-4 z-10"
        onClick={() => setSidebarOpen(true)}
      >
        <PanelLeft className="h-5 w-5" />
      </Button>
    );
  }

  return (
    <div className="w-72 border-r bg-muted/30 flex flex-col h-full">
      <div className="p-4 border-b flex items-center justify-between">
        <h2 className="font-semibold flex items-center gap-2">
          <Clock className="h-4 w-4" />
          History
        </h2>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setSidebarOpen(false)}
        >
          <PanelLeftClose className="h-4 w-4" />
        </Button>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-2 space-y-2">
          {history.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-4">
              No generations yet
            </p>
          ) : (
            history.map((gen) => {
              const thumbnail = gen.images.find(
                (img) => img.image_type === "output"
              );

              return (
                <button
                  key={gen.id}
                  onClick={() => onSelect(gen.id)}
                  className={`w-full text-left p-2 rounded-lg hover:bg-muted transition-colors group ${
                    currentId === gen.id ? "bg-muted ring-1 ring-primary" : ""
                  }`}
                >
                  <div className="flex gap-3">
                    <div className="w-12 h-12 rounded bg-muted-foreground/10 flex-shrink-0 overflow-hidden">
                      {thumbnail ? (
                        <img
                          src={getImageUrl(thumbnail.file_path)}
                          alt=""
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-muted-foreground text-xs">
                          {gen.status === "processing" ? "..." : "—"}
                        </div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm truncate">{gen.prompt}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge
                          variant={
                            gen.status === "completed"
                              ? "default"
                              : gen.status === "failed"
                              ? "destructive"
                              : "secondary"
                          }
                          className="text-xs h-5"
                        >
                          {gen.status}
                        </Badge>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 opacity-0 group-hover:opacity-100 flex-shrink-0"
                      onClick={(e) => handleDelete(e, gen.id)}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </button>
              );
            })
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
