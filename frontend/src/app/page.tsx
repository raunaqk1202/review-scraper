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
        <p>The percentage represents the proportion of reviews corresponding to each opportunity relative to the total number of classified reviews.</p>
      </div>
      <OpportunityGrid />
    </main>
  );
}
