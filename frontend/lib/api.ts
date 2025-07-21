export class APIError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = "APIError";
  }
}

export interface VerificationFlow {
  step: string;
  result: string;
}

export interface VerificationResponse {
  final_score: number;
  result: string;
  semantic_ranking: Array<{
    title: string;
    score: number;
    url: string;
  }>;
  breakdown: {
    entity_similarity: number;
    semantic_similarity: number;
    source_credibility: number;
    per_entity: {
      persons: number;
      locations: number;
      events: number;
      organizations: number;
    };
  };
  flow?: VerificationFlow[];
}

 const mockVerifyNews = async (text: string): Promise<VerificationResponse> => {
  const res = await fetch("/api/news/verify/simulate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const errorData = await res.json() as { detail: string };
    throw new APIError(errorData.detail, res.status);
  }

  const data = await res.json();
  console.log("Mock API response:", data);
  return data as VerificationResponse;
};

const realVerifyNews = async (text: string): Promise<VerificationResponse> => {
  const res = await fetch("/api/news/verify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const errorData = await res.json() as { detail: string };
    throw new APIError(errorData.detail, res.status);
  }

  const data = await res.json();
  console.log("Mock API response:", data);
  return data as VerificationResponse;
};

export const verifyNews = async (text: string, useMock: boolean): Promise<VerificationResponse> => {
  if (useMock) {
    console.log("Using mock API for verification");
    return mockVerifyNews(text);
  } else {
    return realVerifyNews(text);
  }
};
