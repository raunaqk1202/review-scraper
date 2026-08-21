---
name: Fashion Intelligence System
colors:
  surface: '#0e1224'
  surface-dim: '#0e1224'
  surface-bright: '#34384c'
  surface-container-lowest: '#090d1f'
  surface-container-low: '#161b2d'
  surface-container: '#1b1f31'
  surface-container-high: '#25293c'
  surface-container-highest: '#303447'
  on-surface: '#dee1fa'
  on-surface-variant: '#e3bdc0'
  inverse-surface: '#dee1fa'
  inverse-on-surface: '#2b2f43'
  outline: '#ab888b'
  outline-variant: '#5b4042'
  surface-tint: '#ffb2ba'
  primary: '#ffb2ba'
  on-primary: '#670021'
  primary-container: '#ff4f74'
  on-primary-container: '#5a001c'
  inverse-primary: '#bd0043'
  secondary: '#ffb866'
  on-secondary: '#482900'
  secondary-container: '#e38d00'
  on-secondary-container: '#513000'
  tertiary: '#f9abff'
  on-tertiary: '#570066'
  tertiary-container: '#d560e6'
  on-tertiary-container: '#4c0059'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffd9dc'
  primary-fixed-dim: '#ffb2ba'
  on-primary-fixed: '#400011'
  on-primary-fixed-variant: '#910031'
  secondary-fixed: '#ffddba'
  secondary-fixed-dim: '#ffb866'
  on-secondary-fixed: '#2b1700'
  on-secondary-fixed-variant: '#673d00'
  tertiary-fixed: '#ffd6fe'
  tertiary-fixed-dim: '#f9abff'
  on-tertiary-fixed: '#35003f'
  on-tertiary-fixed-variant: '#7b008f'
  background: '#0e1224'
  on-background: '#dee1fa'
  surface-variant: '#303447'
  surface-dark: '#0F111A'
  surface-card: rgba(40, 44, 63, 0.6)
  glass-stroke: rgba(255, 255, 255, 0.12)
  text-muted: '#A9ABB2'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-margin: 32px
  gutter: 24px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

This design system targets fashion analysts, trend-spotters, and retail executives. The brand personality is **Visionary, Analytical, and Chic**. It bridges the gap between high-fashion editorial aesthetics and high-velocity data intelligence.

The visual direction is **Refined Glassmorphism**. It utilizes deep, saturated dark backgrounds with translucent "frosted" surfaces that suggest depth and digital sophistication. The style avoids the heaviness of traditional enterprise dashboards, opting instead for a lightweight, luminous aesthetic that feels energetic and forward-looking. High-contrast typography and vibrant accents evoke the high-energy world of retail while maintaining the precision of a professional intelligence engine.

## Colors

The palette is anchored by a deep obsidian background (`#0F111A`) to allow Myntra’s signature vibrant tones to pop. 

- **Primary (Vibrant Pink):** Used for primary actions, key data highlights, and brand presence.
- **Secondary (Sunset Orange):** Used for warnings, trend-up indicators, and secondary focus areas.
- **Tertiary (Digital Purple):** Used for creative insights, AI-driven suggestions, and depth gradients.
- **Neutral:** A range of cool-toned grays derived from the core Myntra navy to maintain professional sobriety.

Color is applied with restraint to maintain an editorial feel; use gradients sparingly, primarily within glass surfaces or as subtle glows behind high-priority data points.

## Typography

The system uses **Plus Jakarta Sans** for its modern, geometric construction and open apertures, which ensure readability even on dense data screens. 

- **Display & Headlines:** Use heavy weights (Bold/700) with slight negative letter-spacing to create a "fashion-forward" editorial impact.
- **Body Text:** Standard weight (Regular/400) for clarity. Ensure ample line height (1.5x) to prevent eye fatigue during long sessions.
- **Labels:** Use Medium (500) or SemiBold (600) with increased letter-spacing for UI controls and metadata to distinguish them clearly from content.

## Layout & Spacing

The design system employs a **12-column fluid grid** for desktop, scaling down to a **4-column grid** for mobile. 

- **Layout Philosophy:** Use generous white space (or "dark space") to separate high-level metrics from detailed lists. 
- **Margins:** Desktop margins are fixed at 32px to provide a spacious, premium feel. 
- **Rhythm:** An 8px base grid governs all spatial decisions. Internal card padding should be 24px (`stack-md`) to allow data visualizations to breathe.
- **Breakpoints:**
  - Desktop: 1200px+
  - Tablet: 768px - 1199px (utilize 8 columns)
  - Mobile: <767px (utilize 4 columns, vertical stacking)

## Elevation & Depth

Depth is created through **Luminous Stacking** rather than traditional shadows:

1.  **Level 0 (Base):** Deep `#0F111A` background.
2.  **Level 1 (Cards/Containers):** Glassmorphic surfaces with `backdrop-filter: blur(20px)` and a 1px border (`glass-stroke`).
3.  **Level 2 (Modals/Popovers):** Higher opacity glass with a subtle outer glow using a 10% opacity primary color tint.
4.  **Indicators:** Active states utilize "inner-glow" effects or vibrant 2px left-side accents to denote selection.

Avoid heavy black drop shadows; instead, use color-tinted ambient blurs to suggest light passing through glass.

## Shapes

The shape language is **Fluid and Consumer-Tech friendly**. 

- **Standard Containers:** Use a 16px (`rounded-xl`) corner radius to create a soft, approachable tech feel.
- **Buttons & Inputs:** Use an 8px (`rounded-md`) radius for a slightly sharper, more functional appearance.
- **Interactive Tags/Chips:** Full-pill (`rounded-full`) for a modern, energetic look.

Consistency in roundedness is key; never mix sharp 0px corners with these rounded elements.

## Components

- **Buttons:** 
  - *Primary:* Solid Primary Pink with white text. 
  - *Secondary:* Ghost style with `glass-stroke` and white text. 
  - *Interaction:* Subtle scale-down effect (0.98) on click.
- **Cards:** Must feature the glassmorphic blur and 1px stroke. Headlines within cards should be `headline-md`.
- **Inputs:** Dark background (`#282C3F`) with a `glass-stroke`. On focus, the border transitions to a Primary Pink gradient.
- **Trend Chips:** Small pill-shaped badges. Use green for "Up," red for "Down," and Purple for "Insight."
- **Data Visualizations:** Use a custom-themed palette: Primary Pink, Secondary Orange, and Tertiary Purple. Line charts should use "soft" bezier curves rather than jagged angles to match the rounded UI language.
- **Navigation:** Vertical sidebar with high-transparency glass. Active links use a subtle background tint and a Primary Pink vertical indicator.