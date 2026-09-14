# BayesStack Video Generation Infrastructure (`src/videos/`)

The **BayesStack Video Generation Engine** is an automated, code-first video production pipeline designed for high-density, self-paced mathematical, scientific, and software engineering video lectures.

It transforms structured narration scripts and Manim Python scene code into fully composited 1080p/4K MP4 lectures with synchronized subtitles and audio narration.

---

## 1. Architecture Overview

```
src/videos/
├── engine/                      # Core Video Generation Pipeline
│   ├── tts/                     # Text-to-Speech Providers
│   │   ├── base.py              # BaseTTSProvider, AudioSynthesisResult, WordTimestamp
│   │   └── providers.py         # EdgeTTSProvider, MockTTSProvider, Azure/Google stubs
│   ├── subtitles/               # Subtitle Generation & Alignment
│   │   └── aligner.py           # SubtitleAligner (SRT / WebVTT export with timestamps)
│   ├── visual/                  # Animation & Motion Graphics Base
│   │   └── manim_base.py        # BayesStackScene, branding colors, UI card components
│   ├── compositor/              # Timeline & Multi-Track Assembly
│   │   ├── timeline.py          # VideoTimeline, SceneSegment, TimelineBuilder
│   │   └── ffmpeg_compositor.py # VideoCompositor (FFmpeg muxing, audio overlay, subs)
│   └── pipeline.py              # CLI Driver & Build Orchestration
├── templates/                   # Standardized starter files
│   ├── narration_template.yaml  # Scene-by-scene voiceover script format
│   ├── scene_template.py        # Manim scene template with BayesStack branding
│   └── project.json             # Resolution, FPS, voice, and subtitle configuration
├── sample/                      # End-to-end working reference project
│   └── session-01-bayesian-inference/
│       ├── narration.yaml       # Sample voiceover script
│       ├── scene.py             # Sample Manim scene animations
│       └── project.json         # Session video metadata
└── README.md                    # This documentation
```

---

## 2. Directory Structure in Courses

Every course repository inside `courses/` contains a dedicated `videos/` folder with generator code organized by session:

```
courses/<Course-Folder>/
├── decks/                       # Slide decks (in-class presentation)
├── notes/                       # Publication book notes (reading material)
└── videos/                      # Self-paced video generator code
    └── session-01-<slug>/
        ├── narration.yaml       # Structured narration & cues
        ├── scene.py             # Manim motion graphics / visual scene
        └── project.json         # (Optional) overrides for resolution/voice
```

> **Binary Isolation Guarantee**:
> All rendered video files (`*.mp4`, `*.mov`, `*.webm`), audio stems (`*.wav`, `*.mp3`), and Manim caches (`media/`, `.manim/`) are strictly excluded in `.gitignore`. The repository **only tracks generator code and voiceover scripts**.

---

## 3. Pipeline Stages

1. **Narration Parsing**: Loads `narration.yaml`, extracts scene text, cue markers, and duration targets.
2. **Speech Synthesis (TTS)**: Generates crystal-clear neural voiceover stems with word-level boundary timestamps (`edge-tts`, Azure Speech, or Google Cloud TTS).
3. **Subtitle Synchronization**: Derives millisecond-accurate `.srt` and `.vtt` cue files aligned to the speech synthesis output.
4. **Visual Rendering**: Compiles Manim scene Python scripts (`scene.py`) applying the BayesStack design system (Teal/Dark theme, Outfit & Inter fonts, card containers, LaTeX formulas).
5. **Timeline Composition**: Assembles visual clips and audio tracks according to the timeline segment specifications, padding or trimming holds to match narration duration.
6. **FFmpeg Final Muxing**: Renders the final H.264/AAC MP4 video with optional soft/hard subtitles into the local `build/courses/<Course>/videos/` directory.

---

## 4. Usage & Commands

Run commands from the `learning-content/` root or `src/` directory:

```bash
# Render the playable sample video (narration, subtitles, MP4)
make sample-videos

# Build videos for a specific course
make videos COURSE="CS 101 - Introduction to Computational Thinking"

# Validate scaffolding across all 183 courses (decks, notes, videos)
make scaffold-check
```

### Direct CLI Execution

```bash
.venv/bin/python src/videos/engine/pipeline.py \
  --project src/videos/sample/session-01-bayesian-inference \
  --output-dir build/sample/videos \
  --render
```

## Local setup

The production path requires a TTS provider and an FFmpeg binary. From the
`learning-content/` root, create a project-local environment and install the
declared dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r src/videos/requirements.txt
make -C src sample-videos
```

`edge-tts` supplies the sample narration. `imageio-ffmpeg` supplies a local
FFmpeg binary when no system `ffmpeg` command is available. If Manim is not
installed, the engine produces branded motion-hold cards for each narration
segment; this keeps every sample and course video playable while allowing
individual sessions to adopt bespoke Manim animation later.
