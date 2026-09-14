# `src/` — Central Learning OS Publishing & Video Generation Infrastructure

This directory houses the **centralized publishing engines, typography, visual tokens, video generation pipelines, and authoring templates** for all 183 courses across institutional tenants on the BayesStack Learning OS platform.

Individual course folders in `courses/` contain **strictly learning content and generator scripts** (`*-content.tex`, `narration.yaml`, `scene.py`). All compilation drivers, geometry definitions, document classes, color palettes, TTS/video pipeline engines, and environments reside here in `src/`.

---

## 1. Directory Architecture & Modalities

The infrastructure is partitioned into modular modalities:

```
src/
├── core/                       # Shared platform foundations
│   ├── fonts/                  # Bundled TTF fonts (Inter, Outfit)
│   ├── assets/                 # Brand guide (style.md), logos, wordmarks
│   ├── data/                   # Master curriculum workbook (master curriculum.xlsx)
│   └── render_wrapper.py       # Automated driver generator & LaTeX escaper
│
├── decks/                      # In-Class Slide Deck Infrastructure
│   ├── theme/                  # bayesstackslides.sty (Beamer presentation package)
│   ├── templates/              # session, topic, and course deck templates
│   └── sample/                 # Reference visual sample deck (sample-decks.tex)
│
├── notes/                      # Reading Notes & Publication Book Infrastructure
│   ├── theme/                  # bayesstacknotes.sty (Two-column publication book package)
│   ├── templates/              # chapter, section, and course book templates
│   └── sample/                 # Reference publication book sample (sample-notes.tex)
│
├── videos/                     # Self-Paced Video Generation Engine
│   ├── engine/                 # TTS, subtitle sync, Manim visual wrappers, timeline compositor
│   │   ├── tts/                # Text-to-speech providers (Edge-TTS, ElevenLabs, OpenAI, Piper)
│   │   ├── subtitles/          # Word-level timestamp aligner & SRT/VTT generator
│   │   ├── visual/             # Manim scene base classes & motion graphics helpers
│   │   ├── compositor/         # Multi-track audio/video synchronizer & FFmpeg pipeline
│   │   └── pipeline.py         # Video build CLI and batch orchestrator
│   ├── templates/              # Starter scene.py, narration.yaml, and project configs
│   ├── sample/                 # Reference video generation project (Bayesian Inference)
│   └── README.md               # Video engine developer guide
│
├── Makefile                    # Unified compilation & pipeline engine
└── README.md                   # Infrastructure documentation
```

### Future Infrastructure Slots
The modular design allows adding further instructional formats seamlessly:
- **`assignments/`**: Problem sets, solution keys, rubrics, and grading sheets.
- **`mcqs/`**: Multiple-choice assessment banks with randomized permutations.
- **`labs/`**: Step-by-step practical computing notebooks and instructions.

---

## 2. Academic Terminology

| Learning Modality | Platform Term | Scope & Role | Course Directory Subfolder |
| :--- | :--- | :--- | :--- |
| **In-Class Material** | **`session`** | Coherent lecture or seminar meeting block | `courses/<Course>/decks/session-XX-*/` |
| **In-Class Unit** | **`topic`** | Focused presentation unit / micro-agenda | `courses/<Course>/decks/.../topics/` |
| **Reading Material** | **`chapter`** | Comprehensive narrative exposition book unit | `courses/<Course>/notes/chapter-XX-*/` |
| **Reading Unit** | **`section`** | In-depth prose section with definitions & derivations | `courses/<Course>/notes/.../sections/` |
| **Self-Paced Video** | **`video-session`** | Narrated & animated computational video lesson | `courses/<Course>/videos/session-XX-*/` |

---

## 3. Visual & Typographic Standards (BayesStack Design System)

All published materials adhere to the official **BayesStack Mint & Teal Design System** (`src/core/assets/style.md`):

### Palette Tokens
- **`BayesTeal`** (`#0B6763`): Primary interactive brand color.
- **`BayesDeepTeal`** (`#084C49`): Headers, callout frames, and table header rows.
- **`BayesDark`** (`#091A18`): Dark neutral base for slide backgrounds and high-contrast elements.
- **`BayesInk`** (`#123333`): High-legibility deep ink for body typography.
- **`BayesPale`** (`#E4F2EF`): Soft mint tint for callouts, code backgrounds, and table zebra striping.
- **`BayesBorder`** (`#D7E8E4`): Clean neutral border rule color.
- **Semantic Accents**: `BayesAmber` (`#964200`), `BayesBlue` (`#125282`), `BayesPlum` (`#5E3268`), `BayesGreen` (`#1A6634`), `BayesBrown` (`#5F370E`).

---

## 4. Build Commands

From the workspace root or `src/`:

```bash
# 1. Reference Samples
make sample-decks
make sample-notes
make sample-videos
make sample

# 2. Assembled Course Materials
make course COURSE="CS 101 - Introduction to Computational Thinking"
make decks  COURSE="CS 101 - Introduction to Computational Thinking"
make notes  COURSE="CS 101 - Introduction to Computational Thinking"
make videos COURSE="CS 101 - Introduction to Computational Thinking"

# 3. Validation
make scaffold-check
```
