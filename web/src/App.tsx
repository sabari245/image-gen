import { useState } from "react";
import { GenerationForm } from "@/components/GenerationForm";
import { GenerationResult } from "@/components/GenerationResult";
import { HistorySidebar } from "@/components/HistorySidebar";
import { ThemeProvider } from "@/components/theme-provider";

export function App() {
  const [currentGenerationId, setCurrentGenerationId] = useState<number | null>(
    null
  );

  return (
    <ThemeProvider defaultTheme="dark" storageKey="image-gen-theme">
      <div className="flex h-screen bg-background">
        <HistorySidebar
          onSelect={setCurrentGenerationId}
          currentId={currentGenerationId}
        />

        <main className="flex-1 p-6 overflow-auto">
          <div className="max-w-4xl mx-auto space-y-6">
            <header className="text-center mb-8">
              <h1 className="text-3xl font-bold">Image Generator</h1>
              <p className="text-muted-foreground">
                Generate images with Gemini AI
              </p>
            </header>

            <div className="grid md:grid-cols-2 gap-6">
              <GenerationForm onGenerate={setCurrentGenerationId} />
              <GenerationResult generationId={currentGenerationId} />
            </div>
          </div>
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;
