"use client";

import React, { useState, useEffect } from "react";
import { useOpportunities } from "@/hooks/useOpportunities";

interface IngestStats {
  total_scraped: number;
  platform_counts: Record<string, number>;
}

// Helper to format source names: "APP_STORE" -> "App Store", "onlytech_forum" -> "Onlytech Forum"
function formatLabel(text: string) {
  if (!text) return "";
  return text
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}

export default function KPISection() {
  const { opportunities, loading: oppsLoading } = useOpportunities();
  const [stats, setStats] = useState<IngestStats | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const response = await fetch("/api/v1/ingest/stats");
        if (response.ok) {
          const data = await response.json();
          setStats(data);
        }
      } catch (err) {
        console.error("Failed to fetch stats", err);
      } finally {
        setStatsLoading(false);
      }
    }
    fetchStats();
  }, []);
  
  // Calculate total classified from opportunities
  const totalScraped = stats?.total_scraped || 0;
  
  // Map platform counts to display array
  const displaySources = stats && Object.keys(stats.platform_counts).length > 0
    ? Object.entries(stats.platform_counts).map(([platform, count]) => ({
        label: formatLabel(platform),
        count: count
      }))
    : [];

  if (oppsLoading || statsLoading) {
    return (
      <div className="flex flex-wrap gap-4 mb-xl">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-surface-container/40 border border-outline-variant/20 rounded-lg p-4 min-w-[140px] flex flex-col justify-center relative overflow-hidden animate-pulse">
            <div className="absolute top-0 left-4 right-4 h-[2px] bg-white/10"></div>
            <div className="h-8 bg-white/20 rounded w-1/2 mb-2"></div>
            <div className="h-4 bg-white/10 rounded w-3/4"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="flex flex-wrap gap-4 mb-xl">
      {/* Items Scraped */}
      <div className="bg-surface-container/60 border border-outline-variant/30 rounded-lg p-4 min-w-[140px] flex flex-col justify-center relative overflow-hidden">
        <div className="absolute top-0 left-4 right-4 h-[2px] bg-primary"></div>
        <div className="font-display-md text-display-md font-bold text-on-surface mb-1">
          {totalScraped}
        </div>
        <div className="font-body-sm text-body-sm text-on-surface-variant">
          Reviews Scraped
        </div>
      </div>



      {/* Sources Breakdown */}
      {displaySources.map((src, idx) => (
        <div key={idx} className="bg-surface-container/60 border border-outline-variant/30 rounded-lg p-4 min-w-[140px] flex flex-col justify-center relative overflow-hidden">
          <div className="absolute top-0 left-4 right-4 h-[2px] bg-secondary"></div>
          <div className="font-display-md text-display-md font-bold text-on-surface mb-1">
            {src.count}
          </div>
          <div className="font-body-sm text-body-sm text-on-surface-variant">
            {src.label}
          </div>
        </div>
      ))}
    </div>
  );
}
