const API_BASE = "/api";

export interface GenerationImage {
  id: number;
  file_path: string;
  file_size: number;
  image_type: "input" | "output";
  index: number;
}

export interface Generation {
  id: number;
  prompt: string;
  aspect_ratio: string;
  resolution: string;
  thinking_level: string;
  temperature: number;
  response_text: string | null;
  status: "pending" | "processing" | "completed" | "failed";
  error_message: string | null;
  created_at: string;
  completed_at: string | null;
  images: GenerationImage[];
}

export interface HistoryResponse {
  items: Generation[];
  total: number;
  page: number;
  page_size: number;
}

export interface GenerationParams {
  prompt: string;
  aspect_ratio: string;
  resolution: string;
  thinking_level: string;
  temperature: number;
  images: File[];
}

export async function createGeneration(params: GenerationParams): Promise<Generation> {
  const formData = new FormData();
  formData.append("prompt", params.prompt);
  formData.append("aspect_ratio", params.aspect_ratio);
  formData.append("resolution", params.resolution);
  formData.append("thinking_level", params.thinking_level);
  formData.append("temperature", params.temperature.toString());

  for (const image of params.images) {
    formData.append("images", image);
  }

  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`Generation failed: ${res.statusText}`);
  }

  return res.json();
}

export async function getGeneration(id: number): Promise<Generation> {
  const res = await fetch(`${API_BASE}/generations/${id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch generation: ${res.statusText}`);
  }
  return res.json();
}

export async function getHistory(page = 1, pageSize = 20): Promise<HistoryResponse> {
  const res = await fetch(`${API_BASE}/history?page=${page}&page_size=${pageSize}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch history: ${res.statusText}`);
  }
  return res.json();
}

export async function deleteGeneration(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/generations/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    throw new Error(`Failed to delete generation: ${res.statusText}`);
  }
}

export function getImageUrl(filePath: string): string {
  return `${API_BASE}/images/${filePath}`;
}
