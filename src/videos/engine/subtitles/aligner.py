"""
Subtitle generator and timestamp synchronization engine for BayesStack Video Engine.
"""
import os
import sys
import re
from typing import List, Dict, Any, Optional

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from videos.engine.tts.base import WordTimestamp

def format_timestamp_srt(seconds: float) -> str:
    """Format seconds into SRT timestamp format: HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def format_timestamp_vtt(seconds: float) -> str:
    """Format seconds into VTT timestamp format: HH:MM:SS.mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{millis:03d}"

class SubtitleCue:
    def __init__(self, index: int, start_sec: float, end_sec: float, text: str):
        self.index = index
        self.start_sec = start_sec
        self.end_sec = end_sec
        self.text = text

    def to_srt(self) -> str:
        return f"{self.index}\n{format_timestamp_srt(self.start_sec)} --> {format_timestamp_srt(self.end_sec)}\n{self.text}\n"

    def to_vtt(self) -> str:
        return f"{format_timestamp_vtt(self.start_sec)} --> {format_timestamp_vtt(self.end_sec)}\n{self.text}\n"

class SubtitleAligner:
    """
    Groups words or sentences into readable subtitle cues (typically 32-42 chars per line, max 2 lines).
    """

    def __init__(self, max_chars_per_line: int = 38, max_lines_per_cue: int = 2):
        self.max_chars_per_line = max_chars_per_line
        self.max_lines_per_cue = max_lines_per_cue

    def build_cues_from_timestamps(
        self,
        word_timestamps: List[WordTimestamp],
        start_offset_sec: float = 0.0
    ) -> List[SubtitleCue]:
        if not word_timestamps:
            return []

        cues: List[SubtitleCue] = []
        current_words: List[WordTimestamp] = []
        current_len = 0
        cue_idx = 1

        for wt in word_timestamps:
            current_words.append(wt)
            current_len += len(wt.word) + 1

            # Break cue on natural punctuation (period, comma, question mark) or when length exceeds budget
            is_punct = bool(re.search(r'[.,!?;:]$', wt.word))
            if current_len >= self.max_chars_per_line or is_punct:
                text = " ".join(w.word for w in current_words)
                c_start = current_words[0].start_sec + start_offset_sec
                c_end = current_words[-1].end_sec + start_offset_sec
                cues.append(SubtitleCue(cue_idx, c_start, c_end, text))
                cue_idx += 1
                current_words = []
                current_len = 0

        if current_words:
            text = " ".join(w.word for w in current_words)
            c_start = current_words[0].start_sec + start_offset_sec
            c_end = current_words[-1].end_sec + start_offset_sec
            cues.append(SubtitleCue(cue_idx, c_start, c_end, text))

        return cues

    def export_srt(self, cues: List[SubtitleCue], output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            for cue in cues:
                f.write(cue.to_srt() + "\n")

    def export_vtt(self, cues: List[SubtitleCue], output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for cue in cues:
                f.write(cue.to_vtt() + "\n")
