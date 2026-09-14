"""
BayesStack Video Generation Orchestration Pipeline & CLI.
Manages narration parsing, TTS voice synthesis, subtitle alignment, Manim scene execution, and composition.
"""
import os
import sys
import json
import yaml
import argparse
import shutil
from typing import Dict, Any, List, Optional

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from videos.engine.compositor.timeline import TimelineBuilder, VideoTimeline
from videos.engine.compositor.ffmpeg_compositor import VideoCompositor
from videos.engine.subtitles.aligner import SubtitleAligner
from videos.engine.tts.providers import get_tts_provider
from videos.engine.visual.card_renderer import CardVideoRenderer


def load_project_config(project_dir: str) -> Dict[str, Any]:
    """Load optional project settings without making them mandatory."""
    config_path = os.path.join(project_dir, "project.json")
    if not os.path.isfile(config_path):
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not parse {config_path}: {error}") from error


def resolve_ffmpeg() -> Optional[str]:
    """Use a system FFmpeg first, then the wheel-bundled binary if installed."""
    if binary := shutil.which("ffmpeg"):
        return binary
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except (ImportError, RuntimeError):
        return None

def validate_video_project(project_dir: str) -> bool:
    """Validates that a video project has valid narration.yaml and scene.py."""
    narration_path = os.path.join(project_dir, "narration.yaml")
    scene_path = os.path.join(project_dir, "scene.py")

    if not os.path.exists(narration_path):
        print(f"Error: Missing narration.yaml in {project_dir}")
        return False

    try:
        with open(narration_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict) or "scenes" not in data:
                print(f"Error: narration.yaml in {project_dir} must contain a 'scenes' list.")
                return False
    except Exception as e:
        print(f"Error parsing narration.yaml in {project_dir}: {e}")
        return False

    if not os.path.exists(scene_path):
        print(f"Error: Missing scene.py in {project_dir}")
        return False

    # Check python syntax of scene.py
    try:
        with open(scene_path, "r", encoding="utf-8") as f:
            compile(f.read(), scene_path, "exec")
    except Exception as e:
        print(f"Error: Syntax error in {scene_path}: {e}")
        return False

    return True

def synthesize_timeline(timeline: VideoTimeline, out_dir: str, tts_engine: str,
                        voice: Optional[str] = None, speed: float = 1.0) -> List[Any]:
    """Generate one narration stem per segment and attach accurate timeline offsets."""
    provider = get_tts_provider(tts_engine, voice=voice, speed=speed)
    results = []
    offset = 0.0
    for segment in timeline.segments:
        audio_path = os.path.join(out_dir, "audio", f"{segment.scene_id}.mp3")
        result = provider.synthesize(segment.script, audio_path)
        segment.audio_path = result.audio_path
        segment.duration_sec = result.duration_sec
        segment.start_sec = offset
        segment.end_sec = offset + result.duration_sec
        offset = segment.end_sec
        results.append(result)
    timeline.total_duration_sec = offset
    return results


def export_timeline_artifacts(timeline: VideoTimeline, results: List[Any], out_dir: str) -> None:
    """Write the timeline and readable, synchronized subtitles."""
    with open(os.path.join(out_dir, "timeline_plan.json"), "w", encoding="utf-8") as handle:
        json.dump(timeline.to_dict(), handle, indent=2)

    timestamps = []
    for segment, result in zip(timeline.segments, results):
        for word in result.word_timestamps:
            # Providers return local scene timings; subtitle time is session-global.
            word.start_sec += segment.start_sec
            word.end_sec += segment.start_sec
            timestamps.append(word)
    aligner = SubtitleAligner()
    cues = aligner.build_cues_from_timestamps(timestamps)
    aligner.export_srt(cues, os.path.join(out_dir, "subtitles.srt"))
    aligner.export_vtt(cues, os.path.join(out_dir, "subtitles.vtt"))


def plan_session_video(session_dir: str, out_dir: Optional[str] = None,
                       tts_engine: str = "mock") -> VideoTimeline:
    """Build a dry-run timeline, silent timing stems, and subtitles."""
    narration_path = os.path.join(session_dir, "narration.yaml")
    timeline = TimelineBuilder.from_narration_yaml(narration_path)

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        results = synthesize_timeline(timeline, out_dir, tts_engine)
        export_timeline_artifacts(timeline, results, out_dir)

    return timeline


