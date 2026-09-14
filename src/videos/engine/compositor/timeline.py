"""
Timeline model and video composition planning engine for BayesStack.
Synchronizes narration cues, visual scene keyframes, background audio, and subtitles.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import os
import json
import yaml

@dataclass
class SceneSegment:
    scene_id: str
    title: str
    script: str
    visual_action: str
    duration_sec: float = 0.0
    start_sec: float = 0.0
    end_sec: float = 0.0
    audio_path: Optional[str] = None
    video_path: Optional[str] = None

@dataclass
class VideoTimeline:
    title: str
    course_code: str
    session_num: str
    total_duration_sec: float = 0.0
    segments: List[SceneSegment] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "course_code": self.course_code,
            "session_num": self.session_num,
            "total_duration_sec": round(self.total_duration_sec, 2),
            "segments": [
                {
                    "scene_id": s.scene_id,
                    "title": s.title,
                    "script": s.script,
                    "visual_action": s.visual_action,
                    "duration_sec": round(s.duration_sec, 2),
                    "start_sec": round(s.start_sec, 2),
                    "end_sec": round(s.end_sec, 2),
                    "audio_path": s.audio_path,
                    "video_path": s.video_path
                }
                for s in self.segments
            ],
            "metadata": self.metadata
        }

class TimelineBuilder:
    """Builds a synchronized VideoTimeline from a narration YAML and scene definition."""

    @staticmethod
    def from_narration_yaml(yaml_path: str) -> VideoTimeline:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        title = data.get("title", "Untitled Session")
        course_code = data.get("course_code", "COURSE 101")
        session_num = str(data.get("session", "01"))
        scenes_data = data.get("scenes", [])

        timeline = VideoTimeline(
            title=title,
            course_code=course_code,
            session_num=session_num,
            metadata=data.get("metadata", {})
        )

        current_time = 0.0
        for idx, sc in enumerate(scenes_data, 1):
            s_id = sc.get("id", f"scene_{idx:02d}")
            s_title = sc.get("title", f"Scene {idx}")
            script = sc.get("narration", "")
            action = sc.get("visual", "")

            # Estimate duration based on word count (~2.5 words per second)
            word_count = len(script.split())
            dur = max(2.5, word_count / 2.5 if word_count > 0 else 3.0)

            segment = SceneSegment(
                scene_id=s_id,
                title=s_title,
                script=script,
                visual_action=action,
                duration_sec=dur,
                start_sec=current_time,
                end_sec=current_time + dur
            )
            timeline.segments.append(segment)
            current_time += dur

        timeline.total_duration_sec = current_time
        return timeline
