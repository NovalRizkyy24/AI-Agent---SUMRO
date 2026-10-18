---
name: SUMROM
description: Modern minimalist notice for WhatsApp group members whose group is summarised by a bot.
colors:
  vermilion: "#d2361a"
  ink: "#0f1115"
  muted-gray: "#5b616b"
  cool-white: "#fbfbfc"
  panel-gray: "#f0f1f3"
  hairline: "#e2e4e8"
  vermilion-dark: "#ff6b4f"
  ink-dark: "#f2f3f5"
  muted-gray-dark: "#a1a7b0"
  near-black: "#0e0f11"
  panel-gray-dark: "#17191c"
  hairline-dark: "#272a2f"
typography:
  display:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(3rem, 11.5vw, 8.75rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.04em"
  display-close:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.75rem, 10vw, 7rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.875rem, 4.4vw, 3rem)"
    fontWeight: 750
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  headline-objection:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.75rem, 4.4vw, 2.75rem)"
    fontWeight: 750
    lineHeight: 1.08
    letterSpacing: "-0.03em"
  title-risk:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.375rem, 2.6vw, 1.625rem)"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.02em"
  title-fact:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.25rem, 2.2vw, 1.5rem)"
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  lede:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.1875rem, 2.2vw, 1.4375rem)"
    fontWeight: 400
    lineHeight: 1.45
  item:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 500
  body:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 700
  small:
    fontFamily: "Schibsted Grotesk Variable, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
  code:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "0.92em"
    fontWeight: 500
    letterSpacing: "-0.01em"
rounded:
  focus: "2px"
  panel: "20px"
  pill: "999px"
spacing:
  gutter: "clamp(20px, 5vw, 48px)"
  section: "clamp(64px, 9vw, 96px)"
  row-tight: "12px"
  row: "14px"
  column: "48px"
  panel-pad: "clamp(22px, 4vw, 44px)"
  panel-gap: "32px"
components:
  summary-panel:
    backgroundColor: "{colors.panel-gray}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "clamp(22px, 4vw, 44px)"
  summary-panel-dark:
    backgroundColor: "{colors.panel-gray-dark}"
    textColor: "{colors.ink-dark}"
    rounded: "{rounded.panel}"
  pill-sample:
    textColor: "{colors.muted-gray}"
    rounded: "{rounded.pill}"
    padding: "3px 12px"
  fact:
    textColor: "{colors.ink}"
    typography: "{typography.title-fact}"
  fact-alert:
    textColor: "{colors.vermilion}"
    typography: "{typography.title-fact}"
  command-row:
    textColor: "{colors.ink}"
    padding: "14px 0"
  objection:
    textColor: "{colors.vermilion}"
    typography: "{typography.headline-objection}"
  top-bar:
    textColor: "{colors.ink}"
    padding: "22px 0"
---

<!-- Replaces the retired split-flap departure-board world in full (2026-10-18). The split-flap tokens, cells, Antonio display face and amber/red status palette no longer apply to any surface. The quality-bar rasters in .impeccable/mocks/quality/ are retired references of that world: kept on disk for history, not a target for new work. -->

# Design System: SUMROM

## Overview

**Creative North Star: "The Plain Statement"**

A short, plain statement set in one confident grotesk, where size and space do all the work. The page reads like a notice someone wrote carefully: one very large sentence, a few facts, the evidence, the risks stated flatly. Hierarchy comes from scale jumps and heavy weights (800 display against 400 body), not from ornament, colour fields or containers.

The ground is a cool white in light mode and a near-black in dark mode, following `prefers-color-scheme`. Ink and one neutral gray carry all text. A single vermilion is the only colour on the page, and it is spent on objection and risk: the "Keberatan?" fact, the late task status, and the objection sentence. Density is low; sections are separated by generous vertical space, and the only filled surface is the soft gray panel that holds the sample summary.

This world rejects the bot-landing default of phone mockup, feature cards and green chat bubbles. The split-flap departure-board world that preceded it is retired.

