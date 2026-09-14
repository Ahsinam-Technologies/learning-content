#!/usr/bin/env python3
"""
render_wrapper.py - Generates LaTeX compilation wrappers for courses, sessions, topics, chapters, and sections.
Ensures clean escaping of LaTeX special characters (&, %, _, #) and discovers content modules automatically.
Supports courses placed within courses/ directory or at root.
"""

import os
import sys
import re

def escape_latex(s):
    # Escape special characters for LaTeX text
    # Avoid double escaping
    replacements = [
        ("&", r"\&"),
        ("%", r"\%"),
        ("#", r"\#"),
        ("_", r"\_"),
    ]
    res = s
    for orig, rep in replacements:
        # Match only unescaped
        res = re.sub(r'(?<!\\)' + re.escape(orig), rep, res)
    return res

def parse_course_info(course_str):
    clean_str = os.path.basename(course_str)
    parts = clean_str.split(" - ", 1)
    code = parts[0].strip()
    name = parts[1].strip() if len(parts) > 1 else clean_str
    return code, name

def resolve_course_dir(root, course):
    """Resolves full course directory path and clean course name."""
    c1 = os.path.join(root, "courses", course)
    if os.path.isdir(c1):
        return c1, os.path.basename(course)
    c2 = os.path.join(root, course)
    if os.path.isdir(c2):
        return c2, os.path.basename(course)
    if course.startswith("courses" + os.sep) or course.startswith("courses/"):
        c3 = os.path.join(root, course)
        if os.path.isdir(c3):
            return c3, os.path.basename(course)
    return c1, os.path.basename(course)

def render_decks_wrapper(root, course, build_dir, science=False):
    c_dir, clean_course_name = resolve_course_dir(root, course)
    decks_dir = os.path.join(c_dir, "decks")
    if not os.path.exists(decks_dir):
        raise FileNotFoundError(f"Decks folder not found: {decks_dir}")
        
    code, name = parse_course_info(clean_course_name)
    esc_code = escape_latex(code)
    esc_name = escape_latex(name)
    
    # Find all session content files
    sessions = []
    for entry in sorted(os.listdir(decks_dir)):
        sess_dir = os.path.join(decks_dir, entry)
        if os.path.isdir(sess_dir) and entry.startswith("session-"):
            content_file = os.path.join(sess_dir, f"{entry}-content.tex")
            if os.path.exists(content_file):
                # Try to read session metadata
                with open(content_file, "r", encoding="utf-8") as f:
                    c_text = f.read()
                m = re.search(r"\\SessionDivider\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}", c_text)
                if m:
                    num, s_title, s_outcome = m.group(1), m.group(2), m.group(3)
                else:
                    m2 = re.search(r"\\ChapterDivider\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}", c_text)
                    if m2:
                        num, s_title, s_outcome = m2.group(1), m2.group(2), m2.group(3)
                    else:
                        num = entry.split("-")[1]
                        s_title = entry.replace("-", " ").title()
                        s_outcome = "Session learning outcome."
                sessions.append({
                    "dir": entry,
                    "file": f"{entry}-content.tex",
                    "num": num,
                    "title": s_title,
                    "outcome": s_outcome
                })
                
    out_dir = os.path.join(build_dir, "courses", clean_course_name, "decks")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "course-slides.tex")
    
    sci_opt = "[science]" if science else ""
    
    lines = [
        r"\documentclass[aspectratio=169,10pt]{beamer}",
        r"\usepackage{import}",
        f"\\usepackage{sci_opt}{{bayesstackslides}}",
        f"\\CourseMetadata{{{esc_code}}}{{{esc_name}}}{{In-Class Lecture Slides}}",
        r"\author{BayesStack}",
        r"\date{}",
        r"\begin{document}",
        f"\\BayesCourseTitleSlide{{{esc_name}}}{{In-Class Lecture Slides and Topical Agendas}}",
        r"\CourseSessionMapSlide{"
    ]
    for s in sessions:
        lines.append(f"  \\SessionEntry{{{s['num']}}}{{{s['title']}}}{{{s['outcome']}}}")
    lines.append(r"}")
    for s in sessions:
        lines.append(f"\\import{{decks/{s['dir']}/}}{{{s['file']}}}")
    lines.append(r"\end{document}")
    lines.append("")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_file

