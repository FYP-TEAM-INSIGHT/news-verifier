import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Timeline } from "@/components/timeline";
import { VerificationFlow, VerificationResponse } from "@/lib/api";

interface AnalysisTabContentProps {
  result: VerificationResponse;
}

export default function AnalysisTabContent({
  result,
}: AnalysisTabContentProps) {
  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle>Verification Process Timeline</CardTitle>
        <CardDescription>
          Step-by-step analysis of the verification process
        </CardDescription>
      </CardHeader>
      <CardContent>
        {result.flow && result.flow.length > 0 ? (
          <Timeline
            items={result.flow.map((item) => ({
              step: item.step,
              result: item.result,
              status: "completed" as const,
            }))}
          />
        ) : (
          <div className="text-gray-500">
            No verification flow data available.
          </div>
        )}
      </CardContent>
    </Card>
  );
}
