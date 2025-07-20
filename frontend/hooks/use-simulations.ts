import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SimulationState {
    isEnabled: boolean;
    toggleSimulation: () => void;
}

export const useSimulationStore = create<SimulationState>()(
    persist(
        (set) => ({
            isEnabled: false,
            toggleSimulation: () => set((state) => ({ isEnabled: !state.isEnabled })),
        }),
        {
            name: "simulation-store", // key in localStorage
        }
    )
);