**Key Characteristics:**
- One grotesk family for everything; mono only for typed commands.
- Display type at up to 8.75rem, weight 800, tight negative tracking.
- Ink, one gray, one vermilion. Nothing else carries colour.
- Whitespace separates groups; one soft gray panel; hairline rules only between list rows.
- Light and dark token sets with identical roles.
- One motion moment: the headline wipes in once on load.

## Colors

A cool, nearly achromatic neutral pair with one hot vermilion held in reserve.

### Primary
- **Objection Vermilion** (light `vermilion`, dark `vermilion-dark`): the only chromatic colour. Used for the objection fact, the "Lewat tenggat" task status, the objection sentence, the focus ring, and text selection. It marks what the reader can refuse or should worry about, never decoration or navigation.

### Neutral
- **Ink** (light `ink`, dark `ink-dark`): headlines, body, facts, list items, commands.
- **Muted Gray** (light `muted-gray`, dark `muted-gray-dark`): lede, notes, secondary lines, metadata, the "Tidak dicatat" list, done status, footer, the pill outline.
- **Cool White / Near-Black** (light `cool-white`, dark `near-black`): page ground; also the `theme-color` meta for each scheme.
- **Panel Gray** (light `panel-gray`, dark `panel-gray-dark`): the single filled surface, reserved for the sample summary.
- **Hairline** (light `hairline`, dark `hairline-dark`): 1px row separators in lists and command tables.

### Named Rules
**The One Hot Colour Rule.** Vermilion appears only where the reader's objection or a risk is at stake. If an element is not about refusing, lateness or risk, it is ink or gray.

**The Paired Scheme Rule.** Every colour role exists in both schemes; dark values are swapped on `:root` under `prefers-color-scheme: dark` (skipped when `data-theme='light'`). Never introduce a light-only colour.

## Typography

**Display Font:** Schibsted Grotesk Variable (with Helvetica Neue, Arial, sans-serif)
**Body Font:** Schibsted Grotesk Variable (same stack)
**Label/Mono Font:** JetBrains Mono 500 (with ui-monospace, monospace), for commands only

**Character:** A single sturdy grotesk spans 400 to 800 and does all the hierarchy work through size and weight; the mono appears only where the reader must type something exactly.

### Hierarchy
- **Display** (800, clamp(3rem, 11.5vw, 8.75rem), 0.94, -0.04em, balanced wrap): the opening headline, one span per line. The closing line reuses it at clamp(2.75rem, 10vw, 7rem).
- **Headline** (750, clamp(1.875rem, 4.4vw, 3rem), 1.05, -0.03em): section titles. The objection sentence uses the same weight at clamp(1.75rem, 4.4vw, 2.75rem) in vermilion.
- **Title** (700, clamp(1.375rem, 2.6vw, 1.625rem), 1.3, -0.02em): risk statements. Fact text sits a step lighter (500, clamp(1.25rem, 2.2vw, 1.5rem)); recorded-item names at 600, 1.1875rem.
- **Lede** (400, clamp(1.1875rem, 2.2vw, 1.4375rem), 1.45, muted, max 52ch): the one-line explanation under the headline and the closing line.
- **Body** (400, 1.0625rem, 1.6): notes and descriptions, muted, max 46ch for section notes.
- **Item** (500, 1.125rem): rows inside the sample summary.
- **Label** (700, 0.9375rem): sub-group headings ("Keputusan", "Semua anggota") and fact labels; sentence case, no tracking, no uppercase.
- **Small** (400, 0.875rem): footer.
- **Code** (JetBrains Mono 500, 0.92em, -0.01em): every slash command, inline and in the command table (1.0625rem there).

### Named Rules
**The One Family Rule.** Schibsted Grotesk sets every non-command word. Do not add a second display or serif face.

**The Typed-Only Mono Rule.** Mono marks literal text the reader types into the group (`/ringkas`, `/nonaktifkan`). It is not a decorative label style.

## Layout

Single centred column, max-width 1120px, inline padding `gutter` (clamp(20px, 5vw, 48px)). Mobile-first; one breakpoint at 860px.

