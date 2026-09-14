"""Dependency-light visual fallback for playable lesson videos.

Manim remains the preferred renderer for bespoke animation.  This renderer
keeps the pipeline usable on author machines without Manim by turning each
narration segment into a branded motion hold with the corresponding audio.
"""
from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class CardVideoRenderer:
    WIDTH = 1920
    HEIGHT = 1080
    BACKGROUND = "#091A18"
    TEAL = "#0B6763"
    PALE = "#E4F2EF"
    WHITE = "#FFFFFF"
    MUTED = "#B8D3CE"

    def __init__(self, ffmpeg_bin: str, fonts_dir: str, fps: int = 30):
        self.ffmpeg_bin = ffmpeg_bin
        self.fonts_dir = Path(fonts_dir)
        self.fps = fps

    def _font(self, filename: str, size: int):
        path = self.fonts_dir / filename
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
        return ImageFont.load_default()

    def render_card(self, *, course_code: str, session_title: str, scene_title: str,
                    narration: str, output_path: str) -> None:
        """Create one 16:9 branded visual card for a narration segment."""
        image = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.BACKGROUND)
        draw = ImageDraw.Draw(image)
        outfit_bold = self._font("Outfit-SemiBold.ttf", 70)
        outfit_small = self._font("Outfit-SemiBold.ttf", 32)
        inter = self._font("Inter-Regular.ttf", 38)
        inter_small = self._font("Inter-Regular.ttf", 28)

        draw.rectangle((0, 0, 28, self.HEIGHT), fill=self.TEAL)
        draw.rectangle((130, 132, 560, 142), fill=self.TEAL)
        draw.text((130, 70), course_code.upper(), font=outfit_small, fill=self.PALE)
        draw.text((130, 185), session_title, font=outfit_bold, fill=self.WHITE)
        draw.text((130, 300), scene_title, font=outfit_bold, fill=self.PALE)

        card_left, card_top, card_right, card_bottom = 130, 420, 1790, 890
        draw.rounded_rectangle(
            (card_left, card_top, card_right, card_bottom), radius=30,
            fill="#123333", outline=self.TEAL, width=3,
        )
        wrapped = textwrap.wrap(" ".join(narration.split()), width=72)
        y = card_top + 54
        for line in wrapped[:7]:
            draw.text((card_left + 55, y), line, font=inter, fill=self.WHITE)
            y += 56
        if len(wrapped) > 7:
            draw.text((card_left + 55, y), "…", font=inter, fill=self.MUTED)

        draw.text((130, 970), "BayesStack Learning OS  •  Self-paced lesson", font=inter_small, fill=self.MUTED)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        image.save(output_path, quality=95)

    def render_segment(self, image_path: str, audio_path: str, output_path: str) -> None:
        """Mux a still card and its narration into a standards-compatible MP4."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        command = [
            self.ffmpeg_bin, "-y", "-loop", "1", "-i", image_path, "-i", audio_path,
            "-c:v", "libx264", "-tune", "stillimage", "-r", str(self.fps),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-movflags", "+faststart", output_path,
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg could not render {output_path}: {result.stderr[-800:]}")
