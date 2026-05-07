"""
svg_to_png.py — Convert all SVGs in a post's images/ folder to PNG.

Usage:
    python svg_to_png.py                  # lists available posts
    python svg_to_png.py lqc              # converts posts/lqc/images/
    python svg_to_png.py bell             # converts posts/bell/images/
    python svg_to_png.py fsl              # converts posts/fsl/images/
    python svg_to_png.py --all            # converts every post folder
    python svg_to_png.py lqc --scale 3   # 3x resolution (default: 2)

Output: PNG files saved alongside SVGs in the same images/ folder.
        e.g. banner.svg  →  banner.png  (2400x1260 at scale=2)

Platform notes:
    Medium    — accepts SVG directly; PNGs optional
    Substack  — requires PNG; use this script before uploading

Rendering backend:
    Uses headless Google Chrome for pixel-perfect rendering — all Unicode
    glyphs (Z256 subscripts, Greek letters, math symbols, checkmarks) render
    exactly as they appear in a browser. Falls back to cairosvg if Chrome
    is not found.
"""

import re
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

POSTS_DIR = Path(__file__).parent

CHROME_PATHS = [    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]


def find_chrome() -> str | None:
    """Return path to Chrome/Chromium executable, or None."""
    for p in CHROME_PATHS:
        if Path(p).exists():
            return p
    return shutil.which("google-chrome") or shutil.which("chromium")


# ── Chrome headless rendering ─────────────────────────────────────────────────


def _parse_svg_dimensions(svg_path: Path) -> tuple[int, int]:
    """Extract width/height from SVG viewBox or width/height attributes."""
    import xml.etree.ElementTree as ET
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}
    # Try width/height attributes first
    w = root.get("width")
    h = root.get("height")
    if w and h:
        try:
            return int(float(w)), int(float(h))
        except ValueError:
            pass
    # Try viewBox
    vb = root.get("viewBox")
    if vb:
        parts = vb.split()
        if len(parts) == 4:
            try:
                return int(float(parts[2])), int(float(parts[3]))
            except ValueError:
                pass
    return 900, 500  # fallback


def convert_svg_chrome(svg_path: Path, scale: int, chrome_exe: str) -> Path:
    """Render SVG to PNG via headless Chrome — full Unicode support, exact scale."""
    png_path = svg_path.with_suffix(".png")
    w, h = _parse_svg_dimensions(svg_path)
    # Navigate Chrome directly to the SVG file.
    # --force-device-scale-factor makes Chrome emit a (w*scale) × (h*scale) screenshot.
    cmd = [
        chrome_exe,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--window-size={w},{h}",
        f"--force-device-scale-factor={scale}",
        f"--screenshot={png_path}",
        "--hide-scrollbars",
        svg_path.as_uri(),
    ]
    subprocess.run(cmd, capture_output=True, timeout=30)
    return png_path


# ── cairosvg fallback ─────────────────────────────────────────────────────────

def convert_svg_cairo(svg_path: Path, scale: int) -> Path:
    """Fallback: convert via cairosvg (limited Unicode support)."""
    try:
        import cairosvg
    except ImportError:
        sys.exit("Neither Chrome nor cairosvg found. Install cairosvg: pip install cairosvg")
    png_path = svg_path.with_suffix(".png")
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=scale)
    return png_path


# ── Dispatcher ────────────────────────────────────────────────────────────────

def convert_svg(svg_path: Path, scale: int, chrome_exe: str | None) -> Path:
    if chrome_exe:
        return convert_svg_chrome(svg_path, scale, chrome_exe)
    return convert_svg_cairo(svg_path, scale)


def convert_post(post_name: str, scale: int, chrome_exe: str | None) -> None:
    """Convert all SVGs inside posts/<post_name>/images/."""
    images_dir = POSTS_DIR / post_name / "images"
    if not images_dir.exists():
        print(f"  [skip] No images/ folder found: {images_dir}")
        return

    svgs = sorted(images_dir.glob("*.svg"))
    if not svgs:
        print(f"  [skip] No SVG files in: {images_dir}")
        return

    backend = "Chrome" if chrome_exe else "cairosvg (fallback)"
    print(f"\nPost: {post_name}  ({len(svgs)} SVG files, scale={scale}x, via {backend})")
    for svg in svgs:
        png = convert_svg(svg, scale, chrome_exe)
        kb = png.stat().st_size // 1024
        print(f"  ✓  {svg.name:35s}  →  {png.name}  ({kb} KB)")


def list_post_folders() -> list[str]:
    return [
        d.name
        for d in POSTS_DIR.iterdir()
        if d.is_dir() and (d / "images").exists()
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert SVG post images to PNG for Substack/Medium."
    )
    parser.add_argument(
        "post",
        nargs="?",
        help="Post folder name (e.g. lqc, bell, fsl). Omit to list available posts.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all post folders.",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=2,
        help="Resolution multiplier (default: 2 = 2x / retina).",
    )
    args = parser.parse_args()

    chrome_exe = find_chrome()
    if chrome_exe:
        print(f"Rendering backend: Chrome ({chrome_exe})")
    else:
        print("Rendering backend: cairosvg (Chrome not found — Unicode glyphs may be missing)")

    if args.all:
        posts = list_post_folders()
        if not posts:
            print("No post folders with images/ found.")
            return
        for post in posts:
            convert_post(post, args.scale, chrome_exe)
        print("\nDone.")
        return

    if args.post:
        convert_post(args.post, args.scale, chrome_exe)
        print("\nDone.")
        return

    # No argument — list available posts
    posts = list_post_folders()
    if not posts:
        print("No post folders with images/ found under:", POSTS_DIR)
    else:
        print("Available posts with images/:")
        for p in posts:
            svgs = list((POSTS_DIR / p / "images").glob("*.svg"))
            print(f"  {p:<20s} ({len(svgs)} SVGs)")
        print(
            "\nUsage examples:\n"
            "  python svg_to_png.py lqc\n"
            "  python svg_to_png.py --all\n"
            "  python svg_to_png.py lqc --scale 3"
        )


if __name__ == "__main__":
    main()
