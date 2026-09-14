"""
Base Text-to-Speech (TTS) Provider Abstraction for BayesStack Video Engine.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import json
import os

@dataclass
class WordTimestamp:
    word: str
    start_sec: float
    end_sec: float
    confidence: float = 1.0

@dataclass
class AudioSynthesisResult:
    audio_path: str
    duration_sec: float
    sample_rate: int = 44100
    word_timestamps: List[WordTimestamp] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audio_path": self.audio_path,
            "duration_sec": self.duration_sec,
            "sample_rate": self.sample_rate,
            "word_timestamps": [
                {
                    "word": wt.word,
                    "start_sec": wt.start_sec,
                    "end_sec": wt.end_sec,
                    "confidence": wt.confidence
                }
                for wt in self.word_timestamps
            ],
            "metadata": self.metadata
        }

class BaseTTSProvider(ABC):
    """Abstract interface for voiceover generation engines."""

    def __init__(self, voice: Optional[str] = None, speed: float = 1.0):
        self.voice = voice
        self.speed = speed

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        speed: Optional[float] = None
    ) -> AudioSynthesisResult:
        """
        Synthesize spoken audio from text and return audio path with timing metadata.
        """
        pass
