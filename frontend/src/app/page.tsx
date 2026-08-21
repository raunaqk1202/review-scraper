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
      <div className="flex flex-col gap-1 mb-md text-body-sm text-on-surface-variant">
        <p>Colors indicate the volume of users facing the issue based on the reviews across different platforms:</p>
        <div className="flex gap-4 mt-1">
          <div className="flex items-center gap-1" title="High volume of affected users - Primary focus areas"><div className="w-3 h-3 rounded-full bg-emerald-500"></div> High</div>
          <div className="flex items-center gap-1" title="Medium volume of affected users - Secondary focus areas"><div className="w-3 h-3 rounded-full bg-amber-500"></div> Medium</div>
          <div className="flex items-center gap-1" title="Low volume of affected users - Emerging or niche issues"><div className="w-3 h-3 rounded-full bg-rose-500"></div> Low</div>
        </div>
      </div>
      <OpportunityGrid />
    </main>
  );
}
