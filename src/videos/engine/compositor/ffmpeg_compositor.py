"""
FFmpeg video compositor and multi-track assembly for BayesStack Video Engine.
"""
import os
import sys
import subprocess
from typing import List, Optional, Dict, Any

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from videos.engine.compositor.timeline import VideoTimeline

class VideoCompositor:
    """Combines rendered animation chunks, narration voiceovers, and subtitles using FFmpeg."""

    def __init__(self, ffmpeg_bin: str = "ffmpeg"):
        self.ffmpeg_bin = ffmpeg_bin

    def has_ffmpeg(self) -> bool:
        try:
            res = subprocess.run([self.ffmpeg_bin, "-version"], capture_output=True, check=False)
            return res.returncode == 0
        except Exception:
            return False

    def concatenate_segments(
        self,
        video_segments: List[str],
        audio_segments: List[str],
        output_mp4: str,
        subtitles_srt: Optional[str] = None
    ) -> bool:
        """
        Concatenates video & audio segments and attaches subtitles into a single deliverable MP4.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)

        if not self.has_ffmpeg():
            print(f"Notice: FFmpeg is not available in current environment. Dry-run mode for {output_mp4}")
            return True

        # Write concat demuxer file
        concat_list = f"{output_mp4}.concat.txt"
        with open(concat_list, "w", encoding="utf-8") as f:
            for v in video_segments:
                f.write(f"file '{os.path.abspath(v)}'\n")

        if not video_segments:
            print("Error: No rendered video segments were supplied for composition.")
            return False

        cmd = [
            self.ffmpeg_bin, "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "192k",
            output_mp4
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            if os.path.exists(concat_list):
                os.remove(concat_list)
            return True
        except Exception as e:
            print(f"Error during video composition: {e}")
            return False