Sections are padded vertically by `section` (clamp(64px, 9vw, 96px)). Above 860px a section becomes a 4fr / 8fr two-column grid with 48px column gap: title and note on the left, content on the right. A full-width variant (risks) drops to one column so the risk list spans the page in two 1fr columns. The three facts stack with 28px gaps on mobile and become three equal columns with 40px gaps on desktop. Recorded / not-recorded lists split 1fr 1fr at 48px. Command rows become an 11rem / 1fr grid.

Row rhythm inside lists is 12 to 14px block padding; sub-groups are 12px below their label; section internal gaps are clamp(28px, 4vw, 40px).

## Elevation & Depth

Flat. No shadows anywhere. Depth is expressed only by the one tonal step from ground to panel gray, and by type scale.

### Named Rules
**The Flat Page Rule.** No box-shadow, no blur, no layered cards. If something needs separating, use space first, a hairline second, the panel tone only for the sample.

## Shapes

Mostly square and open: text sits directly on the ground. Three radii exist: the sample panel's gently rounded corners (`panel`), the fully rounded "Contoh" pill (`pill`), and a 2px softening on the focus outline. Borders appear only as 1px hairline row separators in lists and command tables, and as the pill's 1px muted outline.

## Components

### Top Bar
Plain text row, space-between, baseline aligned, 22px block padding, 0.9375rem. Left: "SUMROM" wordmark at weight 800, +0.02em. Right: bot number in muted gray. No nav links, no buttons.

### Fact
Label (0.9375rem / 700) over a fact sentence (title-fact, 500). The alert variant turns both label and sentence vermilion; commands inside stay mono.

### Sample Summary Panel (signature)
- **Corner Style:** gently rounded (`panel`, 20px)
- **Background:** panel gray (light/dark pair)
- **Shadow Strategy:** none (see Elevation)
- **Border:** none; inner lists use hairline rows
- **Internal Padding:** clamp(22px, 4vw, 44px), 32px gap between groups
- Header row: title (1.25rem / 700) and muted meta, with the "Contoh" pill right-aligned. Task rows are a two-column grid: what + muted who/when on the left, status on the right (600; late = vermilion; done = muted 500).

### Chips
- **Style:** "Contoh" pill only: transparent fill, 1px muted outline, muted text, 0.8125rem / 600, +0.02em, 3px 12px padding, fully rounded.
- **State:** static label; no interactive chips exist.

### Command Table
Definition list of rows, each with a hairline top border and 14px block padding. Command in mono (1.0625rem, ink), description in muted gray. Stacked on mobile; 11rem / 1fr columns at 860px+.

### Risk List and Objection
Risks are bold title-weight statements with a muted explanation, two columns on desktop. The objection follows: one vermilion headline-scale sentence, then a muted 46ch line naming `/nonaktifkan`.

### Focus
2px solid vermilion outline, 4px offset, 2px radius, on every focusable element.

### Motion
One moment only: on load, each headline line is revealed by a clip-path wipe (0.9s, `cubic-bezier(.16, 1, .3, 1)`, second line delayed 0.1s), and the lede rises 10px and fades in after 0.25s. Gated behind `prefers-reduced-motion: no-preference`; reduced motion shows everything at rest.

## Do's and Don'ts

### Do:
- **Do** let size and weight carry hierarchy: display 800 against body 400.
- **Do** keep vermilion for objection, lateness and risk only.
- **Do** separate groups with section spacing (clamp(64px, 9vw, 96px)) before reaching for a line or a surface.
- **Do** set every typed command in JetBrains Mono 500.
- **Do** define every new colour role in both light and dark token sets.
- **Do** keep the headline wipe as the only entrance motion, and honour reduced motion.

### Don't:
- **Don't** use shadows, gradients or a second accent colour.
- **Don't** wrap content in cards; the gray panel is reserved for sample output.
- **Don't** use mono as a decorative label style or uppercase-tracked eyebrows above headings.
- **Don't** reintroduce split-flap cells, Antonio, the amber/red board palette, or the retired quality-bar rasters as references.
- **Don't** use phone mockups, chat bubbles or rows of icon cards.