def render_session_video(session_dir: str, out_dir: str, tts_engine: Optional[str] = None) -> str:
    """Render a playable MP4 using Manim-ready content and the card fallback.

    The fallback is deliberately deterministic: every narration segment receives
    a branded visual card, its real narration audio, readable subtitles, and a
    standards-compatible H.264/AAC final MP4. Manim-specific animation can be
    introduced per scene later without changing this authoring contract.
    """
    ffmpeg_bin = resolve_ffmpeg()
    if not ffmpeg_bin:
        raise RuntimeError(
            "FFmpeg is required for --render. Install FFmpeg or add imageio-ffmpeg "
            "to the active Python environment."
        )

    os.makedirs(out_dir, exist_ok=True)
    config = load_project_config(session_dir)
    narration = TimelineBuilder.from_narration_yaml(os.path.join(session_dir, "narration.yaml"))
    tts_config = config.get("tts", {}) if isinstance(config.get("tts", {}), dict) else {}
    narration_meta = narration.metadata
    engine = tts_engine or tts_config.get("engine", "edge-tts")
    voice = tts_config.get("voice") or narration_meta.get("voice")
    speed = float(tts_config.get("speed") or narration_meta.get("speed") or 1.0)
    results = synthesize_timeline(narration, out_dir, engine, voice=voice, speed=speed)
    export_timeline_artifacts(narration, results, out_dir)

    resolution = config.get("resolution", [1920, 1080])
    if resolution != [1920, 1080]:
        print("Notice: the card fallback currently renders at 1920x1080.")
    renderer = CardVideoRenderer(
        ffmpeg_bin=ffmpeg_bin,
        fonts_dir=os.path.join(SRC_DIR, "core", "fonts"),
        fps=int(config.get("fps", 30)),
    )
    rendered_segments = []
    for segment in narration.segments:
        image_path = os.path.join(out_dir, "visuals", f"{segment.scene_id}.png")
        video_path = os.path.join(out_dir, "segments", f"{segment.scene_id}.mp4")
        renderer.render_card(
            course_code=narration.course_code,
            session_title=narration.title,
            scene_title=segment.title,
            narration=segment.script,
            output_path=image_path,
        )
        renderer.render_segment(image_path, segment.audio_path or "", video_path)
        segment.video_path = video_path
        rendered_segments.append(video_path)

    output_mp4 = os.path.join(out_dir, "lesson.mp4")
    compositor = VideoCompositor(ffmpeg_bin=ffmpeg_bin)
    if not compositor.concatenate_segments(rendered_segments, [], output_mp4):
        raise RuntimeError("FFmpeg could not compose the final lesson MP4.")
    return output_mp4

def process_course_videos(course_dir: str, out_dir: str, plan_only: bool = True) -> bool:
    """Discovers and processes all session video directories in a course."""
    videos_dir = os.path.join(course_dir, "videos")
    if not os.path.isdir(videos_dir):
        print(f"No videos directory found in {course_dir}")
        return False

    session_dirs = [
        d for d in os.listdir(videos_dir)
        if os.path.isdir(os.path.join(videos_dir, d)) and not d.startswith(".")
    ]

    if not session_dirs:
        print(f"Notice: No video sessions found in {videos_dir}")
        return True

    success = True
    for s_dir in sorted(session_dirs):
        full_s_dir = os.path.join(videos_dir, s_dir)
        s_out_dir = os.path.join(out_dir, s_dir)
        print(f"  -> Planning video session: {s_dir}")
        try:
            if not validate_video_project(full_s_dir):
                success = False
                continue
            if plan_only:
                plan_session_video(full_s_dir, s_out_dir)
            else:
                render_session_video(full_s_dir, s_out_dir)
        except Exception as e:
            print(f"Error processing session {s_dir}: {e}")
            success = False

    return success

def main():
    parser = argparse.ArgumentParser(description="BayesStack Video Generation Pipeline Engine")
    parser.add_argument("--project", help="Path to single session video project directory")
    parser.add_argument("--session-dir", help="Path to session video directory")
    parser.add_argument("--course-dir", help="Path to course root directory")
    parser.add_argument("--out-dir", "--output-dir", dest="out_dir", default="build/videos",
                        help="Output directory for video deliverables")
    parser.add_argument("--validate", action="store_true", help="Validate project without building")
    parser.add_argument("--plan", action="store_true", help="Generate timeline and subtitle plan")
    parser.add_argument("--render", action="store_true", help="Execute full video render")
    parser.add_argument("--tts", choices=["edge-tts", "mock"], help="Override the project's TTS engine")

    args = parser.parse_args()

    if args.validate and args.project:
        if validate_video_project(args.project):
            print(f"Validation successful for video project: {args.project}")
            sys.exit(0)
        else:
            sys.exit(1)

    if args.project or args.session_dir:
        p_dir = args.project or args.session_dir
        if not validate_video_project(p_dir):
            sys.exit(1)
        if args.render:
            output_mp4 = render_session_video(p_dir, args.out_dir, tts_engine=args.tts)
            print(f"Video session rendered successfully: {output_mp4}")
        else:
            plan_session_video(p_dir, args.out_dir, tts_engine=args.tts or "mock")
            print(f"Video session planned successfully in: {args.out_dir}")
        sys.exit(0)

    if args.course_dir:
        ok = process_course_videos(args.course_dir, args.out_dir, plan_only=not args.render)
        sys.exit(0 if ok else 1)

    parser.print_help()

if __name__ == "__main__":
    main()
