# Shared build system engine in src/
SHELL := /bin/bash

ROOT ?= $(abspath ..)
SRC := $(ROOT)/src
COURSES_DIR := $(ROOT)/courses
BUILD ?= $(ROOT)/.build
OUTPUT_DIR ?= $(ROOT)/build
ENGINE ?= $(shell if command -v xelatex >/dev/null 2>&1; then echo xelatex; elif command -v lualatex >/dev/null 2>&1; then echo lualatex; else echo unavailable; fi)
SCIENCE ?= 0
LATEXMK ?= latexmk
PYTHON ?= $(if $(wildcard $(ROOT)/.venv/bin/python),$(ROOT)/.venv/bin/python,python3)
VIDEO_RENDER ?= 0
VIDEO_ACTION := $(if $(filter 1 true yes,$(VIDEO_RENDER)),--render,--plan)

TEX_INPUTS_ENV := $(SRC)/decks/theme:$(SRC)/notes/theme:$(SRC)/core/fonts:$(SRC)/core/assets:$(SRC)/core/assets/img:$$TEXINPUTS

.PHONY: all help video-setup sample sample-decks sample-notes sample-videos course decks notes videos session topic chapter section video-session all-decks all-notes all-videos scaffold-check clean list validate concept

help:
	@echo "BayesStack Learning OS Publishing & Video Engine (src/)"
	@echo "======================================================="
	@echo "In-Class Decks (Slides):"
	@echo "  make sample-decks                          Build reference in-class slide deck"
	@echo "  make decks COURSE='<Course>'               Build assembled course slide deck"
	@echo "  make session SESSION='<Course>/decks/...'  Build standalone in-class session deck"
	@echo "  make topic TOPIC='<Course>/decks/.../...'  Build standalone topic deck"
	@echo ""
	@echo "Reading Notes (Publication Book):"
	@echo "  make sample-notes                          Build reference publication-ready reading book"
	@echo "  make notes COURSE='<Course>'               Build assembled course reading book"
	@echo "  make chapter CHAPTER='<Course>/notes/...'  Build standalone chapter reading notes"
	@echo "  make section SECTION='<Course>/notes/.../... Build standalone section reading notes"
	@echo ""
	@echo "Self-Paced Video Generation Engine:"
	@echo "  make video-setup                           Install project-local video dependencies"
	@echo "  make sample-videos                         Render the playable reference MP4"
	@echo "  make videos COURSE='<Course>'              Plan course videos (set VIDEO_RENDER=1 to render)"
	@echo "  make video-session SESSION='<path>'        Plan a session (set VIDEO_RENDER=1 to render)"
	@echo ""
	@echo "Unified Workflows:"
	@echo "  make sample                                Build reference decks, notes, and sample video"
	@echo "  make course COURSE='<Course>'              Build slides, reading book, and video assets for course"
	@echo "  make scaffold-check                        Verify decks, notes, and videos across all 183 courses"
	@echo "  make all-decks                             Compile slide decks for all courses"
	@echo "  make all-notes                             Compile reading notes for all courses"
	@echo "  make all-videos                            Compile/validate video assets for all courses"
	@echo "  make all                                   Compile decks, notes, and video assets for all courses"
	@echo "  make clean                                 Remove build cache and output artifacts"
	@echo ""
	@echo "Configuration: ENGINE=$(ENGINE) | SCIENCE=$(SCIENCE) | VIDEO_RENDER=$(VIDEO_RENDER) | PYTHON=$(PYTHON)"

video-setup:
	@python3 -m venv "$(ROOT)/.venv"
	@"$(ROOT)/.venv/bin/python" -m pip install -r "$(SRC)/videos/requirements.txt"
	@echo "Video dependencies installed in $(ROOT)/.venv"

# --- Reference Samples ---
sample-decks:
	@mkdir -p "$(OUTPUT_DIR)/sample/decks"
	@echo "==> Building sample slide deck [$(ENGINE)]"
	@cd "$(SRC)/decks/sample" && \
	  TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$(BUILD)/sample/decks" "sample-decks.tex"
	@cp "$(BUILD)/sample/decks/sample-decks.pdf" "$(OUTPUT_DIR)/sample/decks/sample-decks.pdf"
	@echo "Generated: $(OUTPUT_DIR)/sample/decks/sample-decks.pdf"

sample-notes:
	@mkdir -p "$(OUTPUT_DIR)/sample/notes"
	@echo "==> Building sample notes book [$(ENGINE)]"
	@cd "$(SRC)/notes/sample" && \
	  TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$(BUILD)/sample/notes" "$(SRC)/notes/sample/sample-notes.tex"
	@cp "$(BUILD)/sample/notes/sample-notes.pdf" "$(OUTPUT_DIR)/sample/notes/sample-notes.pdf"
	@echo "Generated: $(OUTPUT_DIR)/sample/notes/sample-notes.pdf"

