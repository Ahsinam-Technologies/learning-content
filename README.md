# BayesStack Multi-Format Course Publishing & Video Generation Platform

This repository implements a modular, extensible academic platform separating **reusable engine infrastructure (`src/`)** from **pure course learning content (`courses/`)**:

1. **`src/`**: The consolidated platform engine housing core assets, typography, curriculum data, the in-class slide deck engine (`decks/`), the publication-ready reading book engine (`notes/`), and the self-paced video generation pipeline (`videos/`).
2. **`courses/` (183 courses)**: Strictly **content & script-only** directories. Each course contains:
   - `decks/`: In-class slide presentation modules organized into **sessions** and **topics**.
   - `notes/`: Comprehensive publication reading book modules organized into **chapters** and **sections**.
   - `videos/`: Self-paced video generation scripts (Manim scene scripts and narration files) organized into **sessions**.
   - Zero LaTeX documentclass, preambles, or video rendering boilerplate.
3. **`build/`**: Hierarchical build output folder mirroring the course directory structure (`build/courses/<Course>/decks/`, `build/courses/<Course>/notes/`, `build/courses/<Course>/videos/`).

---

## Repository Tree Architecture

```text
learning-content/
├── src/                                        # CENTRAL PUBLISHING & VIDEO ENGINE
│   ├── core/                                   # Shared foundations
│   │   ├── fonts/                              # Inter and Outfit TrueType font assets
│   │   ├── assets/                             # BayesStack style guide (style.md) & wordmarks
│   │   ├── data/                               # Master curriculum spreadsheet (master curriculum.xlsx)
│   │   └── render_wrapper.py                   # Automated LaTeX wrapper driver & escaper
│   ├── decks/                                  # In-class slide deck engine
│   │   ├── theme/                              # bayesstackslides.sty (Beamer presentation package)
│   │   ├── templates/                          # Session, topic, and course deck templates
│   │   └── sample/                             # Reference visual test deck (gallery-deck.tex)
│   ├── notes/                                  # Reading material / book publishing engine
│   │   ├── theme/                              # bayesstacknotes.sty (Two-column publication book package)
│   │   ├── templates/                          # Chapter, section, and course book templates
│   │   └── sample/                             # Reference publication book sample (sample-notes.tex)
│   ├── videos/                                 # Self-paced video generation engine
│   │   ├── engine/                             # TTS, subtitles, visual animation, and compositor
│   │   ├── templates/                          # Starter scene.py and narration.yaml templates
│   │   └── sample/                             # Reference video generation project
│   ├── Makefile                                # Main build engine
│   └── README.md                               # Infrastructure documentation
├── courses/                                    # 183 CONTENT & GENERATOR COURSE FOLDERS
│   ├── cs-101-introduction-to-computational-thinking/
│   │   ├── decks/                              # In-class lecture materials
│   │   │   └── session-01-name/
│   │   │       ├── session-01-name-content.tex
│   │   │       └── topics/
│   │   │           └── topic-01-name-content.tex
│   │   ├── notes/                              # Reading book materials (2-column letterpaper)
│   │   │   └── chapter-01-name/
│   │   │       ├── chapter-01-name-content.tex
│   │   │       └── sections/
│   │   │           └── section-01-name-content.tex
│   │   └── videos/                             # Self-paced video generation source code
│   │       └── session-01-name/
│   │           ├── narration.yaml              # Voiceover script & TTS timestamps
│   │           └── scene.py                    # Manim / visual animation code
│   └── ... (all 183 courses)
├── .creds/                                     # Local credentials (ignored by git)
├── build/                                      # Hierarchical build deliverables
│   ├── sample/
│   │   ├── decks/gallery-deck.pdf
│   │   ├── notes/sample-notes.pdf
│   │   └── videos/
│   └── courses/<course-slug>/
│       ├── decks/
│       │   ├── <Course Name> - Slides.pdf
│       │   └── session-XX-<name>.pdf
│       ├── notes/
│       │   ├── <Course Name> - Notes.pdf
│       │   └── chapter-XX-<name>.pdf
│       └── videos/                             # Video output deliverables (git ignored)
├── Makefile                                    # Root forwarding Makefile
└── README.md                                   # This repository overview
```

---

## Academic & Instructional Modalities

| Learning Modality | Platform Term | Scope & Role | Course Directory Subfolder |
| :--- | :--- | :--- | :--- |
| **In-Class Material** | **`session`** | Coherent lecture or seminar meeting block | `courses/<course-slug>/decks/session-XX-*/` |
| **In-Class Unit** | **`topic`** | Focused presentation unit / micro-agenda | `courses/<course-slug>/decks/.../topics/` |
| **Reading Material** | **`chapter`** | Comprehensive narrative exposition book unit | `courses/<course-slug>/notes/chapter-XX-*/` |
| **Reading Unit** | **`section`** | In-depth prose section with definitions & derivations | `courses/<course-slug>/notes/.../sections/` |
| **Self-Paced Video** | **`video-session`** | Narrated & animated computational video lesson | `courses/<course-slug>/videos/session-XX-*/` |

---

## Quick Start (Build Commands)

Run from either the repository root or within `src/`:

```bash
# 1. Build Reference Samples
make gallery-deck                                                        # Reference masterclass slide deck (30 Editorial Compositions)
make sample-notes                                                        # Reference publication book
make sample-videos                                                       # Reference video pipeline
make sample                                                              # All reference samples

# 2. Build Assembled Course Materials
make course COURSE="cs-101-introduction-to-computational-thinking"       # Slides, Notes, and Videos
make decks  COURSE="cs-101-introduction-to-computational-thinking"       # Assembles slides only
make notes  COURSE="cs-101-introduction-to-computational-thinking"       # Assembles reading book only
make videos COURSE="cs-101-introduction-to-computational-thinking"       # Plans/builds course videos

# 3. Build Standalone Units
make session SESSION="cs-101-introduction-to-computational-thinking/decks/session-01-course-orientation"
make chapter CHAPTER="cs-101-introduction-to-computational-thinking/notes/chapter-01-course-orientation"
make topic   TOPIC="cs-101-introduction-to-computational-thinking/decks/session-01-course-orientation/topics/topic-01-course-orientation-content.tex"
make section SECTION="cs-101-introduction-to-computational-thinking/notes/chapter-01-course-orientation/sections/section-01-course-orientation-content.tex"

# 4. Verification and Integrity Check
make scaffold-check                                                      # Checks all 183 courses in courses/ (decks, notes, videos)

# 5. Clean Build Artifacts
make clean
```
