# BayesStack Slide Authoring Guide

## Mental model

Every slide has three layers: **chrome** (header/footer, always managed by the theme), a **content area** (what you author), and an optional **canvas mode** (whether chrome is present at all). Your job as an author is to choose a canvas mode, pick the right component(s) for the content type, and use gap tokens instead of raw `\vspace{}`.

---

## Standard frame authoring

The vast majority of slides use a standard chrome frame:

```latex
\begin{frame}{Your frametitle here}
  \begin{ConceptCard}{Title of card}
    Your content here.
  \end{ConceptCard}
  \BayesGap
  \TakeawayBanner{The one thing a learner must leave with.}
\end{frame}
```

Keep frametitles under 80 characters. The accent rule below the title truncates gracefully but very long titles compress the content area.

---

## Component quick reference

| Component | Semantic use | Accent colour |
|---|---|---|
| `LearningGoals` | Topic/session objectives | Teal (OUTCOMES badge) |
| `DefinitionCard` | Formal definition | Blue (THEORY badge) |
| `InsightCard` | Key conceptual observation | Teal (CORE badge) |
| `CautionCard` | Common pitfall or invariant to watch | Amber (WATCHOUT badge) |
| `WorkedExample` | Worked calculation or derivation | Plum (APPLIED badge) |
| `KeyTakeaway` | Summary or closing point | Teal (SUMMARY badge) |
| `ProofSketch` | Mathematical derivation or proof | Dark (RIGOR badge) |
| `ExerciseCard` | Active challenge or lab | Teal (LAB badge) |
| `ConceptCard` | General concept, flexible | Teal (custom badge) |
| `DeepDiveCard` | Advanced / optional material | Deep teal |
| `BayesEquation` | Boxed display equation | Pale/teal |
| `MathDerivationStep` | Single numbered derivation step | Deep teal |
| `StatCard` | Single metric tile | Teal top accent |
| `StatGridTwo/Three/Four` | 2–4 metric tiles in a row | — |
| `CompareGrid` | Two-column trade-off comparison | Blue vs teal |
| `TwoPane` | General two-column layout | — |
| `TakeawayBanner` | Full-width dark punchline | Dark/teal |
| `TerminalWindow` | Terminal/CLI output | Dark terminal |
| `CodeBlock` | Syntax-highlighted code | Teal code theme |
| `ArchitectureCard` | System diagram container | Teal (ARCHITECTURE) |
| `AlgorithmCard` | Algorithm/pseudocode block | Teal |
| `QuantPayoffCard` | Finance payoff and Greeks | Amber (QUANT) |

---

## Canvas mode selection

| Mode | How to use | When to use |
|---|---|---|
| **Standard** | `\begin{frame}{Title}...\end{frame}` | Default — most slides |
| **FullCanvas** | `\begin{FullCanvas}...\end{FullCanvas}` | Large TikZ diagrams, full-screen images, custom compositions |
| **DarkCanvas** | `\begin{DarkCanvas}...\end{DarkCanvas}` | Dramatic session transitions, emphasis slides |
| **LightCanvas** | `\begin{LightCanvas}...\end{LightCanvas}` | Soft topic dividers, gentle emphasis |

Canvas environments suppress header and footer automatically. Do not manually call `\setbeamertemplate{footline}{}` — use a canvas environment instead.

---

## Gap and spacing tokens

Replace bare `\vspace{}` with named tokens from `bayesstackgeometry.sty`:

| Token | Size | Use |
|---|---|---|
| `\BayesSmallGap` | 0.08 cm | Tight — within a logical group |
| `\BayesGap` | 0.15 cm | Standard — between two components |
| `\BayesBigGap` | 0.28 cm | Spacious — after a major section or banner |
| `\BayesHGap` | 0.15 cm | Horizontal — between inline elements |

These are the central tuning point. If all slides feel tight or loose after the first render, adjust the values in `bayesstackgeometry.sty` once rather than editing every slide.

---

## Layout helpers

