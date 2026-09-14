# Root Makefile forwarding all build targets to the unified src/ publishing engine
SHELL := /bin/bash

SRC_DIR := src

.PHONY: all help sample sample-decks sample-notes sample-videos course decks notes videos session topic concept chapter section video-session all-decks all-notes all-videos scaffold-check validate list clean

help:
	@$(MAKE) -C $(SRC_DIR) help ROOT="$(CURDIR)"

sample:
	@$(MAKE) -C $(SRC_DIR) sample ROOT="$(CURDIR)"

sample-decks:
	@$(MAKE) -C $(SRC_DIR) sample-decks ROOT="$(CURDIR)"

sample-notes:
	@$(MAKE) -C $(SRC_DIR) sample-notes ROOT="$(CURDIR)"

sample-videos:
	@$(MAKE) -C $(SRC_DIR) sample-videos ROOT="$(CURDIR)"

course:
	@$(MAKE) -C $(SRC_DIR) course COURSE="$(COURSE)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

decks:
	@$(MAKE) -C $(SRC_DIR) decks COURSE="$(COURSE)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

notes:
	@$(MAKE) -C $(SRC_DIR) notes COURSE="$(COURSE)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

videos:
	@$(MAKE) -C $(SRC_DIR) videos COURSE="$(COURSE)" ROOT="$(CURDIR)"

session:
	@$(MAKE) -C $(SRC_DIR) session SESSION="$(SESSION)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

topic:
	@$(MAKE) -C $(SRC_DIR) topic TOPIC="$(TOPIC)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

concept:
	@$(MAKE) -C $(SRC_DIR) concept CONCEPT="$(CONCEPT)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

chapter:
	@$(MAKE) -C $(SRC_DIR) chapter CHAPTER="$(CHAPTER)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

section:
	@$(MAKE) -C $(SRC_DIR) section SECTION="$(SECTION)" ROOT="$(CURDIR)" SCIENCE="$(SCIENCE)"

video-session:
	@$(MAKE) -C $(SRC_DIR) video-session SESSION="$(SESSION)" ROOT="$(CURDIR)"

all-decks:
	@$(MAKE) -C $(SRC_DIR) all-decks ROOT="$(CURDIR)"

all-notes:
	@$(MAKE) -C $(SRC_DIR) all-notes ROOT="$(CURDIR)"

all-videos:
	@$(MAKE) -C $(SRC_DIR) all-videos ROOT="$(CURDIR)"

all:
	@$(MAKE) -C $(SRC_DIR) all ROOT="$(CURDIR)"

validate:
	@$(MAKE) -C $(SRC_DIR) validate ROOT="$(CURDIR)"

scaffold-check:
	@$(MAKE) -C $(SRC_DIR) scaffold-check ROOT="$(CURDIR)"

list:
	@$(MAKE) -C $(SRC_DIR) list ROOT="$(CURDIR)"

clean:
	@$(MAKE) -C $(SRC_DIR) clean ROOT="$(CURDIR)"
