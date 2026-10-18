---
name: SUMROM
description: Papan keberangkatan split-flap untuk grup WhatsApp yang dirangkum bot.
colors:
  status-amber: "#ffb400"
  status-red: "#ff5a4a"
  steel-frame: "#8e949c"
  steel: "#b6bbc2"
  steel-dark: "#6f757e"
  ground: "#1a1c1f"
  board: "#111214"
  flap-top: "#1a1a1a"
  flap-bottom: "#0e0e0e"
  seam: "#000000"
  rule-line: "#2c2f33"
  type: "#f2f2f2"
  type-soft: "#c4c8cd"
typography:
  display-cells-xl:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "calc(var(--cw) * 1.08); --cw clamp(28px, (100vw - 92px) / 9.6, 68px) mobile, clamp(40px, (min(100vw,1120px) - 160px) / 13.8, 72px) desktop"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "normal"
  display-cells-lg:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "calc(var(--cw) * 1.08); --cw clamp(24px, (100vw - 92px) / 13, 52px) mobile, clamp(36px, (min(100vw,1120px) - 160px) / 16, 60px) desktop"
    fontWeight: 700
    lineHeight: 1
  headline-cells-md:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "calc(var(--cw) * 1.08); --cw clamp(22px, (100vw - 92px) / 12, 36px) mobile, clamp(26px, (min(100vw,1120px) - 160px) / 26, 36px) desktop"
    fontWeight: 700
    lineHeight: 1
  title-row:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.08em"
  title-flap:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "0.1em"
  body:
    fontFamily: "Barlow Semi Condensed, Arial Narrow, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.45
    fontFeature: "tnum"
  body-detail:
    fontFamily: "Barlow Semi Condensed, Arial Narrow, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.35
  label-column:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "0.16em"
  label-tag:
    fontFamily: "Antonio, Arial Narrow, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    letterSpacing: "0.14em"
rounded:
  none: "0px"
  flap: "2px"
  cell: "3px"
spacing:
  cell-gap: "3px"
  row-gap: "4px"
  frame: "6px"
  cell-pad: "10px"
  board-gap: "18px"
  board-pad: "clamp(12px, 3vw, 28px)"
  page-gap: "clamp(20px, 4vw, 40px)"
  page-max: "1120px"
components:
  frame:
    backgroundColor: "{colors.steel-frame}"
    padding: "{spacing.frame}"
    rounded: "{rounded.none}"
  board-panel:
    backgroundColor: "{colors.board}"
    textColor: "{colors.type}"
    padding: "{spacing.board-pad}"
    rounded: "{rounded.none}"
  flap-cell:
    backgroundColor: "{colors.flap-top}"
    textColor: "{colors.type}"
    typography: "{typography.display-cells-lg}"
    rounded: "{rounded.cell}"
    width: "var(--cw)"
    height: "calc(var(--cw) * 1.4)"
  flap-strip:
    backgroundColor: "{colors.flap-top}"
    textColor: "{colors.type}"
    typography: "{typography.title-flap}"
    rounded: "{rounded.flap}"
    padding: "4px 10px"
    height: "34px"
  flap-strip-amber:
    backgroundColor: "{colors.flap-top}"
    textColor: "{colors.status-amber}"
  flap-strip-red:
    backgroundColor: "{colors.flap-top}"
    textColor: "{colors.status-red}"
  flap-strip-dim:
    backgroundColor: "{colors.flap-top}"
    textColor: "{colors.type-soft}"
  board-row-cell:
    backgroundColor: "{colors.flap-top}"
    textColor: "{colors.type}"
    typography: "{typography.title-row}"
    rounded: "{rounded.none}"
    padding: "9px 10px"
  column-header:
    textColor: "{colors.status-amber}"
    typography: "{typography.label-column}"
    padding: "0 10px 4px"
  tag-sample:
    textColor: "{colors.status-amber}"
    typography: "{typography.label-tag}"
    rounded: "{rounded.none}"
    padding: "2px 8px"
---

# Design System: SUMROM

## Overview

**Creative North Star: "The Concourse Board"**

The system is a split-flap departure board, mounted for one WhatsApp group. Every surface is a steel-framed board; every rule, sample task, stored datum, and command is a ruled row with a fixed status column; every display word is set letter by letter in flap cells. The board refuses the category default of headline, phone mockup, and feature cards: rows and columns are the whole composition.

Density is high and legible, the way a concourse board is: condensed caps, tabular numerals, tight row spacing (4px), and a status column that holds one fixed width per table so the lamps line up. The palette is mechanical (matte flap-black, brushed steel, painted white) with two lamp colors. Depth comes from the hardware itself: the flap's two-tone halves, the hinge seam, the steel frame showing through the gaps between panels.

Motion is the board's own: one load-time cascade where the headline cells flip through random glyphs and settle, then the status flaps resolve row by row. Reduced motion shows the final board instantly.