```latex
% Figure left (52%), explanation right
\FigureExplain{figure-content}{explanation-content}
\FigureExplain[.60]{figure-content}{explanation-content}  % custom ratio

% Explanation left, figure right
\ExplainFigure{explanation-content}{figure-content}

% Two stacked components with \BayesGap between them
\SlideTwo{top-content}{bottom-content}

% Three stacked with \BayesGap
\SlideThree{a}{b}{c}

% Top content + vfill + bottom content (bottom anchored to foot)
\SlideFill{main-content}{anchored-footer-content}

% Convenience: main content + BayesCaption anchored at foot
\SlideCaption{main-content}{Caption text here.}
```

---

## Debug mode

Enable layout guides to see the content area boundary, header/footer zones, and content dimensions while authoring:

```latex
% Enable globally for a file:
\usepackage[debug]{bayesstackslides}

% Enable/disable around specific slides:
\BayesDebugOn
\begin{frame}{...}...\end{frame}
\BayesDebugOff
```

The red dashed rectangle marks the safe content zone. Content outside it will collide with chrome. Debug guides never appear in production builds (the flag defaults to false).

---

## Overflow detection

Wrap frame body content with `\BayesOverflowCheck` to get a compile-time warning if content exceeds the content area height:

```latex
\begin{frame}{Dense slide}
  \BayesOverflowCheck[dense-slide-01]{%
    \begin{ConceptCard}{...}...\end{ConceptCard}
    \BayesGap
    \BayesEquation{...}
    \BayesGap
    \TakeawayBanner{...}
  }
\end{frame}
```

This is an early-warning aid, not a guarantee. Visual inspection on the rendering machine is authoritative.

---

## When to split a slide

Split when any of these apply:
- Content overflows visually into the footer zone (check with debug guides).
- You are using `\BayesSmallGap` between every component to force content in.
- A single component (e.g., `WorkedExample`) already fills 80%+ of the content area and you want to add another.
- You have reduced font sizes below `\footnotesize` to make content fit.

Do not shrink font sizes as a fix — that reduces readability for the audience. Split the slide instead.

---

## Common patterns (copy-paste)

**Goals + takeaway:**
```latex
\begin{frame}{Learning goals}
  \begin{LearningGoals}{By the end of this topic, learners can}
    \begin{itemize}
      \item outcome one; and
      \item outcome two.
    \end{itemize}
  \end{LearningGoals}
  \BayesGap
  \TakeawayBanner{The single most important point from this topic.}
\end{frame}
```

**Two derivation steps + takeaway:**
```latex
\begin{frame}{Derivation title}
  \MathDerivationStep{1}{Step name}{math}{Analytical invariant explanation.}
  \BayesSmallGap
  \MathDerivationStep{2}{Step name}{math}{Analytical invariant explanation.}
  \BayesGap
  \TakeawayBanner{What the derivation proves.}
\end{frame}
```

**Stats + concept:**
```latex
\begin{frame}{Latency benchmarks}
  \StatGridThree{%
    \StatCard{1 ns}{L1}{4 cycles}{64 KB/core}%
  }{%
    \StatCard{28 ns}{L3}{55 cycles}{32 MB}%
  }{%
    \StatCard{95 ns}{DRAM}{220 cycles}{Off-chip}%
  }
  \BayesGap
  \begin{ConceptCard}[MEMORY WALL]{The Latency Gap}
    A single DRAM miss stalls the pipeline for 220 cycles.
  \end{ConceptCard}
\end{frame}
```

---

## What not to do

- **Do not** use `\vspace{.12cm}` or `\vspace{.15cm}` — use `\BayesGap` or `\BayesSmallGap`.
- **Do not** manually call `\setbeamertemplate{footline}{}` — use a canvas environment.
- **Do not** manually set font sizes smaller than `\footnotesize` to make content fit — split the slide.
- **Do not** use absolute TikZ coordinates (`\node at (3.2, 1.7)`) for ordinary content — use tcolorbox components.
- **Do not** use `\textwidth` arithmetic for column widths manually — use `\TwoPane`, `\FigureExplain`, or `\ExplainFigure`.
- **Do not** add TikZ `remember picture, overlay` inside a content component that will be reused — it will break standalone compilation.