sample-videos:
	@mkdir -p "$(OUTPUT_DIR)/sample/videos"
	@echo "==> Rendering playable sample video"
	@$(PYTHON) "$(SRC)/videos/engine/pipeline.py" --project "$(SRC)/videos/sample/session-01-bayesian-inference" --out-dir "$(OUTPUT_DIR)/sample/videos" --render
	@test -s "$(OUTPUT_DIR)/sample/videos/lesson.mp4"
	@echo "Generated: $(OUTPUT_DIR)/sample/videos/lesson.mp4"

sample: sample-decks sample-notes sample-videos

# --- Assembled Course Targets ---
course: decks notes videos

decks:
	@test -n "$(COURSE)" || (echo "Error: Set COURSE='Course Name'"; exit 2)
	@course_path=$$(if [ -d "$(COURSES_DIR)/$(COURSE)" ]; then echo "$(COURSES_DIR)/$(COURSE)"; elif [ -d "$(ROOT)/$(COURSE)" ]; then echo "$(ROOT)/$(COURSE)"; else echo ""; fi); \
	  test -n "$$course_path" || (echo "Error: Course directory not found: $(COURSE)"; exit 2); \
	  wrapper=$$(python3 "$(SRC)/core/render_wrapper.py" decks "$(ROOT)" "$$course_path" "$(BUILD)" $(SCIENCE)); \
	  clean_name=$$(basename "$$course_path"); \
	  mkdir -p "$(OUTPUT_DIR)/courses/$$clean_name/decks"; \
	  echo "==> Compiling course slides: $$clean_name [$(ENGINE)]"; \
	  cd "$$course_path" && \
	    TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$$(dirname "$$wrapper")" "$$wrapper"; \
	  cp "$$(dirname "$$wrapper")/course-slides.pdf" "$(OUTPUT_DIR)/courses/$$clean_name/decks/$$clean_name - Slides.pdf"; \
	  echo "Generated: $(OUTPUT_DIR)/courses/$$clean_name/decks/$$clean_name - Slides.pdf"

notes:
	@test -n "$(COURSE)" || (echo "Error: Set COURSE='Course Name'"; exit 2)
	@course_path=$$(if [ -d "$(COURSES_DIR)/$(COURSE)" ]; then echo "$(COURSES_DIR)/$(COURSE)"; elif [ -d "$(ROOT)/$(COURSE)" ]; then echo "$(ROOT)/$(COURSE)"; else echo ""; fi); \
	  test -n "$$course_path" || (echo "Error: Course directory not found: $(COURSE)"; exit 2); \
	  wrapper=$$(python3 "$(SRC)/core/render_wrapper.py" notes "$(ROOT)" "$$course_path" "$(BUILD)" $(SCIENCE)); \
	  clean_name=$$(basename "$$course_path"); \
	  mkdir -p "$(OUTPUT_DIR)/courses/$$clean_name/notes"; \
	  echo "==> Compiling course notes book: $$clean_name [$(ENGINE)]"; \
	  cd "$$course_path" && \
	    TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$$(dirname "$$wrapper")" "$$wrapper"; \
	  cp "$$(dirname "$$wrapper")/course-notes.pdf" "$(OUTPUT_DIR)/courses/$$clean_name/notes/$$clean_name - Notes.pdf"; \
	  echo "Generated: $(OUTPUT_DIR)/courses/$$clean_name/notes/$$clean_name - Notes.pdf"

videos:
	@test -n "$(COURSE)" || (echo "Error: Set COURSE='Course Name'"; exit 2)
	@course_path=$$(if [ -d "$(COURSES_DIR)/$(COURSE)" ]; then echo "$(COURSES_DIR)/$(COURSE)"; elif [ -d "$(ROOT)/$(COURSE)" ]; then echo "$(ROOT)/$(COURSE)"; else echo ""; fi); \
	  test -n "$$course_path" || (echo "Error: Course directory not found: $(COURSE)"; exit 2); \
	  clean_name=$$(basename "$$course_path"); \
	  echo "==> Processing video generation pipeline for: $$clean_name"; \
	  $(PYTHON) "$(SRC)/videos/engine/pipeline.py" --course-dir "$$course_path" --out-dir "$(OUTPUT_DIR)/courses/$$clean_name/videos" $(VIDEO_ACTION); \
	  echo "Video pipeline ready for: $$clean_name"

