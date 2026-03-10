import { Download, ImagePlus } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { getImageUrl } from "@/api/client";
import { useGenerationStore } from "@/store/generation";

interface ImageLightboxProps {
  imagePath: string | null;
  onClose: () => void;
}

export function ImageLightbox({ imagePath, onClose }: ImageLightboxProps) {
  const { addSelectedImage } = useGenerationStore();

  if (!imagePath) return null;

  const imageUrl = getImageUrl(imagePath);

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = imagePath.split("/").pop() || "image.webp";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleUseAsInput = async () => {
    try {
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      const fileName = imagePath.split("/").pop() || "image.webp";
      const file = new File([blob], fileName, { type: blob.type });
      addSelectedImage(file);
      onClose();
    } catch (error) {
      console.error("Failed to add image as input:", error);
    }
  };

  return (
    <Dialog open={!!imagePath} onOpenChange={() => onClose()}>
      <DialogContent className="max-w-4xl">
        <DialogHeader>
          <DialogTitle className="flex items-center justify-between">
            <span>Generated Image</span>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={handleUseAsInput}>
                <ImagePlus className="mr-2 h-4 w-4" />
                Use as Input
              </Button>
              <Button variant="outline" size="sm" onClick={handleDownload}>
                <Download className="mr-2 h-4 w-4" />
                Download
              </Button>
            </div>
          </DialogTitle>
        </DialogHeader>
        <div className="flex items-center justify-center">
          <img
            src={imageUrl}
            alt="Generated"
            className="max-h-[70vh] object-contain rounded-lg"
          />
        </div>
      </DialogContent>
    </Dialog>
  );
}
