"use client";

import React from "react";
import { useOpportunities } from "@/hooks/useOpportunities";

const DIMENSION_CONFIG = [
  { key: "user_pain", label: "Pain", color: "bg-red-500/20 text-red-300 border-red-500/30" },
  { key: "business_impact", label: "Impact", color: "bg-amber-500/20 text-amber-300 border-amber-500/30" },
  { key: "reach", label: "Reach", color: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  { key: "evidence_strength", label: "Evidence", color: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
] as const;

export default function OpportunityGrid() {
  const { opportunities, loading, error } = useOpportunities();

  if (loading) {
    return (
      <div className="flex flex-col gap-4 pb-xl">
        {[1, 2, 3].map((i) => (
          <div key={i} className="border rounded-lg p-0 overflow-hidden flex flex-col bg-surface-container/20 border-outline-variant/30 animate-pulse">
            <div className="p-4 border-b border-white/10 bg-black/10">
              <div className="h-6 bg-white/20 rounded w-1/3"></div>
            </div>
            <div className="p-4">
              <div className="h-4 bg-white/10 rounded w-full mb-2"></div>
              <div className="h-4 bg-white/10 rounded w-5/6"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return <div className="text-error">Error loading opportunities: {error.message}</div>;
  }

  if (opportunities.length === 0) {
    return <div className="text-on-surface-variant">No opportunities found. Please run the pipeline.</div>;
  }

  // Sort by composite score (0–100), descending
  const sortedOpportunities = [...opportunities].sort((a, b) => {
    const scoreA = a.score?.composite_score ?? 0;
    const scoreB = b.score?.composite_score ?? 0;
    return scoreB - scoreA;
  });

  return (
    <div className="flex flex-col gap-4 pb-xl">
      {sortedOpportunities.map((opp, index) => {
        const composite = opp.score?.composite_score ?? 0;
        const scorePercent = composite.toFixed(1);

        return (
          <div key={opp.id} className="glass-card rounded-lg p-0 overflow-hidden flex flex-col text-on-surface">
            {/* Header row */}
            <div className="flex items-center justify-between p-4 border-b border-white/20 bg-black/20">
              <div className="flex items-center gap-3 flex-grow min-w-0">
                <span className="text-body-sm font-bold text-on-surface-variant bg-white/10 w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0">
                  {index + 1}
                </span>
                <h4 className="font-headline-sm text-headline-sm font-semibold truncate">
                  {opp.title}
                </h4>
              </div>
              <div className="flex items-center gap-2 ml-4 flex-shrink-0">
                <div className="text-headline-sm font-bold text-primary">
                  {scorePercent}
                </div>
                <div className="text-body-sm text-on-surface-variant">
                  /100
                </div>
              </div>
            </div>
            
            {/* Description */}
            {opp.description && (
              <div className="px-4 pt-3 pb-2 text-white/90 text-body-sm leading-relaxed">
                {opp.description}
              </div>
            )}

            {/* Score dimension badges */}
            {opp.score && (
              <div className="px-4 pb-3 pt-1 flex flex-wrap gap-2">
                {DIMENSION_CONFIG.map(({ key, label, color }) => {
                  const value = opp.score?.[key as keyof typeof opp.score] as number | undefined;
                  if (value == null) return null;
                  return (
                    <span
                      key={key}
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${color}`}
                    >
                      {label}
                      <span className="font-bold">{value.toFixed(1)}</span>
                    </span>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
