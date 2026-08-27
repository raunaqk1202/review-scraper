import React from "react";
import KPISection from "@/components/dashboard/KPISection";
import OpportunityGrid from "@/components/dashboard/OpportunityGrid";

export default function Home() {
  return (
    <main className="ml-[var(--spacing-sidebar-width)] w-[calc(100%-var(--spacing-sidebar-width)-var(--spacing-panel-right-width))] pt-24 px-xl pb-xl h-screen overflow-y-auto relative z-10">
      {/* Header Section */}
      <div className="mb-lg">

        <h2 className="font-display-lg text-display-lg font-bold text-on-surface mb-xs tracking-tight">
          Opportunity-Discovery Engine
        </h2>
        <p className="font-body-lg text-body-lg text-on-surface-variant max-w-3xl">
          AI-classified themes from global data streams — surfacing unmet user needs and market gaps.
        </p>
      </div>

      <KPISection />
      
      <div className="flex items-baseline justify-between mb-xs mt-xl">
        <h3 className="font-headline-md text-headline-md font-semibold text-on-surface">
          Opportunities
        </h3>
      </div>

      {/* Scoring formula explanation */}
      <div className="glass-card rounded-lg p-4 mb-md border border-white/10">
        <div className="flex items-start gap-3">
          <span className="text-primary text-lg mt-0.5">ƒ</span>
          <div>
            <p className="text-body-sm font-semibold text-on-surface mb-1">
              Score = 35% × User Pain + 30% × Business Impact + 20% × Reach + 15% × Evidence Strength
            </p>
            <p className="text-body-sm text-on-surface-variant leading-relaxed">
              Each dimension is rated 1.0–5.0 by the AI, producing a 0–100 composite score.
              Opportunities are ranked by composite score to surface the most impactful product opportunities first.
            </p>
          </div>
        </div>
      </div>

      <OpportunityGrid />
    </main>
  );
}
