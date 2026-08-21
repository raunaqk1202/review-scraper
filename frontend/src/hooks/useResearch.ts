import { useState } from "react";

export interface AISource {
  id: string;
  journey_stage?: string;
  signal_type?: string;
  confidence_score?: number;
}

export interface ResearchQueryResponse {
  query: string;
  answer: string;
  sources: AISource[];
}

export function useResearch() {
  const [response, setResponse] = useState<ResearchQueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const askQuestion = async (query: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/research/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) {
        throw new Error(`Error: ${res.statusText}`);
      }
      const data: ResearchQueryResponse = await res.json();
      setResponse(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return { response, loading, error, askQuestion };
}
