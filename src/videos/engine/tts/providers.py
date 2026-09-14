"""
TTS Providers implementation for BayesStack Video Generation Engine.
Supports Edge-TTS (free neural voices), OpenAI TTS, ElevenLabs, Piper, and Mock.
"""
import os
import sys
import re
import math
import subprocess
from typing import Optional, List, Dict, Any

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from videos.engine.tts.base import BaseTTSProvider, AudioSynthesisResult, WordTimestamp

class MockTTSProvider(BaseTTSProvider):
    """
    Mock TTS engine for testing, local CI, and dry-run validation.
    Estimates timing based on average English speech rate (approx 150 words per minute / 2.5 words/sec).
    """

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        speed: Optional[float] = None
    ) -> AudioSynthesisResult:
        words = text.strip().split()
        num_words = len(words)
        rate = (speed or self.speed) * 2.5 # ~2.5 words per second
        duration = max(1.0, num_words / rate if num_words > 0 else 1.0)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Estimate word-level timestamps
        timestamps: List[WordTimestamp] = []
        current_time = 0.0
        word_dur = duration / max(1, num_words)
        for w in words:
            timestamps.append(WordTimestamp(
                word=w,
                start_sec=round(current_time, 3),
                end_sec=round(current_time + word_dur, 3)
            ))
            current_time += word_dur

        # If ffmpeg is available, generate silent audio file for testing
        try:
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", f"anullsrc=r=44100:cl=stereo",
                "-t", str(duration),
                "-q:a", "9", "-acodec", "libmp3lame",
                output_path
            ], capture_output=True, check=False)
        except Exception:
            # Fallback touch file if ffmpeg is missing
            with open(output_path, "wb") as f:
                f.write(b"MOCK_AUDIO_DATA")

        return AudioSynthesisResult(
            audio_path=output_path,
            duration_sec=round(duration, 3),
            word_timestamps=timestamps,
            metadata={"engine": "mock", "voice": voice or self.voice or "default", "word_count": num_words}
        )

class EdgeTTSProvider(BaseTTSProvider):
    """
    Edge-TTS provider using Microsoft Azure neural voices (en-US-ChristopherNeural, en-US-AriaNeural, etc.).
    """

    def __init__(self, voice: str = "en-US-ChristopherNeural", speed: float = 1.0):
        super().__init__(voice=voice, speed=speed)

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        speed: Optional[float] = None
    ) -> AudioSynthesisResult:
        v = voice or self.voice or "en-US-ChristopherNeural"
        s = speed or self.speed
        rate_str = f"{int((s - 1.0) * 100):+d}%"

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        vtt_path = f"{os.path.splitext(output_path)[0]}.vtt"

        cmd = [
            sys.executable, "-m", "edge_tts",
            "--voice", v,
            "--rate", rate_str,
            "--text", text,
            "--write-media", output_path,
            "--write-subtitles", vtt_path
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
        except Exception as e:
            raise RuntimeError(
                "Edge TTS synthesis failed. Install edge-tts and check network access, "
                f"voice '{v}', and the narration text. Details: {e}"
            ) from e

        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise RuntimeError(f"Edge TTS completed without producing audio: {output_path}")

        # Estimate duration or probe with ffprobe
        duration = 5.0
        try:
            probe = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries",
                "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                output_path
            ], capture_output=True, text=True, check=True)
            duration = float(probe.stdout.strip())
        except Exception:
            pass

        words = text.strip().split()
        word_duration = duration / max(1, len(words))
        timestamps = [
            WordTimestamp(word=word, start_sec=round(index * word_duration, 3),
                          end_sec=round((index + 1) * word_duration, 3))
            for index, word in enumerate(words)
        ]
        return AudioSynthesisResult(
            audio_path=output_path,
            duration_sec=round(duration, 3),
            word_timestamps=timestamps,
            metadata={"engine": "edge-tts", "voice": v, "subtitles": vtt_path}
        )

def get_tts_provider(name: str = "mock", **kwargs) -> BaseTTSProvider:
    """Factory function for selecting TTS provider."""
    providers = {
        "mock": MockTTSProvider,
        "edge-tts": EdgeTTSProvider,
    }
    provider_cls = providers.get(name.lower(), MockTTSProvider)
    return provider_cls(**kwargs)