def render_notes_wrapper(root, course, build_dir, science=False):
    c_dir, clean_course_name = resolve_course_dir(root, course)
    notes_dir = os.path.join(c_dir, "notes")
    if not os.path.exists(notes_dir):
        raise FileNotFoundError(f"Notes folder not found: {notes_dir}")
        
    code, name = parse_course_info(clean_course_name)
    esc_code = escape_latex(code)
    esc_name = escape_latex(name)
    
    # Find all chapter content files
    chapters = []
    for entry in sorted(os.listdir(notes_dir)):
        chap_dir = os.path.join(notes_dir, entry)
        if os.path.isdir(chap_dir) and entry.startswith("chapter-"):
            content_file = os.path.join(chap_dir, f"{entry}-content.tex")
            if os.path.exists(content_file):
                chapters.append({
                    "dir": entry,
                    "file": f"{entry}-content.tex"
                })
                
    out_dir = os.path.join(build_dir, "courses", clean_course_name, "notes")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "course-notes.tex")
    
    sci_opt = "[science]" if science else ""
    
    lines = [
        r"\documentclass[10pt,letterpaper,twoside,openright,twocolumn]{book}",
        r"\usepackage{import}",
        r"\usepackage{subfiles}",
        f"\\usepackage{sci_opt}{{bayesstacknotes}}",
        f"\\CourseMetadata{{{esc_code}}}{{{esc_name}}}{{Comprehensive Reading Notes \\& Reference Manual}}",
        r"\author{BayesStack Academic Editorial Board}",
        r"\date{}",
        r"\begin{document}",
        r"\frontmatter",
        r"\onecolumn",
        r"\BayesBookCover",
        r"\BayesCopyrightPage",
        r"\BayesOpeningPage",
        r"\cleardoublepage",
        r"\tableofcontents",
        r"\cleardoublepage",
        r"\twocolumn",
        r"\mainmatter",
    ]
    for ch in chapters:
        lines.append(f"\\import{{notes/{ch['dir']}/}}{{{ch['file']}}}")
    lines.extend([
        r"\backmatter",
        r"\onecolumn",
        r"\BayesBackCover",
        r"\end{document}",
        ""
    ])
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_file

def render_unit_wrapper(mode, root, unit_path, build_dir, science=False):
    # unit_path can be relative to root or absolute
    full_path = os.path.abspath(os.path.join(root, unit_path) if not os.path.isabs(unit_path) else unit_path)
    if not os.path.exists(full_path):
        alt_path = os.path.abspath(os.path.join(root, "courses", unit_path))
        if os.path.exists(alt_path):
            full_path = alt_path

    if os.path.isdir(full_path):
        candidates = [f for f in os.listdir(full_path) if f.endswith("-content.tex")]
        if not candidates:
            raise FileNotFoundError(f"No content file found in {full_path}")
        content_path = os.path.join(full_path, sorted(candidates)[0])
    else:
        content_path = full_path
        
    if not os.path.exists(content_path):
        raise FileNotFoundError(f"Content file not found: {content_path}")
        
    # Find enclosing course directory
    curr = os.path.dirname(content_path)
    course_path = None
    while curr and curr != root and curr != os.path.dirname(root):
        if os.path.isdir(os.path.join(curr, "decks")) or os.path.isdir(os.path.join(curr, "notes")):
            course_path = curr
            break
        curr = os.path.dirname(curr)

    if not course_path:
        course_path = os.path.dirname(os.path.dirname(content_path))

    clean_course_name = os.path.basename(course_path)
    code, name = parse_course_info(clean_course_name)
    esc_code = escape_latex(code)
    esc_name = escape_latex(name)
    sci_opt = "[science]" if science else ""
    
    content_dir = os.path.dirname(content_path)
    content_file = os.path.basename(content_path)
    rel_content_dir = os.path.relpath(content_dir, course_path)
    
    if mode in ("session", "topic"):
        out_dir = os.path.join(build_dir, "courses", clean_course_name, "decks", "units")
        os.makedirs(out_dir, exist_ok=True)
        unit_name = os.path.splitext(content_file)[0].replace("-content", "")
        out_file = os.path.join(out_dir, f"{unit_name}.tex")
        lines = [
            r"\documentclass[aspectratio=169,10pt]{beamer}",
            r"\usepackage{import}",
            f"\\usepackage{sci_opt}{{bayesstackslides}}",
            f"\\CourseMetadata{{{esc_code}}}{{{esc_name}}}{{{unit_name.replace('-', ' ').title()}}}",
            r"\author{BayesStack}",
            r"\date{}",
            r"\begin{document}",
            f"\\import{{{rel_content_dir}/}}{{{content_file}}}",
            r"\end{document}"
        ]
    else: # chapter or section
        out_dir = os.path.join(build_dir, "courses", clean_course_name, "notes", "units")
        os.makedirs(out_dir, exist_ok=True)
        unit_name = os.path.splitext(content_file)[0].replace("-content", "")
        out_file = os.path.join(out_dir, f"{unit_name}.tex")
        lines = [
            r"\documentclass[10pt,letterpaper,twoside,openright,twocolumn]{book}",
            r"\usepackage{import}",
            r"\usepackage{subfiles}",
            f"\\usepackage{sci_opt}{{bayesstacknotes}}",
            f"\\CourseMetadata{{{esc_code}}}{{{esc_name}}}{{{unit_name.replace('-', ' ').title()}}}",
            r"\author{BayesStack Academic Editorial Board}",
            r"\date{}",
            r"\begin{document}",
            r"\twocolumn",
            f"\\import{{{rel_content_dir}/}}{{{content_file}}}",
            r"\end{document}"
        ]
        
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_file

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: render_wrapper.py <mode: decks|notes|session|topic|chapter|section> <root> <target> <build_dir> [science: 0|1]")
        sys.exit(1)
        
    mode = sys.argv[1].lower()
    root = os.path.abspath(sys.argv[2])
    target = sys.argv[3]
    build_dir = os.path.abspath(sys.argv[4])
    science = len(sys.argv) > 5 and sys.argv[5] in ("1", "true", "yes")
    
    if mode == "decks":
        out = render_decks_wrapper(root, target, build_dir, science)
    elif mode == "notes":
        out = render_notes_wrapper(root, target, build_dir, science)
    elif mode in ("session", "topic", "chapter", "section"):
        out = render_unit_wrapper(mode, root, target, build_dir, science)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(2)
        
    print(out)
