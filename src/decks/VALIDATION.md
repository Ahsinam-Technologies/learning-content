# BayesStack Slide System — Rendering Validation Checklist

This document guides the first rendering pass on the fully provisioned machine (XeLaTeX + Beamer + all packages installed). Its purpose is to produce actionable feedback rather than require architectural debugging.

---

## 1. Prerequisites

- XeLaTeX (TeX Live 2023+ recommended) or LuaLaTeX as fallback
- Beamer, tcolorbox (with skins/raster), pgfplots, tikz, listings, fontspec, microtype
- Fonts: Inter (Regular + SemiBold) and Outfit (Regular + SemiBold) in `src/core/fonts/`
- Python 3.10+ with `latexmk` available (for the Makefile build path)

---

## 2. Build commands

### Gallery (primary validation target)

Compile from the `src/decks/sample/` directory:

```bash
cd src/decks/sample
TEXINPUTS=../../theme:../../../notes/theme:../../core/fonts:../../core/assets:../../core/assets/img: \
  latexmk -xelatex -interaction=nonstopmode -file-line-error gallery-deck.tex
```

Expected output: `gallery-deck.pdf` (approximately 40–45 slides).

### Reference sample deck (Gallery 2.0)

```bash
cd src
make gallery-deck
```

Expected output: `build/sample/decks/gallery-deck.pdf`.

### Reference notes (confirm no regression)

```bash
cd src
make sample-notes
```

Expected output: `build/sample/notes/sample-notes.pdf`.

### Single course (integration test)

```bash
cd src
make decks COURSE=cs-101-introduction-to-computational-thinking
```

---

## 3. Gallery section inspection checklist

Work through `gallery-deck.pdf` section by section.

### Section 1 — Canvas Modes (slides 2–5)

| Slide | Check |
|---|---|
| S1.1 Standard | Frametitle with teal accent rule; footer with course code left, wordmark + page number right |
| S1.2 FullCanvas | Blank white slide; NO header, NO footer; text centred on full page |
| S1.3 DarkCanvas | BayesDark background; NO header, NO footer; text in white/pale colour |
| S1.4 LightCanvas | BayesPale background; NO header, NO footer |

### Section 2 — Educational Containers (slides 6–13)

Verify for each container:
- Left accent bar present and correct colour (see AUTHORING.md quick reference)
- Pill badge visible top-right with correct label
- Title text in correct colour
- Body text readable at normal viewing distance

### Section 3 — Math Components (slides 14–17)

| Slide | Check |
|---|---|
| S3.1 BayesEquation | Equation at `\displaystyle`; centred tcolorbox; 90% textwidth; teal border |
| S3.2 Single step | Step badge left; equation in pale box centre; invariant text right; columns aligned |
| S3.3 Two steps | Both steps fully visible; neither overlaps the footer |
| S3.4 ProofSketch math | Display equation inside ProofSketch is not clipped; box height expands naturally |

### Section 4 — Data & Metrics (slides 18–20)

Check that all stat cards are top-aligned and equally spaced. StatGridFour should not cause text to clip inside the narrow cards.

### Section 5 — Code and Terminal (slides 21–23)

| Slide | Check |
|---|---|
| S5.1 CodeBlock | Teal keyword colour; plum string colour; gray comment colour; line numbers left |
| S5.2 HighlightedCodeBlock | Line 4 has distinct CodeHighlight background; other lines standard |
| S5.3 TerminalWindow | Dark terminal background; traffic-light dots; monospace output |

### Section 6 — Layout Primitives (slides 24–28)

| Slide | Check |
|---|---|
| S6.1 TwoPane | Two equal columns, top-aligned |
| S6.2 CompareGrid | Left column blue top accent; right column teal top accent |
| S6.3 FigureExplain | Figure left (~52%); explanation right; PGFPlots renders |
| S6.4 ExplainFigure | Text left; figure right; proportions mirror S6.3 |
| S6.5 SlideFill | Top card at natural height; caption anchored at foot of content area |

### Section 7 — Architecture & Algorithm (slides 29–31)

Verify TikZ diagrams inside ArchitectureCard render without clipping. Arrow tips should be sharp (Latex tip style).

### Section 8 — Composite Patterns (slides 32–36)

These are the reference patterns for real authoring. Check that:
- Components are visually separated by consistent gaps
- TakeawayBanner fills the full text width
- No component bleeds into the footer zone

### Section 9 — Gap Token Comparison (slide 37)

Three visually distinct gaps should be visible between the blocks. If all gaps look identical, the gap tokens may have been inadvertently set to the same value.

### Section 10 — Debug Mode (slides 38–39)

| Expected guide | Colour |
|---|---|
| Content area boundary (safe zone) | Red dashed rectangle |
| Header chrome zone | Blue tinted band |
| Header/content boundary | Blue dotted line |
| Footer chrome zone | Green tinted band |
| Footer/content boundary | Green dotted line |
| Vertical midpoint of content | Gray dotted line |
| Dimension label (bottom-right) | Small red-black text |

After slide 39, debug mode is disabled — slides 40+ must have NO guide overlay.

### Section 11 — Edge Cases (slides 40–42)