**Key Characteristics:**
- One continuous steel frame; panels separated by 6px of exposed steel, never by cards or shadows between panels.
- Two-tone flap black (top #1a1a1a / bottom #0e0e0e) with a black center seam on every cell, strip, row, and day tile.
- Display words only in per-letter flap cells (xl / lg / md).
- Amber and red are lamps, not decoration.
- Square, unrounded geometry except the flap hardware (2–3px).

## Colors

A dark mechanical palette: flap-black and brushed steel carrying painted white type, with two lamp colors.

### Primary
- **Concourse Amber** (status-amber): the "needs attention" lamp. Status flaps with an inset 1px amber outline (Ya, Belum ditetapkan), amber row keys for risks, and the board's painted column headers and group labels (the yellow header paint of a real departure board). Also the interaction signal: focus ring, link underline, text selection, and commands quoted inside prose.

### Secondary
- **Signal Red** (status-red): late, stopped, or objection, and nothing else. Red row keys and red-outlined status flaps (Lewat, Admin /nonaktifkan, Keberatan), and the HAPUS tile of the retention strip.

### Neutral
- **Frame Steel** (steel-frame): the single continuous frame and the 6px dividers between panels.
- **Brushed Steel / Dark Steel** (steel, steel-dark): reserved steel tones; dark steel colors the scrollbar thumb.
- **Concourse Ground** (ground): page background behind the frame, with a near-invisible 1px vertical brush stripe every 3px.
- **Board Black** (board): panel fill; also the 3px separators between cells in a row.
- **Flap Top / Flap Bottom** (flap-top, flap-bottom): the two halves of every flap surface, hard-split at 50%.
- **Hinge Seam** (seam): the 1–2px black line across the middle of each flap.
- **Rule Line** (rule-line): the 1px rule under a panel's head bar.
- **Painted White** (type): primary text and cell glyphs.
- **Soft White** (type-soft): notes, row detail lines, dim statuses (Selesai, Tidak disimpan), meta labels, footer.

### Named Rules
**The Lamp Rule.** Red marks only late, stopped, deleted, or objection. Amber marks only what needs the reader's attention, plus the board's header paint and interaction states. Neither ever fills a panel or a background.

**The No Third Lamp Rule.** There is no green, blue, or brand accent. A state that is fine is painted white; a state that is finished or absent is soft white.

## Typography

**Display Font:** Antonio (with Arial Narrow, sans-serif), weights 500/600/700, self-hosted
**Body Font:** Barlow Semi Condensed (with Arial Narrow, sans-serif), weights 400/500, self-hosted

**Character:** Antonio is the painted flap lettering: tall, condensed, uppercase, tracked. Barlow Semi Condensed carries readable sentences at the same narrow width, so prose sits on the board without breaking its rhythm. Tabular numerals are on page-wide.

### Hierarchy
- **Display, cells xl** (700, cell width up to 72px, glyph = 1.08 × cell width, line-height 1): the opening headline and the closing line, one letter per cell.
- **Display, cells lg** (700, cell width up to 60px): available step between xl and md.
- **Headline, cells md** (700, cell width up to 36px): every panel heading.
- **Title, row key** (600, 1.0625rem, 0.08em, uppercase, line-height 1.2): the left column of every board row; scales to clamp(1.0625rem, 2.6vw, 1.375rem) in the opening rules table.
- **Title, flap strip** (600, 1.0625rem, 0.1em, uppercase): status values and the identity strips.
- **Board title / meta** (700 clamp(1.25rem, 3.4vw, 2rem) 0.08em; 500 0.9375rem 0.12em soft white): head-bar text when a heading is not in cells.
- **Body** (400, 1.0625rem, line-height 1.45, max 62ch): notes under a board, white-on-black.
- **Body detail** (400, 1rem, line-height 1.35, soft white): the sentence line under a row key.
- **Label, column header** (500, 0.8125rem, 0.16em, uppercase, amber): table column headers and group labels (0.875rem).
- **Code** (Antonio 600, 0.04em): slash commands, white in tables, amber inside prose.

### Named Rules
**The Cell Rule.** Every display word is set in per-letter flap cells, uppercase, with real text exposed to screen readers. No display headline is ever set as free type.

**The Condensed Pair Rule.** Antonio for anything painted on the board, Barlow Semi Condensed for anything a person reads as a sentence. No third family.

## Layout

A single column, max 1120px, centered, padding 12px (32px from 900px). Inside it, one steel frame holds every panel as a grid with 6px gaps; the page grid gap between frame and footer is clamp(20px, 4vw, 40px). Each panel pads clamp(12px, 3vw, 28px) and stacks its parts at 18px.

Content is tables of board rows: rows spaced 4px apart (border-spacing), cells padded 9px 10px and separated by 3px of board black. The status column is right-aligned and holds one fixed width per table set through a custom property (8.5em for rules, 8em for retention, 5.5em for tasks), so status flaps align and wrap inside that width.

Cell sizes are computed from viewport width so the xl headline breaks into whole words across lines on a phone and fewer lines on desktop. At 900px and up, paired panels (stored data and commands) sit side by side in a 1fr 1fr split with a 6px steel gap; below 900px, secondary columns (Siapa) fold into a detail line under the row key.

## Elevation & Depth

Flat inside, one lift outside. The frame alone carries a single soft drop (0 18px 40px -18px at 80% black) that lifts the whole board off the ground. Inside the frame, depth is mechanical, not shadowed: the two-tone flap halves, a 2px inset shadow at each cell's foot, a 1px highlight beneath, and the hinge seam.

### Shadow Vocabulary
- **Board lift** (`box-shadow: 0 18px 40px -18px rgb(0 0 0 / .8)`): the frame only.
- **Cell foot** (`box-shadow: inset 0 -2px 0 rgb(0 0 0 / .6), 0 1px 0 rgb(255 255 255 / .04)`): per-letter cells.
- **Lamp outline** (`box-shadow: inset 0 0 0 1px <lamp color>`): amber and red status flaps, the HAPUS tile.

### Named Rules
**The One Frame Rule.** There is one frame. Panels never get their own shadow, border, or radius; they are separated only by exposed steel.

## Shapes

Square by default: frame, panels, rows, tags, and day tiles have no radius. Only flap hardware rounds, and barely: cells 3px, flap strips 2px. Every flap surface is split horizontally at 50% into a lighter top and darker bottom with a seam line across the middle. Cells are fixed-aspect (height 1.4 × width).

## Components

### Flap Cell (signature)
- **Shape:** fixed cell, width from the size step, height 1.4×, 3px radius, glyph centered at 1.08× width.
- **Color:** flap-top/flap-bottom halves, painted white glyph, 2px black seam.
- **Grouping:** 3px between letters, 0.45 cell width between words, 6px between wrapped lines.
- **Motion:** in the load cascade each cell flips 3–6 random glyphs before settling (90ms scaleY flip, cubic-bezier(.2,.7,.2,1), 40ms stagger per cell). Only the opening headline cascades. Reduced motion: no animation.

### Flap Strip (status and identity)
- **Shape:** inline strip, min-height 34px, padding 4px 10px, 2px radius, 1px seam.
- **Tones:** white (default), amber and red with an inset 1px outline of the lamp color, dim in soft white.
- **In the status column:** centered and stretched to the table's fixed status width. Opening-board statuses resolve left to right after the headline settles.

### Board Row
- **Style:** two-tone flap cells, 9px 10px padding, 3px board-black separators, 4px between rows; key in Antonio 600 caps, optional soft-white Barlow detail line below.
- **States:** amber row key for attention items, red row key for late/objection; the status column has no flap fill of its own, only its strip.

### Column Header
- **Style:** amber Antonio 500, 0.8125rem, 0.16em tracked caps, left-aligned (right-aligned over status).

### Panel Head Bar
- **Style:** heading in md cells on the left, a sample tag or soft-white meta on the right, baseline-aligned, 1px rule-line below with 10px padding.

### Sample Tag
- **Style:** square outlined box (1px currentColor), amber Antonio 600 caps 0.875rem, 2px 8px. Sits in the head bar beside a heading to mark invented example content (CONTOH).

### Retention Strip
- **Style:** grid of day tiles (min-height 44px, flap two-tone, Antonio 600), 3px gaps; the terminal tile spans two columns in red with a red inset outline.

### Links and Focus
- **Links:** white text, 2px amber underline at 0.2em offset; hover turns the text amber.
- **Focus:** 2px solid amber outline, 3px offset.

## Do's and Don'ts

### Do:
- **Do** put every new section on the same steel frame as another panel, separated by the 6px steel gap.
- **Do** express content as board rows with a fixed-width, right-aligned status column per table.
- **Do** set every display word in per-letter flap cells (xl for open/close, md for panel headings).
- **Do** reserve red for late, stopped, deleted, or objection, and amber for attention and header paint.
- **Do** label invented example content with the amber CONTOH tag in the head bar.
- **Do** keep the cascade to a single load-time run and show the settled board under reduced motion.

### Don't:
- **Don't** add rounded cards, per-panel shadows, or borders between panels; the steel gap is the divider.
- **Don't** introduce a third lamp color or a brand accent fill.
- **Don't** set a display headline as free type outside the flap cells.
- **Don't** place a small label above a heading; panel context goes in the head bar beside the heading.
- **Don't** add airport or travel props beyond the board itself (planes, gates, tickets).
- **Don't** animate on scroll or loop the flip; the board flips once.
