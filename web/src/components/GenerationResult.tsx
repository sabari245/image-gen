import { useEffect, useState } from "react";
import { AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { useGenerationStore } from "@/store/generation";
import { getGeneration, getImageUrl } from "@/api/client";
import { ImageLightbox } from "./ImageLightbox";

interface GenerationResultProps {
  generationId: number | null;
}

export function GenerationResult({ generationId }: GenerationResultProps) {
  const { currentGeneration, setCurrentGeneration, setIsGenerating, addToHistory } =
    useGenerationStore();
  const [lightboxImage, setLightboxImage] = useState<string | null>(null);

  useEffect(() => {
    if (!generationId) {
      setCurrentGeneration(null);
      return;
    }

    let intervalId: number | undefined;

    const fetchGeneration = async () => {
      try {
        const gen = await getGeneration(generationId);
        setCurrentGeneration(gen);
        addToHistory(gen);

        if (gen.status === "completed" || gen.status === "failed") {
          setIsGenerating(false);
          if (intervalId) clearInterval(intervalId);
        }
      } catch (error) {
        console.error("Failed to fetch generation:", error);
        setIsGenerating(false);
        if (intervalId) clearInterval(intervalId);
      }
    };

    fetchGeneration();
    intervalId = window.setInterval(fetchGeneration, 2000);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [generationId]);

  if (!generationId || !currentGeneration) {
    return (
      <Card className="h-full flex items-center justify-center">
        <CardContent className="text-center text-muted-foreground py-12">
          <p>Generate an image to see results here</p>
        </CardContent>
      </Card>
    );
  }

  const outputImages = currentGeneration.images.filter(
    (img) => img.image_type === "output"
  );

  const statusBadge = {
    pending: <Badge variant="secondary">Pending</Badge>,
    processing: (
      <Badge variant="default" className="bg-blue-500">
        <Loader2 className="mr-1 h-3 w-3 animate-spin" />
        Processing
      </Badge>
    ),
    completed: (
      <Badge variant="default" className="bg-green-500">
        <CheckCircle2 className="mr-1 h-3 w-3" />
        Completed
      </Badge>
    ),
    failed: (
      <Badge variant="destructive">
        <AlertCircle className="mr-1 h-3 w-3" />
        Failed
      </Badge>
    ),
  }[currentGeneration.status];

  return (
    <>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-lg">Result</CardTitle>
          {statusBadge}
        </CardHeader>
        <CardContent className="space-y-4">
          {currentGeneration.status === "processing" && (
            <div className="grid grid-cols-2 gap-4">
              {[...Array(2)].map((_, i) => (
                <Skeleton key={i} className="aspect-square rounded-lg" />
              ))}
            </div>
          )}

          {currentGeneration.status === "failed" && (
            <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
              <p className="text-destructive text-sm">
                {currentGeneration.error_message || "Generation failed"}
              </p>
            </div>
          )}

          {currentGeneration.status === "completed" && (
            <>
              {outputImages.length > 0 && (
                <div className="grid grid-cols-2 gap-4">
                  {outputImages.map((img) => (
                    <button
                      key={img.id}
                      onClick={() => setLightboxImage(img.file_path)}
                      className="relative aspect-square overflow-hidden rounded-lg border hover:ring-2 hover:ring-primary transition-all"
                    >
                      <img
                        src={getImageUrl(img.file_path)}
                        alt={`Generated ${img.index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}

              {currentGeneration.response_text && (
                <div className="bg-muted rounded-lg p-4">
                  <p className="text-sm whitespace-pre-wrap">
                    {currentGeneration.response_text}
                  </p>
                </div>
              )}
            </>
          )}

          <div className="text-xs text-muted-foreground">
            <p>Prompt: {currentGeneration.prompt}</p>
            <p>
              {currentGeneration.aspect_ratio} · {currentGeneration.resolution} ·{" "}
              {currentGeneration.thinking_level} · temp {currentGeneration.temperature}
            </p>
          </div>
        </CardContent>
      </Card>

      <ImageLightbox
        imagePath={lightboxImage}
        onClose={() => setLightboxImage(null)}
      />
    </>
  );
}