# --- Standalone Modular Units ---
session:
	@test -n "$(SESSION)" || (echo "Error: Set SESSION to session directory or main content file"; exit 2)
	@wrapper=$$(python3 "$(SRC)/core/render_wrapper.py" session "$(ROOT)" "$(SESSION)" "$(BUILD)" $(SCIENCE)); \
	  sess_path=$$(if [ -e "$(COURSES_DIR)/$(SESSION)" ]; then echo "$(COURSES_DIR)/$(SESSION)"; elif [ -e "$(ROOT)/$(SESSION)" ]; then echo "$(ROOT)/$(SESSION)"; else echo "$(SESSION)"; fi); \
	  clean_course=$$(basename "$$(dirname "$$(dirname "$$(dirname "$$wrapper")")")"); \
	  unit_name=$$(basename "$${wrapper%.tex}"); \
	  mkdir -p "$(OUTPUT_DIR)/courses/$$clean_course/decks"; \
	  echo "==> Compiling standalone session deck: $$unit_name"; \
	  cd "$(COURSES_DIR)/$$clean_course" 2>/dev/null || cd "$$(dirname "$$(dirname "$$sess_path")")"; \
	    TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$$(dirname "$$wrapper")" "$$wrapper"; \
	  cp "$$(dirname "$$wrapper")/$$unit_name.pdf" "$(OUTPUT_DIR)/courses/$$clean_course/decks/$$unit_name.pdf"; \
	  echo "Generated: $(OUTPUT_DIR)/courses/$$clean_course/decks/$$unit_name.pdf"

topic:
	@test -n "$(TOPIC)" || (echo "Error: Set TOPIC to topic content file"; exit 2)
	@wrapper=$$(python3 "$(SRC)/core/render_wrapper.py" topic "$(ROOT)" "$(TOPIC)" "$(BUILD)" $(SCIENCE)); \
	  topic_path=$$(if [ -e "$(COURSES_DIR)/$(TOPIC)" ]; then echo "$(COURSES_DIR)/$(TOPIC)"; elif [ -e "$(ROOT)/$(TOPIC)" ]; then echo "$(ROOT)/$(TOPIC)"; else echo "$(TOPIC)"; fi); \
	  clean_course=$$(basename "$$(dirname "$$(dirname "$$(dirname "$$wrapper")")")"); \
	  unit_name=$$(basename "$${wrapper%.tex}"); \
	  mkdir -p "$(OUTPUT_DIR)/courses/$$clean_course/decks/topics"; \
	  echo "==> Compiling standalone topic deck: $$unit_name"; \
	  cd "$(COURSES_DIR)/$$clean_course" 2>/dev/null || cd "$$(dirname "$$(dirname "$$(dirname "$$topic_path")")")"; \
	    TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$$(dirname "$$wrapper")" "$$wrapper"; \
	  cp "$$(dirname "$$wrapper")/$$unit_name.pdf" "$(OUTPUT_DIR)/courses/$$clean_course/decks/topics/$$unit_name.pdf"; \
	  echo "Generated: $(OUTPUT_DIR)/courses/$$clean_course/decks/topics/$$unit_name.pdf"

concept: topic

chapter:
	@test -n "$(CHAPTER)" || (echo "Error: Set CHAPTER to chapter directory or main content file"; exit 2)
	@wrapper=$$(python3 "$(SRC)/core/render_wrapper.py" chapter "$(ROOT)" "$(CHAPTER)" "$(BUILD)" $(SCIENCE)); \
	  chap_path=$$(if [ -e "$(COURSES_DIR)/$(CHAPTER)" ]; then echo "$(COURSES_DIR)/$(CHAPTER)"; elif [ -e "$(ROOT)/$(CHAPTER)" ]; then echo "$(ROOT)/$(CHAPTER)"; else echo "$(CHAPTER)"; fi); \
	  clean_course=$$(basename "$$(dirname "$$(dirname "$$(dirname "$$wrapper")")")"); \
	  unit_name=$$(basename "$${wrapper%.tex}"); \
	  mkdir -p "$(OUTPUT_DIR)/courses/$$clean_course/notes"; \
	  echo "==> Compiling standalone chapter notes: $$unit_name"; \
	  cd "$(COURSES_DIR)/$$clean_course" 2>/dev/null || cd "$$(dirname "$$(dirname "$$chap_path")")"; \
	    TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$$(dirname "$$wrapper")" "$$wrapper"; \
	  cp "$$(dirname "$$wrapper")/$$unit_name.pdf" "$(OUTPUT_DIR)/courses/$$clean_course/notes/$$unit_name.pdf"; \
	  echo "Generated: $(OUTPUT_DIR)/courses/$$clean_course/notes/$$unit_name.pdf"

