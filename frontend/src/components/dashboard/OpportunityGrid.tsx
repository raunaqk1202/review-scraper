"use client";

import React from "react";
import { useOpportunities } from "@/hooks/useOpportunities";

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

  const sortedOpportunities = [...opportunities].sort((a, b) => b.supporting_conversations - a.supporting_conversations);
  const total = sortedOpportunities.length;

  const getColorClass = (index: number) => {
    if (total === 0) return "bg-surface-container/40 border-outline-variant/30 text-on-surface";
    if (index < total / 3) return "bg-emerald-500 border-emerald-400 text-white shadow-[0_0_15px_rgba(16,185,129,0.2)]";
    if (index < (2 * total) / 3) return "bg-amber-500 border-amber-400 text-white shadow-[0_0_15px_rgba(245,158,11,0.2)]";
    return "bg-rose-500 border-rose-400 text-white shadow-[0_0_15px_rgba(244,63,94,0.2)]";
  };

  return (
    <div className="flex flex-col gap-4 pb-xl">
      {sortedOpportunities.map((opp, index) => {
        return (
          <div key={opp.id} className={`border rounded-lg p-0 overflow-hidden flex flex-col ${getColorClass(index)}`}>
            {/* Top row with title only */}
            <div className="flex items-center justify-between p-4 border-b border-white/20 bg-black/20">
              <h4 className="font-headline-sm text-headline-sm font-semibold flex-grow">
                {opp.title}
              </h4>
            </div>
            
            {/* Description / Sub-item row */}
            {opp.description && (
              <div className="p-4 text-white/90 text-body-sm leading-relaxed">
                {opp.description}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
