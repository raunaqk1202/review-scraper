export type EvidenceLevel = 'OBSERVED' | 'DERIVED' | 'HYPOTHESIZED';
export type JourneyStage = 'DISCOVERY' | 'BROWSING' | 'PRODUCT_CONSIDERATION' | 'SHORTLISTING' | 'COMPARISON' | 'WISHLIST' | 'EVALUATION' | 'PURCHASE' | 'PURCHASE_POSTPONEMENT' | 'ABANDONMENT' | 'POST_PURCHASE';

export interface OpportunityScore {
  composite_score: number;
  reach: number;
  frequency: number;
  severity: number;
  business_impact: number;
  evidence_strength: number;
}

export interface Opportunity {
  id: string;
  title: string;
  description: string;
  user_segment: string;
  evidence_level: EvidenceLevel;
  confidence_level: number;
  score?: OpportunityScore;
}
