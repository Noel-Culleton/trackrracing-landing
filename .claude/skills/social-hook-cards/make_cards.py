#!/usr/bin/env python3
"""
Render social hook cards (text-on-image) from a JSON spec, using headless Chromium.

    python3 make_cards.py cards.json ./out

Why HTML -> Chromium rather than an image library: real web typography, webfonts,
flexbox, gradients and CSS you can iterate on quickly — and no Pillow dependency,
which is frequently absent.

Spec format (JSON): {"size": "square", "brand": "...", "theme": {...}, "cards": [...]}
See SKILL.md for the full contract.
"""
import json, os, subprocess, sys, shutil, urllib.request, glob

SIZES = {            # w, h
    "square":    (1080, 1080),   # safest default; works in every feed
    "portrait":  (1080, 1350),   # 4:5 — most mobile feed real estate
    "landscape": (1200, 630),    # link previews / OG images
    "story":     (1080, 1920),
}

CHROME_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("google-chrome") or "",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    for p in glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome"):
        return p
    sys.exit("No Chromium found. Set PLAYWRIGHT_BROWSERS_PATH or install chromium.")


_DELTA = None


def viewport_delta(chrome):
    """How much taller --window-size must be than the layout viewport.

    Headless Chromium reserves vertical space, so --window-size=1080,1080 lays
    out in a viewport of only ~993px. Anything bottom-anchored on a full-height
    canvas then falls outside the visible area and is silently clipped. Measure
    the gap once and compensate, rather than hardcoding a version-specific number.
    """
    global _DELTA
    if _DELTA is not None:
        return _DELTA
    import tempfile
    probe = os.path.join(tempfile.gettempdir(), "_hookcard_probe.html")
    # Marker is concatenated at runtime so the literal string does not also
    # appear in the script source, which --dump-dom echoes back and which would
    # otherwise be what we parse.
    open(probe, "w").write(
        "<body><script>document.write('V'+'P='+window.innerHeight+'|')</script></body>")
    r = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--window-size=800,1000",
         "--virtual-time-budget=2000", "--dump-dom", "file://" + probe],
        capture_output=True, text=True)
    try:
        vh = int(r.stdout.split("VP=")[1].split("|")[0].strip())
        _DELTA = max(0, 1000 - vh)
        print(f"  viewport probe: asked 1000px, got {vh}px -> compensating {_DELTA}px")
    except Exception:
        _DELTA = 0
        print("  ! viewport probe failed; bottom-anchored elements may clip")
    return _DELTA


def ensure_fonts(families):
    """Install Google fonts locally so Chromium can use them offline.

    Chromium's own network fetch of fonts.googleapis.com often fails behind an
    agent proxy even when curl/urllib succeed, so we download the TTFs and drop
    them in ~/.fonts instead of linking a stylesheet.
    """
    if not families:
        return
    fontdir = os.path.expanduser("~/.fonts")
    os.makedirs(fontdir, exist_ok=True)
    have = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout
    missing = [f for f in families if f.split(":")[0] not in have]
    if not missing:
        return
    spec = "&".join("family=" + f.replace(" ", "+") for f in missing)
    url = f"https://fonts.googleapis.com/css2?{spec}&display=swap"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        css = urllib.request.urlopen(req, timeout=30).read().decode()
    except Exception as e:
        print(f"  ! could not fetch fonts ({e}); falling back to system fonts")
        return
    urls, seen = [], set()
    for chunk in css.split("url(")[1:]:
        u = chunk.split(")")[0].strip("'\"")
        if u.startswith("http") and u not in seen:
            seen.add(u)
            urls.append(u)
    for i, u in enumerate(urls):
        ext = u.rsplit(".", 1)[-1].split("?")[0]
        dest = os.path.join(fontdir, f"hookcard_{i}.{ext}")
        try:
            urllib.request.urlretrieve(u, dest)
        except Exception:
            pass
    subprocess.run(["fc-cache", "-f"], capture_output=True)
    print(f"  installed {len(urls)} font file(s)")


PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
/* 100vh, not a fixed pixel height. The screenshot is always as tall as the
   window, but headless Chromium's layout viewport is ~87px shorter than the
   window it is given. Anchoring to the viewport keeps every element inside the
   painted area; the unused strip at the foot just carries the background. */
