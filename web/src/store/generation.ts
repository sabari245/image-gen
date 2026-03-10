import { create } from "zustand";
import type { Generation } from "@/api/client";

interface GenerationState {
  currentGeneration: Generation | null;
  selectedImages: File[];
  history: Generation[];
  historyTotal: number;
  historyPage: number;
  isGenerating: boolean;
  isSidebarOpen: boolean;

  setCurrentGeneration: (gen: Generation | null) => void;
  updateCurrentGeneration: (gen: Generation) => void;
  addSelectedImage: (file: File) => void;
  removeSelectedImage: (index: number) => void;
  clearSelectedImages: () => void;
  setHistory: (items: Generation[], total: number, page: number) => void;
  addToHistory: (gen: Generation) => void;
  removeFromHistory: (id: number) => void;
  setIsGenerating: (val: boolean) => void;
  setSidebarOpen: (val: boolean) => void;
}

export const useGenerationStore = create<GenerationState>((set) => ({
  currentGeneration: null,
  selectedImages: [],
  history: [],
  historyTotal: 0,
  historyPage: 1,
  isGenerating: false,
  isSidebarOpen: true,

  setCurrentGeneration: (gen) => set({ currentGeneration: gen }),
  updateCurrentGeneration: (gen) =>
    set((state) => ({
      currentGeneration:
        state.currentGeneration?.id === gen.id ? gen : state.currentGeneration,
    })),
  addSelectedImage: (file) =>
    set((state) => ({ selectedImages: [...state.selectedImages, file] })),
  removeSelectedImage: (index) =>
    set((state) => ({
      selectedImages: state.selectedImages.filter((_, i) => i !== index),
    })),
  clearSelectedImages: () => set({ selectedImages: [] }),
  setHistory: (items, total, page) =>
    set({ history: items, historyTotal: total, historyPage: page }),
  addToHistory: (gen) =>
    set((state) => ({
      history: [gen, ...state.history.filter((g) => g.id !== gen.id)],
      historyTotal: state.historyTotal + 1,
    })),
  removeFromHistory: (id) =>
    set((state) => ({
      history: state.history.filter((g) => g.id !== id),
      historyTotal: Math.max(0, state.historyTotal - 1),
    })),
  setIsGenerating: (val) => set({ isGenerating: val }),
  setSidebarOpen: (val) => set({ isSidebarOpen: val }),
}));
