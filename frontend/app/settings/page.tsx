"use client";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { useSimulationStore } from "@/hooks/use-simulations";

export default function Page() {
  const { isEnabled, toggleSimulation } = useSimulationStore();
  return (
    <div className="bg-white p-6 rounded-xl shadow-md flex flex-col items-start space-y-4">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-gray-600">Adjust your application settings below.</p>
      </div>

      <div className="flex items-center space-x-2">
        <Switch
          id="animations"
          checked={isEnabled}
          onCheckedChange={toggleSimulation}
        />
        <Label htmlFor="animations" className=" font-medium">
          Enable Simulations for API
        </Label>
      </div>
      <p className="text-xs text-gray-500 mt-1">
        This setting allows you to simulate API responses for testing purposes.
        When enabled, the application will use mock api instead of making real
        API calls.
      </p>

      <div className="w-full mt-8">
        <Button
          variant="default"
          className="w-full"
          onClick={() => (window.location.href = "/")}
        >
          Go Back to Home
        </Button>
      </div>
    </div>
  );
}
