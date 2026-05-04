#!/usr/bin/env python3
"""
agile-web generator
Usage:  python generate.py briefs/my-brief.yaml
        python generate.py briefs/my-brief.yaml --output output/my-page.html
        python generate.py briefs/my-brief.yaml --watch
"""

import argparse
import sys
import time
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


import types


def _to_ns(obj):
    """Convert dicts to SimpleNamespace recursively so Jinja2 dot-access
    works correctly even for keys that shadow dict methods (e.g. 'items')."""
    if isinstance(obj, dict):
        ns = types.SimpleNamespace()
        for k, v in obj.items():
            setattr(ns, k, _to_ns(v))
        return ns
    if isinstance(obj, list):
        return [_to_ns(i) for i in obj]
    return obj


TEMPLATES_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR    = Path(__file__).parent / "output"


def load_brief(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def render(brief: dict, template_name: str = "page.html.j2") -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        keep_trailing_newline=True,
    )
    tmpl = env.get_template(template_name)
    context = {k: _to_ns(v) for k, v in brief.items()}
    return tmpl.render(**context)


def write_output(html: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")


def default_output_path(brief_path: Path) -> Path:
    return OUTPUT_DIR / brief_path.with_suffix(".html").name


def build(brief_path: Path, out_path: Path, quiet: bool = False) -> None:
    brief = load_brief(brief_path)
    html  = render(brief)
    write_output(html, out_path)
    if not quiet:
        print(f"✓  Generated → {out_path}")


def watch(brief_path: Path, out_path: Path) -> None:
    print(f"Watching {brief_path}  (Ctrl+C to stop)")
    last_mtime = None
    try:
        while True:
            mtime = brief_path.stat().st_mtime
            if mtime != last_mtime:
                last_mtime = mtime
                try:
                    build(brief_path, out_path)
                except Exception as exc:
                    print(f"✗  Error: {exc}", file=sys.stderr)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a web page from a YAML brief."
    )
    parser.add_argument("brief", type=Path, help="Path to the YAML brief file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output HTML file (default: output/<brief-name>.html)"
    )
    parser.add_argument(
        "-t", "--template", default="page.html.j2",
        help="Template file name inside templates/ (default: page.html.j2)"
    )
    parser.add_argument(
        "-w", "--watch", action="store_true",
        help="Rebuild automatically when the brief changes"
    )
    args = parser.parse_args()

    brief_path = args.brief
    if not brief_path.exists():
        print(f"Error: brief not found: {brief_path}", file=sys.stderr)
        sys.exit(1)

    out_path = args.output or default_output_path(brief_path)

    if args.watch:
        build(brief_path, out_path)          # initial build
        watch(brief_path, out_path)
    else:
        build(brief_path, out_path)


if __name__ == "__main__":
    main()
