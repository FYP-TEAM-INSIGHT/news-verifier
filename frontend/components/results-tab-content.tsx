import React from "react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { VerificationResponse } from "@/lib/api";
import { ExternalLink } from "lucide-react";
import { Button } from "./ui/button";


const COLOR_THRESHOLDS = {
  red: { min: 0, max: 50 },
  yellow: { min: 51, max: 70 },
  green: { min: 71, max: 100 },
};

interface ResultsTabContentProps {
  result: VerificationResponse;
}


export default function ResultsTabContent({ result }: ResultsTabContentProps) {

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
  return (
       <div className="space-y-6">
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

          {/* Semantic Ranking */}
          {result.semantic_ranking && result.semantic_ranking.length > 0 && (
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle>Related News Sources - Semantic Ranking</CardTitle>
                <CardDescription>
                  Similar news articles found for cross-reference 
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.semantic_ranking.map((news, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center space-x-3">
                        <Badge variant="outline">
                          {Math.round(news.score * 100)}% match
                        </Badge>
                        <span className="text-sm text-gray-600">
                          {news.title.length > 70
                            ? `${news.title.substring(0, 70)}...`
                            : news.title}{" "}
                        </span>
                      </div>
                      <Button variant="ghost" size="sm" asChild>
                        <a
                          href={news.url}
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
  );
}