html,body{{width:100%;height:100vh;overflow:hidden}}
body{{font-family:{body_font};background:{bg};color:{fg};
  display:flex;flex-direction:column;padding:{pad}px}}
.stage{{flex:1;display:flex;flex-direction:column;justify-content:{justify};min-height:0}}
.kicker{{font-size:{kicker_size}px;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase;color:{accent};margin-bottom:34px}}
h1{{font-family:{display_font};font-weight:700;line-height:1.02;
  letter-spacing:-.02em;font-size:{h1}px;color:{fg}}}
.sub{{font-size:{sub_size}px;line-height:1.45;color:{muted};margin-top:34px;max-width:{subw}px}}
.brand{{flex:none;display:flex;align-items:center;gap:14px;
  font-size:{brand_size}px;font-weight:700;color:{fg};opacity:.92}}
.brand .dot{{width:{dot}px;height:{dot}px;border-radius:50%;background:{accent};flex:none}}
{extra}
</style></head><body>
<div class="stage">{content}</div>
<div class="brand"><span class="dot"></span>{brand}</div>
</body></html>"""


def build(spec, outdir):
    w, h = SIZES[spec.get("size", "square")]
    t = spec.get("theme", {})
    chrome = find_chrome()
    fonts = spec.get("google_fonts", [])
    ensure_fonts(fonts)
    os.makedirs(outdir, exist_ok=True)

    # Scale type off the canvas so one spec works at any size.
    k = h / 1080.0
    made = []
    for i, c in enumerate(spec["cards"], 1):
        name = c.get("name") or f"card-{i:02d}"
        html = PAGE.format(
            w=w, h=h,
            pad=int(c.get("pad", t.get("pad", 76)) * k),
            bg=c.get("bg", t.get("bg", "#111")),
            fg=c.get("fg", t.get("fg", "#fff")),
            accent=c.get("accent", t.get("accent", "#8FC4A8")),
            muted=c.get("muted", t.get("muted", "rgba(255,255,255,.80)")),
            justify=c.get("justify", "center"),
            body_font=t.get("body_font", "'Inter',sans-serif"),
            display_font=t.get("display_font", "'Fraunces',Georgia,serif"),
            h1=int(c.get("h1", 92) * k),
            kicker_size=int(c.get("kicker_size", 26) * k),
            sub_size=int(c.get("sub_size", 30) * k),
            subw=int(c.get("subw", 860) * k),
            # Brand mark must survive thumbnail scale: 24px on a 1080 canvas
            # renders ~9px on a phone feed, which is illegible. 32 is the floor.
            brand_size=int(c.get("brand_size", t.get("brand_size", 32)) * k),
            brand_bottom=int(c.get("brand_bottom", 58) * k),
            dot=int(14 * k),
            brand=spec.get("brand", ""),
            extra=c.get("extra_css", ""),
            content=c["content"],
        )
        # MUST be absolute. "file://./x.html" is an invalid URL and Chromium
        # happily screenshots its own error page, which looks like success.
        hp = os.path.abspath(os.path.join(outdir, name + ".html"))
        pp = os.path.abspath(os.path.join(outdir, name + ".png"))
        open(hp, "w").write(html)
        subprocess.run([
            chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
            "--force-device-scale-factor=1", f"--window-size={w},{h}",
            f"--screenshot={pp}", "--virtual-time-budget=4000", "file://" + hp,
        ], capture_output=True)
        ok = os.path.exists(pp) and os.path.getsize(pp) > 2000
        print(f"  {'OK ' if ok else 'FAIL'} {name}.png"
              + (f" ({os.path.getsize(pp)//1024}KB)" if ok else ""))
        if ok:
            made.append(pp)

    # A whole set failing the same way (bad path, missing font, CSS error) yields
    # near-identical files. Real cards differ in size because they differ visually.
    sizes = [os.path.getsize(p) for p in made]
    if len(sizes) > 2 and (max(sizes) - min(sizes)) < 0.02 * max(sizes):
        print("\n  WARNING: every card is within 2% of the same file size.")
        print("  That usually means they all rendered the same thing (an error page,")
        print("  or a blank canvas). Open one before you ship them.")
    return made


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2] if len(sys.argv) > 2 else "./cards"
    print(f"Rendering {len(spec['cards'])} card(s) at {spec.get('size','square')}:")
    files = build(spec, out)
    print(f"\n{len(files)} card(s) -> {os.path.abspath(out)}")
