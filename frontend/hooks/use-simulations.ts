import { create } from "zustand";

interface SimulationState {
    isEnabled: boolean;
    toggleSimulation: () => void;
}

export const useSimulationStore = create<SimulationState>((set) => ({
    isEnabled: false,
    toggleSimulation: () => set((state) => ({ isEnabled: !state.isEnabled })),
}));