| Slide | Check |
|---|---|
| S11.1 Long frametitle | Title wraps or truncates; does not collide with content area or footer |
| S11.2 Dense slide | All three components visible; bottom component not hidden behind footer |
| S11.3 Single large component | WorkedExample fills most of content area; math is readable |

---

## 4. Expected compile-time warnings

| Warning source | Text | When |
|---|---|---|
| `bayesstackdebug` | `Content overflow on slide (label): measured X, content area Y (excess: Z).` | Only if `\BayesOverflowCheck` wraps content that exceeds `\BayesContentHeight` |
| Beamer | `You are using the class option 'aspectratio=169'` | Normal |
| pgfplots | `compat=1.18` notice | Normal |

No warnings from `bayesstackgeometry`, `bayesstacklayouts`, or the three new `\RequirePackage` calls are expected. If you see `Package bayesstackdebug Warning:` outside of slides where `\BayesOverflowCheck` is used, investigate the content on that slide.

---

## 5. What constitutes a failure

**Hard failures** (architectural defect — investigate before proceeding):
- PDF does not compile (non-zero `latexmk` exit code)
- Any canvas environment leaves residual header or footer visible
- Debug guides appear on slides after `\BayesDebugOff`
- Any component's tcolorbox extends beyond the red dashed content boundary when debug mode is on
- Font fallback to TeX Gyre Heros (means Inter/Outfit TTF not found on TEXINPUTS)

**Soft failures** (numerical tuning — expected, adjust centrally):
- Small gaps between chrome and content (see Section 8 below)
- Component appears slightly too close to footer
- Gap token sizes look too tight or too loose

---

## 6. Central tuning constants and where to find them

All geometry constants are in `src/decks/theme/bayesstackgeometry.sty`. Edit there; do not patch individual slides.

| Constant | Current value | What to adjust if... |
|---|---|---|
| `\BayesHeaderHeight` | 11.5 mm | Content consistently starts too high (decrease) or overlaps frametitle (increase) |
| `\BayesFooterHeight` | 5.6 mm | Content overlaps footline (increase) or too much gap above footline (decrease) |
| `\BayesSafeMarginH` | 7.8 mm | Left/right chrome collision (adjust to match `\setbeamersize` value) |
| `\BayesGap` | 0.18 cm | All slides too tight (increase) or too spacious (decrease) |
| `\BayesSmallGap` | 0.10 cm | Tight gaps look incorrect |
| `\BayesBigGap` | 0.32 cm | Large gaps look incorrect |

`BayesContentHeight` and `BayesContentWidth` are derived automatically in `\AtBeginDocument` — do not set them directly.

---

## 7. Distinguishing numerical tuning from architectural defects

| Symptom | Likely category | Action |
|---|---|---|
| Consistent small gap above all frametitles | Numerical tuning | Decrease `\BayesHeaderHeight` by 0.5–1 mm |
| Content routinely overflows by a small amount | Numerical tuning | Increase `\BayesHeaderHeight` or `\BayesFooterHeight` |
| Debug guides appear on wrong slides | Architectural defect | Check `\BayesDebugOn`/`\BayesDebugOff` placement |
| Canvas environments show residual chrome | Architectural defect | Check Beamer template override order in `bayesstackgeometry.sty` |
| Font is TeX Gyre Heros instead of Inter | Environment defect | Verify TEXINPUTS includes `src/core/fonts/` directory |
| FullCanvas content is clipped at paper edge | Numerical tuning | Adjust content placement; 160×90mm is the hard boundary |
| New `.sty` files not found | Environment defect | Verify TEXINPUTS includes `src/decks/theme/` |

Numerical tuning after the first render is expected and normal. Architectural debugging should be minimal if the implementation is correct.

---

## 8. Gallery 3.0 projection QA pass

After every gallery change, render the full deck and inspect these representative risk cases at 100\% zoom:

- title slide: course-code pill and series line have visibly separate vertical lanes;
- standard chrome: title sits close to, but not on, its dividing rule; footer reads `current / total`;
- derivations: headings, equations, and interpretation text use the same named spacing sequence;
- diagrams: node bounding boxes and connectors do not overlap after font substitution;
- long equations and canvas statements: a bounded panel or text width keeps content inside the safe margin;
- tables and provenance labels: no right-edge clipping; compress metadata rather than shrinking the slide typography.

Treat any `Overfull \\hbox` or `Overfull \\vbox` in a changed gallery slide as a release blocker unless it is investigated and explicitly accepted.

---

## 9. Notes system regression check

After validating the gallery, confirm the notes system is unaffected:

```bash
cd src
make sample-notes
```

Open `build/sample/notes/sample-notes.pdf` and verify:
- Cover page, copyright page, table of contents render
- Chapter openers render correctly
- All tcolorbox environments (intuitionbox, interviewbox, etc.) are present
- Running headers and footers are present
- Two-column layout is intact on body pages

If the notes system fails, the regression is in the shared `bayesstackslides.sty` changes (the `debug` option declaration or the extension module `\RequirePackage` calls). The fix is to verify that `bayesstacknotes.sty` does not import `bayesstackslides.sty` (it does not — they are independent packages).
