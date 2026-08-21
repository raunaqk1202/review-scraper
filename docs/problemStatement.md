# AI-Powered Fashion Purchase Discovery Intelligence Engine

> **Core Discovery Loop:** Question → Evidence → Analysis → Pattern → Opportunity → Business Relevance

---

## 1. Role

Act as a senior product engineer, AI engineer, data engineer, and product designer.

Design and build an MVP of an **AI-powered customer discovery and opportunity intelligence engine for Myntra**.

> **This is NOT a sentiment-analysis or review-summarization application.**

The purpose is to help a Product Manager understand:
- **Why** users behave the way they do during fashion-shopping journeys
- **What** prevents them from progressing toward purchase
- **Which** recurring unmet needs represent meaningful product opportunities

---

## 2. Business Problem

Myntra has large amounts of user-generated feedback distributed across:

| Source Type | Examples |
|---|---|
| App Reviews | App Store reviews, Google Play reviews |
| Community | Reddit, fashion/shopping communities |
| Social | Public social-media conversations |
| Video | YouTube comments |
| Product Feedback | Product reviews, Product Q&A |
| Other | Other publicly available conversations about fashion and online shopping |

This feedback contains valuable signals about **user intent, uncertainty, purchase barriers, comparison behavior, and unmet needs**.

However, raw feedback is fragmented and difficult for PMs to systematically analyze.

### Limitations of Traditional Approaches

Traditional methods such as sentiment analysis, keyword extraction, topic modeling, review summaries, and word clouds can tell a PM *what* users are talking about — but **not sufficiently explain**:

> What is the user trying to accomplish? Why are they behaving this way? What uncertainty or friction prevents progression? How widespread is the problem? Which segments experience it? Could it affect a business metric? And what product opportunity could address it?

**The system should solve this problem.**

---

## 3. Primary Business Objective

The initial version focuses on understanding factors that influence:

### Wishlist → Purchase Conversion

> **Why do users wishlist fashion products but fail to purchase them, and what product opportunities could increase the probability of purchase?**

The architecture should be flexible enough to later support:

- Product conversion
- Add-to-cart → purchase conversion
- Repeat purchase
- Search → product-view conversion
- Reduced purchase abandonment
- Engagement
- Customer retention

---

## 4. Core Product Questions

The system must investigate questions across the following areas:

### 4.1 Wishlist Behavior

- Why do users wishlist products?
- What percentage/signals indicate genuine purchase intent?
- When is wishlisting simply bookmarking?
- What causes users to wishlist multiple competing products?
- Why do users wishlist but never purchase?

### 4.2 Purchase Hesitation

- What prevents a wishlisted product from being purchased?
- What causes users to postpone purchases?
- What uncertainties remain after users identify a product they like?
- What information prevents users from feeling confident enough to purchase?

### 4.3 Product Comparison

- How do users compare multiple shortlisted products?
- Which attributes matter during comparison?
- What trade-offs do users make?
- What causes one product to win over another?

### 4.4 External Research

- What information do users seek outside Myntra?
- Why do they leave Myntra to find that information?
- Which external sources do they trust?
- What unmet information needs could potentially be solved within Myntra?

### 4.5 Fashion-Specific Factors

Analyze the role of:

| Category | Factors |
|---|---|
| **Fit & Sizing** | Fit, Size, Body type |
| **Aesthetics** | Styling, Color, Versatility, Product imagery |
| **Context** | Occasion, Trends |
| **Economics** | Price, Discounts |
| **Trust & Proof** | Reviews, Ratings, Quality, Fabric/material, Brand, Social validation, Influencer validation |
| **Logistics** | Returns/exchanges, Delivery, Availability |

The system must also identify **interactions** between factors:

- Fit uncertainty + return anxiety
- Price + quality uncertainty
- Occasion + styling uncertainty
- Reviews + social validation
- Discount waiting + purchase postponement

---

## 5. Target User

