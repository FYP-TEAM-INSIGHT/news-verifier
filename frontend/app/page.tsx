"use client";

import { useState } from "react";
import { APIError, VerificationResponse, verifyNews } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Loader2,
  Shield,
  XCircle,
  ExternalLink,
  AlertTriangle,
} from "lucide-react";
import { useSimulationStore } from "@/hooks/use-simulations";

// Configurable color thresholds
const COLOR_THRESHOLDS = {
  red: { min: 0, max: 50 },
  yellow: { min: 51, max: 70 },
  green: { min: 71, max: 100 },
};

interface AnalyzedTextSummaryProps {
  newsText: string;
}

function AnalyzedTextSummary({ newsText }: AnalyzedTextSummaryProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const previewLength = 150;
  const shouldShowExpand = newsText.length > previewLength;

  return (
    <Card className="shadow-lg border-l-4 border-l-blue-500">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg text-gray-700">Analyzed Text</CardTitle>
          <Badge variant="secondary" className="text-xs">
            {newsText.length} characters
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="bg-gray-50 rounded-lg p-4 border-l-2 border-l-gray-300">
          <div className="text-gray-800 leading-relaxed">
            {isExpanded ? (
              <div className="whitespace-pre-wrap">{newsText}</div>
            ) : (
              <div>
                {shouldShowExpand ? (
                  <>
                    <span className="whitespace-pre-wrap">
                      {newsText.substring(0, previewLength)}
                    </span>
                    <span className="text-gray-500">...</span>
                  </>
                ) : (
                  <span className="whitespace-pre-wrap">{newsText}</span>
                )}
              </div>
            )}
          </div>

          {shouldShowExpand && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsExpanded(!isExpanded)}
              className="mt-3 text-blue-600 hover:text-blue-800 p-0 h-auto font-medium"
            >
              {isExpanded ? "Show Less" : "Show More"}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export default function NewsVerifier() {
  const [newsText, setNewsText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<VerificationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiError, setApiError] = useState<{
    message: string;
    status: number;
  } | null>(null);
  const [viewMode, setViewMode] = useState<"input" | "results">("input");
  const {isEnabled} = useSimulationStore();

  const getScoreColor = (score: number) => {
    const percentage = Math.round(score * 100);
    if (percentage >= COLOR_THRESHOLDS.green.min) return "text-green-600";
    if (percentage >= COLOR_THRESHOLDS.yellow.min) return "text-yellow-600";
    return "text-red-600";
  };

  const getProgressColor = (score: number) => {
    const percentage = Math.round(score * 100);
    if (percentage >= COLOR_THRESHOLDS.green.min) return "bg-green-500";
    if (percentage >= COLOR_THRESHOLDS.yellow.min) return "bg-yellow-500";
    return "bg-red-500";
  };

  const handleVerify = async () => {
    if (!newsText.trim()) {
      setError("Please enter some news text to verify");
      return;
    }

    setIsLoading(true);
    setError(null);
    setApiError(null);
    setResult(null);

    try {
      const data = await verifyNews(newsText, isEnabled);
      setResult(data);
      setViewMode("results");
    } catch (err) {
      if (err instanceof APIError) {
        // Handle specific API errors
        setApiError({ message: err.message, status: err.status });
        setViewMode("results"); // Show the error in results mode
      } else {
        // Handle general errors
        setError("Failed to verify news. Please try again.");
        console.error("Verification error:", err);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyAnother = () => {
    setNewsText("");
    setResult(null);
    setError(null);
    setApiError(null);
    setViewMode("input");
  };

  return (
    <div>
      {/* Main Input Section */}
      <div className="max-w-4xl mx-auto mb-8">
        {viewMode === "input" ? (
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl">Enter News Text</CardTitle>
              <CardDescription>
                Paste the news article or social media post you want to verify
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Paste your news text here..."
                value={newsText}
                onChange={(e) => setNewsText(e.target.value)}
                className="min-h-[200px] text-base"
                disabled={isLoading}
              />

              {error && (
                <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-md">
                  <XCircle className="h-5 w-5" />
                  <span>{error}</span>
                </div>
              )}

              <div className="flex justify-center">
                <Button
                  onClick={handleVerify}
                  disabled={isLoading || !newsText.trim()}
                  size="lg"
                  className="px-12 py-3 text-lg font-semibold"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Verifying...
                    </>
                  ) : (
                    "VERIFY"
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <AnalyzedTextSummary newsText={newsText} />
        )}
      </div>

      {/* API Error Section */}
      {apiError && (
        <div className="max-w-4xl mx-auto mb-8">
          <Card className="shadow-lg border-l-4 border-l-red-500">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <AlertTriangle className="h-6 w-6 text-red-600" />
                <CardTitle className="text-xl text-red-700">
                  Verification Error
                </CardTitle>
                <Badge variant="destructive" className="text-sm">
                  Error {apiError.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                <p className="text-red-800 font-medium">{apiError.message}</p>
                <p className="text-red-600 text-sm mt-2">
                  Please try with different news content or check our supported
                  formats.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Main Result */}
          <Card className="shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">Verification Result</CardTitle>
                <Badge
                  variant={
                    result.result.includes("NOT FAKE")
                      ? "default"
                      : "destructive"
                  }
                  className="text-lg px-4 py-2"
                >
                  {result.result}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-lg font-medium">
                      Overall Credibility Score
                    </span>
                    <span
                      className={`text-2xl font-bold ${getScoreColor(
                        result.final_score
                      )}`}
                    >
                      {Math.round(result.final_score * 100)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-300 ${getProgressColor(
                        result.final_score
                      )}`}
                      style={{ width: `${result.final_score * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Detailed Breakdown */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle>Detailed Analysis</CardTitle>
              <CardDescription>
                Breakdown of verification metrics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Main Metrics */}
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Core Metrics</h3>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span>Entity Similarity</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(
                              result.breakdown.entity_similarity
                            )}`}
                            style={{
                              width: `${
                                result.breakdown.entity_similarity * 100
                              }%`,
                            }}
                          ></div>
                        </div>
                        <span
                          className={`font-medium ${getScoreColor(
                            result.breakdown.entity_similarity
                          )}`}
                        >
                          {Math.round(result.breakdown.entity_similarity * 100)}
                          %
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <span>Semantic Similarity</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(
                              result.breakdown.semantic_similarity
                            )}`}
                            style={{
                              width: `${
                                result.breakdown.semantic_similarity * 100
                              }%`,
                            }}
                          ></div>
                        </div>
                        <span
                          className={`font-medium ${getScoreColor(
                            result.breakdown.semantic_similarity
                          )}`}
                        >
                          {Math.round(
                            result.breakdown.semantic_similarity * 100
                          )}
                          %
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <span>Source Credibility</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(
                              result.breakdown.source_credibility
                            )}`}
                            style={{
                              width: `${
                                result.breakdown.source_credibility * 100
                              }%`,
                            }}
                          ></div>
                        </div>
                        <span
                          className={`font-medium ${getScoreColor(
                            result.breakdown.source_credibility
                          )}`}
                        >
                          {Math.round(
                            result.breakdown.source_credibility * 100
                          )}
                          %
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Entity Analysis */}
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Entity Analysis</h3>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span>Persons</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(
                              result.breakdown.per_entity.persons
                            )}`}
                            style={{
                              width: `${
                                result.breakdown.per_entity.persons * 100
                              }%`,
                            }}
                          ></div>
                        </div>
                        <span
                          className={`font-medium ${getScoreColor(
                            result.breakdown.per_entity.persons
                          )}`}
                        >
                          {Math.round(
                            result.breakdown.per_entity.persons * 100
                          )}
                          %
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <span>Locations</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(
                              result.breakdown.per_entity.locations
                            )}`}
                            style={{
                              width: `${
                                result.breakdown.per_entity.locations * 100
                              }%`,
                            }}
                          ></div>
                        </div>
                        <span
                          className={`font-medium ${getScoreColor(
                            result.breakdown.per_entity.locations
                          )}`}
                        >
                          {Math.round(
                            result.breakdown.per_entity.locations * 100
                          )}
                          %
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <span>Events</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(
                              result.breakdown.per_entity.events
                            )}`}
                            style={{
                              width: `${
                                result.breakdown.per_entity.events * 100
                              }%`,
                            }}
                          ></div>
                        </div>
                        <span
                          className={`font-medium ${getScoreColor(
                            result.breakdown.per_entity.events
                          )}`}
                        >
                          {Math.round(result.breakdown.per_entity.events * 100)}
                          %
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <span>Organizations</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(
                              result.breakdown.per_entity.organizations
                            )}`}
                            style={{
                              width: `${
                                result.breakdown.per_entity.organizations * 100
                              }%`,
                            }}
                          ></div>
                        </div>
                        <span
                          className={`font-medium ${getScoreColor(
                            result.breakdown.per_entity.organizations
                          )}`}
                        >
                          {Math.round(
                            result.breakdown.per_entity.organizations * 100
                          )}
                          %
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Relevant News */}
          {result.relevant_news && result.relevant_news.length > 0 && (
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle>Related News Sources</CardTitle>
                <CardDescription>
                  Similar news articles found for cross-reference
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.relevant_news.map((news, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center space-x-3">
                        <Badge variant="outline">
                          {Math.round(news.score * 100)}% match
                        </Badge>
                        <span className="text-sm text-gray-600">
                          Related source
                        </span>
                      </div>
                      <Button variant="ghost" size="sm" asChild>
                        <a
                          href={news.link}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <ExternalLink className="h-4 w-4 mr-1" />
                          View
                        </a>
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Verify Another Button */}
      {viewMode === "results" && (result || apiError) && (
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-center pt-8">
            <Button
              onClick={handleVerifyAnother}
              size="lg"
              variant="outline"
              className="px-8 py-3 text-lg font-semibold bg-transparent"
            >
              Verify Another News
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