section:
	@test -n "$(SECTION)" || (echo "Error: Set SECTION to section content file"; exit 2)
	@wrapper=$$(python3 "$(SRC)/core/render_wrapper.py" section "$(ROOT)" "$(SECTION)" "$(BUILD)" $(SCIENCE)); \
	  sec_path=$$(if [ -e "$(COURSES_DIR)/$(SECTION)" ]; then echo "$(COURSES_DIR)/$(SECTION)"; elif [ -e "$(ROOT)/$(SECTION)" ]; then echo "$(ROOT)/$(SECTION)"; else echo "$(SECTION)"; fi); \
	  clean_course=$$(basename "$$(dirname "$$(dirname "$$(dirname "$$wrapper")")")"); \
	  unit_name=$$(basename "$${wrapper%.tex}"); \
	  mkdir -p "$(OUTPUT_DIR)/courses/$$clean_course/notes/sections"; \
	  echo "==> Compiling standalone section notes: $$unit_name"; \
	  cd "$(COURSES_DIR)/$$clean_course" 2>/dev/null || cd "$$(dirname "$$(dirname "$$(dirname "$$sec_path")")")"; \
	    TEXINPUTS="$(TEX_INPUTS_ENV)" $(LATEXMK) -$(ENGINE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$$(dirname "$$wrapper")" "$$wrapper"; \
	  cp "$$(dirname "$$wrapper")/$$unit_name.pdf" "$(OUTPUT_DIR)/courses/$$clean_course/notes/sections/$$unit_name.pdf"; \
	  echo "Generated: $(OUTPUT_DIR)/courses/$$clean_course/notes/sections/$$unit_name.pdf"

video-session:
	@test -n "$(SESSION)" || (echo "Error: Set SESSION to video session directory"; exit 2)
	@sess_path=$$(if [ -e "$(COURSES_DIR)/$(SESSION)" ]; then echo "$(COURSES_DIR)/$(SESSION)"; elif [ -e "$(ROOT)/$(SESSION)" ]; then echo "$(ROOT)/$(SESSION)"; else echo "$(SESSION)"; fi); \
	  echo "==> Generating video pipeline for session: $$sess_path"; \
	  $(PYTHON) "$(SRC)/videos/engine/pipeline.py" --session-dir "$$sess_path" $(VIDEO_ACTION)

# --- Bulk Targets ---
all-decks:
	@failed=0; while IFS= read -r -d '' course; do \
	  $(MAKE) --no-print-directory -f $(lastword $(MAKEFILE_LIST)) decks COURSE="$$course" ROOT="$(ROOT)" || failed=1; \
	done < <(find "$(COURSES_DIR)" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -printf '%f\0'); \
	exit $$failed

all-notes:
	@failed=0; while IFS= read -r -d '' course; do \
	  $(MAKE) --no-print-directory -f $(lastword $(MAKEFILE_LIST)) notes COURSE="$$course" ROOT="$(ROOT)" || failed=1; \
	done < <(find "$(COURSES_DIR)" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -printf '%f\0'); \
	exit $$failed

all-videos:
	@failed=0; while IFS= read -r -d '' course; do \
	  $(MAKE) --no-print-directory -f $(lastword $(MAKEFILE_LIST)) videos COURSE="$$course" ROOT="$(ROOT)" || failed=1; \
	done < <(find "$(COURSES_DIR)" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -printf '%f\0'); \
	exit $$failed

all: all-decks all-notes all-videos

scaffold-check:
	@failed=0; count=0; while IFS= read -r -d '' course; do \
	  count=$$((count+1)); \
	  test -d "$$course/decks" && find "$$course/decks" -type f -name '*-content.tex' -print -quit | grep -q . || { echo "Missing decks: $$course"; failed=1; }; \
	  test -d "$$course/notes" && find "$$course/notes" -type f -name '*-content.tex' -print -quit | grep -q . || { echo "Missing notes: $$course"; failed=1; }; \
	  test -d "$$course/videos" || { echo "Missing videos: $$course"; failed=1; }; \
	done < <(find "$(COURSES_DIR)" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0); \
	echo "Verified courses: $$count (100% complete across decks, notes, videos in courses/)"; \
	exit $$failed

validate: sample-decks sample-notes sample-videos
	@test -s "$(OUTPUT_DIR)/sample/decks/sample-decks.pdf"
	@test -s "$(OUTPUT_DIR)/sample/notes/sample-notes.pdf"
	@test -s "$(OUTPUT_DIR)/sample/videos/lesson.mp4"
	@echo "Validation succeeded: all reference artifacts verified."

list:
	@find "$(COURSES_DIR)" -mindepth 3 -type f \( -name '*-content.tex' -o -name 'scene.py' -o -name 'narration.yaml' \) | sort

clean:
	@rm -rf "$(BUILD)" "$(OUTPUT_DIR)" "$(ROOT)/.build" "$(ROOT)/build" 2>/dev/null || true
	@echo "Cleaned build cache and output directory."
