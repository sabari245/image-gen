import { useState } from "react";
import { Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ImageUploader } from "./ImageUploader";
import { ParameterControls } from "./ParameterControls";
import { useGenerationStore } from "@/store/generation";
import { createGeneration } from "@/api/client";

interface GenerationFormProps {
  onGenerate: (id: number) => void;
}

export function GenerationForm({ onGenerate }: GenerationFormProps) {
  const [prompt, setPrompt] = useState("");
  const [aspectRatio, setAspectRatio] = useState("1:1");
  const [resolution, setResolution] = useState("2K");
  const [thinkingLevel, setThinkingLevel] = useState("high");
  const [temperature, setTemperature] = useState(1.0);

  const { selectedImages, clearSelectedImages, isGenerating, setIsGenerating, addToHistory } =
    useGenerationStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isGenerating) return;

    setIsGenerating(true);
    try {
      const generation = await createGeneration({
        prompt: prompt.trim(),
        aspect_ratio: aspectRatio,
        resolution,
        thinking_level: thinkingLevel,
        temperature,
        images: selectedImages,
      });
      addToHistory(generation);
      onGenerate(generation.id);
      setPrompt("");
      clearSelectedImages();
    } catch (error) {
      console.error("Generation failed:", error);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-5 w-5" />
          Generate Image
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Textarea
              placeholder="Describe the image you want to generate..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={3}
              className="resize-none"
            />
          </div>

          <ImageUploader />

          <ParameterControls
            aspectRatio={aspectRatio}
            resolution={resolution}
            thinkingLevel={thinkingLevel}
            temperature={temperature}
            onAspectRatioChange={setAspectRatio}
            onResolutionChange={setResolution}
            onThinkingLevelChange={setThinkingLevel}
            onTemperatureChange={setTemperature}
          />

          <Button
            type="submit"
            className="w-full"
            disabled={!prompt.trim() || isGenerating}
          >
            {isGenerating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Generate
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