The primary user is a **Product Manager / Product Researcher**.

The PM should be able to enter a natural-language research question such as:

> "Why are users wishlisting women's dresses but not buying them?"

> "What are the biggest purchase barriers for users buying occasion wear?"

> "What information do users seek outside Myntra before purchasing footwear?"

The system should transform the question into a **structured research analysis**.

---

## 6. Data Sources

Design the system to support ingestion from:

- App Store reviews
- Google Play reviews
- Reddit
- Public social-media conversations
- YouTube comments
- Fashion communities
- Shopping communities
- Product reviews
- Product Q&A
- Other publicly available sources

> **MVP Guidance:** Use sample/mock data if live source APIs or compliant ingestion mechanisms are not available. Do not block the application on external API integrations. The architecture should make real ingestion replaceable later.

---

## 7. Data Model

Create a structured representation of each feedback item capturing:

### 7.1 Source

- Source platform
- URL/reference
- Date
- Conversation/thread ID (where available)
- Anonymized author ID (where applicable)

### 7.2 Product Context

- Product
- Brand
- Category
- Subcategory
- Price band
- Product attributes (where identifiable)

### 7.3 User Context

Where evidence allows:

- User segment
- New vs returning user
- Purchase frequency
- Category familiarity
- Intent level

> ⚠️ Do not invent user attributes that are not supported by evidence.

### 7.4 Behavioral Context

Classify the shopping journey into stages:

```
Discovery → Browsing → Product Consideration → Shortlisting → Comparison → Wishlist → Evaluation → Purchase → Purchase Postponement → Abandonment → Post-purchase
```

### 7.5 AI-Derived Signals

Extract:

- Intent
- Motivation
- Uncertainty
- Barrier
- Decision criteria
- Desired outcome
- Purchase outcome
- External information seeking
- Competitor/alternative mention
- Unmet need
- Opportunity theme
- Confidence

---

## 8. Observation vs Inference (Critical Requirement)

The system **must** distinguish between three evidence levels:

| Level | Definition | Example |
|---|---|---|
| **Observed** | Something directly present in the source | User says they are unsure whether the dress will fit |
| **Derived** | A pattern supported by multiple observations | Fit uncertainty appears frequently among users evaluating dresses |
| **Hypothesized** | A potential explanation or business implication | Fit uncertainty may contribute to wishlist-to-purchase drop-off |

> ⚠️ **Never present hypotheses as established facts.**

---

## 9. AI Analysis Pipeline

Build the analysis pipeline in stages:

### Stage 1 — Cleaning

- Remove spam
- Remove duplicates
- Normalize text
- Detect language (where relevant)
- Preserve original source
- Preserve original context

### Stage 2 — Semantic Enrichment

Use **Groq LLM** to identify:

- Intent, Journey stage, Motivation, Uncertainty, Barrier
- Decision criteria, Outcome
- Product/category, Relevant attributes

### Stage 3 — Semantic Clustering

Group semantically similar conversations. For example:

> "Not sure if this will look good on me."
> "Would this suit my body type?"
> "Wish they showed this on different body shapes."

Should cluster under: **Appearance / fit confidence** — not three unrelated topics.

### Stage 4 — Pattern Detection

Identify recurring patterns across: Users, Products, Categories, Sources, Segments, Time periods.

### Stage 5 — Opportunity Generation

Convert recurring patterns into potential **unmet needs** and **product opportunities**.

---

## 10. Opportunity Framework

The central output should be an **Opportunity Map**, not a list of topics.

### Opportunity Structure

```
User Segment → Context → Behavior → Uncertainty/Barrier → Evidence → Potential Business Impact → Unmet Need → Opportunity
```

### Example Opportunity

