"use client";

import { useState, useEffect } from "react";

export interface OpportunityScore {
  reach: number;
  severity: number;
  business_impact: number;
  evidence_strength: number;
  composite_score: number;
}

export interface Opportunity {
  id: string;
  title: string;
  description?: string;
  supporting_conversations: number;
  score?: OpportunityScore;
}

export function useOpportunities() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchOpportunities() {
      try {
        const response = await fetch("/api/v1/opportunities");
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
        const data = await response.json();
        setOpportunities(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    }

    fetchOpportunities();
  }, []);

  return { opportunities, loading, error };
}
