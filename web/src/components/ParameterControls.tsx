import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const ASPECT_RATIOS = [
  "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1",
  "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
];

const RESOLUTIONS = ["512", "1K", "2K", "4K"];

interface ParameterControlsProps {
  aspectRatio: string;
  resolution: string;
  thinkingLevel: string;
  temperature: number;
  onAspectRatioChange: (value: string) => void;
  onResolutionChange: (value: string) => void;
  onThinkingLevelChange: (value: string) => void;
  onTemperatureChange: (value: number) => void;
}

export function ParameterControls({
  aspectRatio,
  resolution,
  thinkingLevel,
  temperature,
  onAspectRatioChange,
  onResolutionChange,
  onThinkingLevelChange,
  onTemperatureChange,
}: ParameterControlsProps) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="space-y-2">
        <Label>Aspect Ratio</Label>
        <Select value={aspectRatio} onValueChange={onAspectRatioChange}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {ASPECT_RATIOS.map((ratio) => (
              <SelectItem key={ratio} value={ratio}>
                {ratio}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label>Resolution</Label>
        <Select value={resolution} onValueChange={onResolutionChange}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {RESOLUTIONS.map((res) => (
              <SelectItem key={res} value={res}>
                {res}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label>Thinking Level</Label>
        <Select value={thinkingLevel} onValueChange={onThinkingLevelChange}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="minimal">Minimal</SelectItem>
            <SelectItem value="high">High</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label>Temperature: {temperature.toFixed(1)}</Label>
        <Slider
          value={[temperature]}
          onValueChange={([val]) => onTemperatureChange(val)}
          min={0}
          max={2}
          step={0.1}
          className="mt-2"
        />
      </div>
    </div>
  );
}