| Field | Value |
|---|---|
| **Opportunity** | Improve fit confidence during product evaluation |
| **Segment** | Users considering women's dresses |
| **Context** | User likes a product but is uncertain about fit |
| **Behavior** | User reads multiple reviews and seeks external information |
| **Barrier** | Lack of confidence that the product will fit their body type |
| **Evidence** | Multiple independent conversations describing fit uncertainty |
| **Potential Business Impact** | May contribute to purchase postponement or abandonment |
| **Unmet Need** | Personalized fit confidence |
| **Potential Opportunity** | Help users understand expected fit using richer fit information, contextual reviews, or other product-experience mechanisms |

---

## 11. Opportunity Scoring

Create a configurable opportunity score across dimensions:

| Dimension | Description |
|---|---|
| Reach | How many users are affected |
| Frequency | How often the issue occurs |
| Severity | How significantly it impacts users |
| Business Impact | Potential effect on key metrics |
| Evidence Strength | Quality and reliability of supporting data |
| Cross-Source Consistency | Appears across multiple platforms |
| Cross-Segment Relevance | Affects multiple user segments |
| Trend | Growing, stable, or declining |
| Strategic Relevance | Alignment with business priorities |

> ⚠️ Do not assume frequency alone means importance. A low-frequency issue with extremely high purchase impact may deserve more attention than a high-frequency low-severity complaint.

Show underlying dimensions separately so PMs can understand **why** an opportunity ranks highly.

---

## 12. Quantification

Where evidence allows, quantify:

- Number of conversations / independent users
- Percentage of relevant feedback
- Number of sources
- Segment distribution / Category distribution
- Trend over time
- Frequency of barriers / uncertainty / external research
- Association with wishlist behavior / purchase postponement / abandonment

> ⚠️ **Never fabricate precision.** If a metric cannot be reliably calculated, label it as *unavailable* or *directional*.

---

## 13. Evidence Layer

Every important insight must be **traceable to supporting evidence**.

For every opportunity, show:

- Number of supporting conversations
- Number of independent sources
- Relevant source platforms
- Time period
- Supporting evidence
- Contradictory evidence
- Confidence level
- Whether the insight is observed, derived, or hypothesized

### Drill-Down Path

```
Opportunity → Pattern → Cluster → Individual Feedback → Original Source
```

> ⚠️ Do not generate fake user quotes. If presenting examples, clearly label them as paraphrases unless the original text is explicitly shown.

---

## 14. Natural Language Research Interface

Build a simple interface where the PM can ask questions in natural language:

> "Why do users wishlist dresses but not purchase them?"
> "What are the biggest barriers to buying ethnic wear?"
> "What makes users postpone fashion purchases?"
> "What information do users seek outside Myntra?"
> "How do first-time buyers differ from repeat buyers?"
> "Which problems are increasing over the last six months?"
> "What are the strongest unmet needs related to fit?"

The system should translate the question into appropriate filters and analysis steps.

---

## 15. Dashboard

Create a clean PM-oriented dashboard with the following sections:

| Section | Description |
|---|---|
| **A. Research Question** | Show the question being analyzed |
| **B. Executive Insight** | Concise evidence-backed answer |
| **C. Opportunity Areas** | Ranked opportunities with frequency, severity, business relevance, confidence, and trend |
| **D. User Journey** | Visualize where problems occur: Discovery → Consideration → Comparison → Wishlist → Purchase |
| **E. Segment Analysis** | Allow comparison across relevant segments |
| **F. Decision Factors** | Show major factors: Fit, Price, Reviews, Styling, Quality, Occasion, Social proof |
| **G. Evidence** | Supporting conversations and source distribution |
| **H. Contradictions** | Evidence that challenges the conclusion |

---

## 16. Segment Comparison

Allow PMs to compare opportunity patterns across:

- Categories
- Price bands
- User types (new vs returning)
- High vs low intent
- Wishlist-heavy vs non-wishlist users
- Product categories
- Occasions

> Example: "Compare purchase barriers for new vs repeat customers." — The system should show how barrier distribution changes between segments.

---

## 17. Trend Analysis

