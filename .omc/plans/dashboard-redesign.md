# Dashboard Visual Redesign Plan

**Date**: 2026-04-08
**Scope**: Visual-only redesign of `agents/dashboard/` -- no feature/API changes
**Goal**: Transform "AI control center" aesthetic into a clean, minimal tool feel (Linear/Notion style)

---

## Context

The current dashboard was recently migrated from dark to light theme, but retains aggressive styling:
- Uppercase badge labels everywhere ("SINGLE PIPELINE", "ALL PASS", "TOTAL")
- HUD-style 3-column card grid with nested card-in-card structure
- Saturated primary colors (red/green/yellow) in charts and badges
- Dark terminal log boxes (#1e293b) clashing with light theme
- Donut chart with candy-palette colors (#f472b6, #fb923c)
- "QA CONTROL CENTER" title
- Dense sidebar with inline textarea

## Design Principles

1. **Quiet confidence** -- Data speaks through layout and whitespace, not color saturation or bold type. Use muted, desaturated tones.
2. **Sentence case everywhere** -- Remove all `text-transform: uppercase` and `.toUpperCase()`. Labels read like prose, not alarms.
3. **Single surface tone** -- Log boxes, cards, and panels share the same light surface. No dark terminal islands.
4. **Restrained color** -- Green/red/yellow only for semantic status dots (tiny, not badges). Charts use a monochrome + 1 accent palette.
5. **Flat hierarchy** -- Reduce card nesting. Section titles are lightweight text dividers, not boxed headers.

## Decision Drivers

1. **User feedback**: "too dark and AI-feeling" -- top priority is removing the control-center aesthetic
2. **Minimal diff risk**: CSS-only changes where possible; JS changes only where inline styles or color maps are hardcoded
3. **Consistency**: Every component must follow the same muted palette -- no outlier dark/bright zones

---

## RALPLAN-DR: Options Considered

### Option A: CSS-first refactor (CHOSEN)
Rewrite variables.css palette, remove uppercase transforms, restyle log boxes via CSS. Touch JS only for hardcoded inline styles and color maps.

**Pros**: Smallest blast radius, easy to verify (visual diff only), no class rename risk
**Cons**: Some inline styles in JS still need manual changes (~30 lines across 6 files)

### Option B: Full class rename + BEM migration
Rename all classes to a BEM system, extract all inline styles from JS into CSS classes.

**Pros**: Cleaner long-term architecture
**Cons**: High risk of JS/CSS desync, massive diff, overkill for a visual-only redesign

**Option B invalidated**: Task constraint is "visual redesign only, no feature changes." A BEM migration is an architecture change that risks breaking JS innerHTML references across 12 files.

---

## Guardrails

### Must Have
- All existing features work identically after changes
- Responsive layout preserved (no breakpoint changes)
- Accessibility preserved (focus-visible outlines, reduced-motion)
- Every `text-transform: uppercase` removed or replaced with `none`
- Dark log boxes (#1e293b) replaced with light-theme-consistent style

### Must NOT Have
- New CSS class names (reuse existing classes, change their styles)
- API endpoint changes
- New dependencies or font additions
- Feature additions or removals

---

## Task Flow

### Step 1: Palette and typography reset (variables.css + layout.css)
**Files**: `variables.css`, `layout.css`

Changes:
- Replace saturated semantic colors with muted variants:
  - `--approved-color`: #16a34a -> #22863a (softer green)
  - `--revision-color`: #dc2626 -> #cb2431 (less alarming red)
  - `--pending-color`: #d97706 -> #b08800 (muted amber)
  - Background tints: reduce opacity/saturation of `--approved-bg`, `--revision-bg`, `--pending-bg`
- `--accent`: #2563eb -> #5469d4 (softer blue, Stripe-like)
- `--radius`: 10px -> 8px, `--radius-lg`: 14px -> 10px (less rounded = more tool-like)
- `.header-title`: remove Outfit font-weight 700, set 600; change text from JS
- `.sidebar-label`: remove `text-transform: uppercase`, set `font-weight: 600`, `letter-spacing: 0`
- `.live-indicator`: remove `text-transform: uppercase`, reduce `letter-spacing`

**Acceptance criteria**:
- No uppercase text visible in header or sidebar labels
- Color palette is visibly muted compared to current
- All borders and surfaces remain distinct and readable

### Step 2: Component de-emphasis (components.css + overview.css)
**Files**: `components.css`, `views/overview.css`

Changes:
- `.status-badge`: remove `text-transform: uppercase`, reduce `font-weight` to 600, increase `font-size` to 11px, soften border radius
- `.ov-card-label`, `.ov-stat-label`, `.hud-label`: remove `text-transform: uppercase`, set sentence case styling
- `.ov-stat-num`: reduce `font-size` from 30px to 24px, `font-weight` from 800 to 700
- `.hud-value`: reduce from 28px/800 to 22px/700
- `.ov-card-value`: reduce from 26px/800 to 22px/700
- `.ov-card`: remove hover `translateY(-2px)` lift effect (keep subtle border change only)
- `.hud-card`: same -- remove lift, keep border highlight
- Log boxes (`.run-log-box`, `.ov-log-box`): replace `#1e293b` background with `var(--surface2)`, border with `var(--border)`, text color with `var(--text)` (dark text on light bg)
- `.hs-donut-center`: reduce font-size from 18px to 15px

**Acceptance criteria**:
- No uppercase labels in overview cards or stat grids
- Log boxes are light-themed, visually consistent with surrounding panels
- Card hover effects are subtle (no vertical movement)
- Numbers are present but not "screaming"

### Step 3: Chart and color map cleanup (overview.js + parallel.css)
**Files**: `views/overview.js`, `views/parallel.css`, `components/group-result.js`

Changes in overview.js:
- Replace `typeColors` map with muted monochrome palette:
  - Use shades of slate/blue-gray: #64748b, #94a3b8, #5469d4, #7c8db5, #a0aec0, #718096, #4a5568, #2d3748
- Remove `linear-gradient(135deg,#a78bfa 0%,#6366f1 100%)` from welcome button -- use flat `var(--accent)`
- Trend chart bar colors: use single accent color at varying opacity instead of red/yellow/green
- `'ALL PASS'` string -> `'All pass'`; `'FAILED'` -> `'Failed'`
- Inline `style="color:var(--approved-color)"` etc. -- keep these (they reference CSS vars which are now muted)
- `.ov-stat-label` inline content: "Total", "Passed", "Failed", "Pass Rate" -- already sentence case, no change needed

Changes in group-result.js:
- Line 28: `.toUpperCase()` -> remove, use original group name with first-letter capitalized

Changes in parallel.css:
- Remove all 4 `text-transform: uppercase` instances

**Acceptance criteria**:
- Donut chart uses muted monochrome palette, no candy colors
- Trend bars are single-hue at varying opacity
- No `.toUpperCase()` calls in JS for display labels
- No `text-transform: uppercase` in parallel.css

### Step 4: Header and sidebar refinement (index.html + team.css)
**Files**: `index.html`, `views/team.css`

Changes in index.html:
- Line 7: `<title>` change from "QA 컨트롤 센터" to "QA Dashboard"
- Line 34: "QA CONTROL CENTER" -> "QA Dashboard"
- Lines 75, 90: Remove inline `text-transform:uppercase` from sidebar inline styles
- Consider: move "새 토론 주제" textarea out of sidebar into team view (reduces sidebar density). If too risky, just keep and restyle.

Changes in team.css:
- Dark log box (lines 158-164): replace with light theme (same as Step 2)

**Acceptance criteria**:
- Page title and header say "QA Dashboard" (not control center, not uppercase)
- No inline `text-transform: uppercase` in HTML
- Team view log box is light-themed

### Step 5: Remaining JS inline styles audit (pipeline.js, parallel.js, quick-run.js, utils.js, import.js)
**Files**: All JS files with inline style counts > 0

Changes:
- Search all JS files for hardcoded hex colors (#xxxxxx) and replace with CSS variable references where possible
- Any remaining `background: #eff6ff` or `border-color: #bfdbfe` patterns -> use `var(--senior-bg)` / `var(--senior-border)` etc.
- `utils.js` modal styles: verify already light-themed (noted as done), confirm no dark remnants

**Acceptance criteria**:
- No hardcoded hex colors in JS that could be replaced by CSS variables
- All modal/popup styles are consistent with light theme
- Visual regression check: open each view and confirm no dark islands or saturated outliers

---

## Success Criteria

1. Zero `text-transform: uppercase` in entire codebase (CSS + inline HTML)
2. Zero `.toUpperCase()` used for display labels in JS
3. Zero dark-background (#1e293b) log boxes
4. Header reads "QA Dashboard" in sentence case
5. All charts use muted, monochrome-adjacent palette
6. Every existing feature (sidebar nav, pipeline views, team discussion, reports, quick run, import) works without regression
7. Focus-visible and reduced-motion accessibility preserved

---

## Open Questions

See `.omc/plans/open-questions.md`

---

## ADR: Dashboard Visual Redesign

- **Decision**: CSS-first palette/typography refactor with targeted JS inline style cleanup
- **Drivers**: User feedback ("too AI-feeling"), minimal regression risk, visual-only scope constraint
- **Alternatives considered**: Full BEM class rename migration -- invalidated because it exceeds visual-only scope and risks JS/CSS desync across 12 files with innerHTML
- **Why chosen**: Smallest diff that achieves all design goals; CSS variable changes propagate automatically to most components
- **Consequences**: Some inline styles in JS will still reference CSS variables (acceptable); future refactoring could extract these to classes
- **Follow-ups**: Consider extracting team discussion textarea from sidebar into team view in a separate task