Support time-based analysis to identify:

- **Emerging** problems
- **Persistent** problems
- **Declining** problems
- **Seasonal** problems
- New user behaviors
- Changing decision criteria

> ⚠️ Avoid interpreting temporary spikes as long-term trends without sufficient evidence.

---

## 18. External Research Analysis

Identify conversations indicating users leave Myntra to obtain additional information.

Classify external research into categories:

- Fit, Quality, Styling, Product authenticity
- Reviews, Price comparison, Brand information
- Real-life appearance, Influencer validation, Occasion suitability

> **Key Question:** What information is missing from the Myntra shopping experience that users are currently obtaining elsewhere?

---

## 19. Technical Architecture

### Priorities

- Simplicity
- Explainability
- Evidence traceability
- Maintainability
- Extensibility
- Low infrastructure complexity

### Reasonable MVP Architecture

```
┌─────────────────────┐
│  Frontend Dashboard  │
├─────────────────────┤
│     Backend API      │
├─────────────────────┤
│  Relational Database │
├─────────────────────┤
│ AI/LLM Processing   │
│ Layer (Groq)         │
├─────────────────────┤
│   Analytics Layer    │
├─────────────────────┤
│ Optional: Embeddings │
│ / Vector Search      │
└─────────────────────┘
```

> Design so that RAG, MCP, additional data sources, and more advanced agentic capabilities can be added later without major restructuring.

---

## 20. MVP Scope

Build a **working MVP** rather than attempting to solve every possible problem.

The MVP should:

1. Load a representative sample dataset of fashion-shopping conversations
2. Process the feedback through the AI analysis pipeline
3. Store structured insights
4. Support natural-language research questions
5. Identify recurring barriers and unmet needs
6. Quantify them where possible
7. Generate ranked opportunity areas
8. Show supporting evidence
9. Allow basic segmentation
10. Provide a PM-friendly dashboard

> Use realistic synthetic/sample data if necessary. The application should be demonstrable end-to-end without requiring unavailable production data.

---

## 21. Evaluation Framework

Create a small evaluation framework to test whether the AI is producing useful results.

| Evaluation Area | Key Questions |
|---|---|
| **Classification Quality** | Is the system correctly identifying intent, journey stage, barrier, uncertainty, decision factor? |
| **Clustering Quality** | Are semantically similar problems grouped together? |
| **Evidence Quality** | Can every important conclusion be traced to evidence? |
| **Opportunity Quality** | Does the system distinguish meaningful opportunities from generic complaints? |
| **Hallucination Control** | Does the system avoid inventing user behavior, purchase outcomes, quotes, metrics, causal relationships? |

---

## 22. Important Product Principle

The system should **NOT** answer:

> "What are users saying?"

It **SHOULD** answer:

> **"What are users trying to accomplish, where are they struggling, why are they struggling, how widespread/severe is the problem, and what product opportunities could potentially address it?"**

### Output Hierarchy

```
Raw Feedback
    ↓
Behavior
    ↓
Intent / Uncertainty / Barrier
    ↓
Recurring Pattern
    ↓
Unmet Need
    ↓
Opportunity Hypothesis
    ↓
Potential Business Impact
    ↓
Evidence Required to Validate
```

---

## 23. Final Deliverable

Build the working MVP and provide:

1. Product architecture
2. Data model
3. AI analysis pipeline
4. Sample dataset
5. Backend
6. Frontend/dashboard
7. Opportunity scoring system
8. Natural-language research interface
9. Evidence-traceability mechanism
10. Evaluation framework
11. Setup instructions
12. Clear explanation of architectural decisions

> Before implementing, briefly inspect the requirements and identify any ambiguities or assumptions. Then proceed with the MVP.

> **Do not over-engineer the first version. Optimize for a working end-to-end product that demonstrates the core discovery loop:**
>
> **Question → Evidence → Analysis → Pattern → Opportunity → Business Relevance**
