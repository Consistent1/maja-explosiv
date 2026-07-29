#!/usr/bin/env python3
"""Pull a Figma node subtree and flatten it into a comparable spec.

Companion to project_docs/figma-audit-guide.md, which explains the method and
the traps. Standard library only - this machine has no `requests`.

Usage:
    scripts/figma_audit.py spec 695:5712                 # flattened spec table
    scripts/figma_audit.py spec 695:5712 --json out.json # machine-readable
    scripts/figma_audit.py raw  695:5712 --json raw.json # untouched API JSON
    scripts/figma_audit.py render 695:5712 --out ref.png # 1x PNG of the node
    scripts/figma_audit.py image bd3f21a6...  --out a.png # a fill's source asset

The token is read from ~/.config/figma/token and never printed.
"""

import argparse
import json
import os
import pathlib
import sys
import urllib.request

FILE_KEY = "18tst8uq38FlDlaZA5cPCz"  # MajaExplosiv_Website Redesign
TOKEN_PATH = pathlib.Path.home() / ".config" / "figma" / "token"
CACHE = pathlib.Path(
    os.environ.get("FIGMA_AUDIT_CACHE", pathlib.Path(__file__).parent / ".figma-cache")
)


def _token():
    try:
        return TOKEN_PATH.read_text().strip()
    except FileNotFoundError:
        sys.exit(f"No Figma token at {TOKEN_PATH} - see project_docs/figma-audit-guide.md")


def _get(url):
    req = urllib.request.Request(url, headers={"X-Figma-Token": _token()})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def fetch_node(node_id, refresh=False):
    """Node subtree, cached on disk - the API is slow and the data is static."""
    CACHE.mkdir(exist_ok=True)
    cached = CACHE / f"{node_id.replace(':', '-')}.json"
    if cached.exists() and not refresh:
        return json.loads(cached.read_text())
    data = _get(f"https://api.figma.com/v1/files/{FILE_KEY}/nodes?ids={node_id}")
    doc = data["nodes"][node_id]["document"]
    cached.write_text(json.dumps(doc))
    return doc


# --------------------------------------------------------------------------
# Normalisation. Everything here exists because the raw API shape does not
# compare directly against CSS - see the guide's "Traps" section.
# --------------------------------------------------------------------------

def hexcolor(c):
    return "#%02X%02X%02X" % tuple(round(c[k] * 255) for k in "rgb")


def paint(f):
    """One fill/stroke, flattened to something comparable to a CSS value."""
    t = f.get("type")
    if t == "SOLID":
        out = hexcolor(f["color"])
        if f["color"].get("a", 1) != 1 or f.get("opacity", 1) != 1:
            out += f" @{f['color'].get('a', 1) * f.get('opacity', 1):.2f}"
        var = (f.get("boundVariables") or {}).get("color", {}).get("id")
        if var:
            out += f" [{var}]"
        return out
    if t == "IMAGE":
        # scaleMode STRETCH is what the Figma UI calls "Crop"; imageTransform is
        # the visible window in normalised image space.
        out = f"IMAGE {f.get('imageRef', '?')[:8]} {f.get('scaleMode')}"
        m = f.get("imageTransform")
        if m:
            a, _, tx = m[0]
            _, d, ty = m[1]
            out += (f" crop x {tx * 100:.2f}%..{(tx + a) * 100:.2f}%"
                    f" y {ty * 100:.2f}%..{(ty + d) * 100:.2f}%")
        return out
    return t


def effective_text_style(n):
    """The style that is actually RENDERED, not the node default.

    `node["style"]` is only the default. If any character carries an override,
    the real style lives in styleOverrideTable, keyed by the ids in
    characterStyleOverrides. A node can be entirely overridden - the default
    then describes a font that is never drawn. Reading `style` alone invents
    inconsistencies that do not exist. See the guide's "Traps" section.

    Returns (style_dict, note) where note flags mixed runs.
    """
    base = dict(n.get("style") or {})
    ov = n.get("characterStyleOverrides") or []
    table = n.get("styleOverrideTable") or {}
    if not ov:
        return base, None
    # Pad: characters past the end of the override list use the default.
    ids = list(ov) + [0] * max(0, len(n.get("characters", "")) - len(ov))
    distinct = sorted(set(ids), key=ids.index)
    # letterSpacing is absolute PX, authored against the default fontSize. When an
    # override changes fontSize but not letterSpacing, keeping the px value yields a
    # nonsense em ratio (-0.0514em where Figma's panel shows -3%). Carry the RATIO.
    base_ratio = None
    if base.get("letterSpacing") and base.get("fontSize"):
        base_ratio = base["letterSpacing"] / base["fontSize"]

    merged = []
    for i in distinct:
        o = table.get(str(i), {})
        s = dict(base)
        s.update(o)
        if base_ratio is not None and "letterSpacing" not in o and \
                o.get("fontSize", base.get("fontSize")) != base.get("fontSize"):
            s["letterSpacing"] = s["fontSize"] * base_ratio
        merged.append(s)
    keys = ("fontFamily", "fontWeight", "fontSize", "textCase",
            "lineHeightPercentFontSize", "letterSpacing", "leadingTrim")
    sigs = {tuple(s.get(k) for k in keys) for s in merged}
    if len(sigs) == 1:
        return merged[0], None
    # Mixed runs: report the dominant one but say so loudly.
    counts = {}
    for i in ids:
        counts[i] = counts.get(i, 0) + 1
    top = max(counts, key=counts.get)
    s = dict(base)
    s.update(table.get(str(top), {}))
    return s, f"MIXED ({len(sigs)} runs)"


def textstyle(s):
    """Figma's style block -> the CSS properties worth diffing."""
    size = s.get("fontSize")
    out = {
        "family": s.get("fontFamily"),
        "weight": s.get("fontWeight"),
        "size": size,
    }
    # Figma reports line height two ways; CSS wants a ratio.
    if s.get("lineHeightPx") and size:
        out["line_height"] = round(s["lineHeightPx"] / size, 4)
    elif s.get("lineHeightPercentFontSize"):
        out["line_height"] = round(s["lineHeightPercentFontSize"] / 100, 4)
    # letterSpacing is in PIXELS in the REST API, even though the UI shows %.
    if s.get("letterSpacing") and size:
        out["tracking_em"] = round(s["letterSpacing"] / size, 4)
    if s.get("textCase"):
        out["case"] = s["textCase"]
    if s.get("textAlignHorizontal"):
        out["align"] = s["textAlignHorizontal"]
    if s.get("leadingTrim"):
        # CSS has no stable equivalent; it makes Figma's box cap-height-tight,
        # so box heights will not match CSS line boxes. See the guide.
        out["leading_trim"] = s["leadingTrim"]
    return out


def flatten(root):
    """Depth-first list of nodes with boxes relative to `root`."""
    rb = root["absoluteBoundingBox"]
    rows = []

    def walk(n, depth, path):
        bb = n.get("absoluteBoundingBox")
        row = {
            "id": n["id"],
            "depth": depth,
            "path": path,
            "name": n.get("name", ""),
            "type": n.get("type"),
        }
        if bb:
            # Round to 0.01 - the design has values like 153.95849609375 and the
            # owner's calibration is "34.95 may as well be 35".
            row.update(
                x=round(bb["x"] - rb["x"], 2), y=round(bb["y"] - rb["y"], 2),
                w=round(bb["width"], 2), h=round(bb["height"], 2),
            )
        for k in ("layoutMode", "itemSpacing", "paddingLeft", "paddingRight",
                  "paddingTop", "paddingBottom", "clipsContent", "cornerRadius",
                  "opacity", "counterAxisAlignItems", "primaryAxisAlignItems"):
            if k in n:
                row[k] = n[k]
        if n.get("rotation"):
            row["rotation_deg"] = round(n["rotation"] * 57.29577951308232, 2)
        fills = [paint(f) for f in (n.get("fills") or []) if f.get("visible", True)]
        if fills:
            row["fills"] = fills
        strokes = [paint(f) for f in (n.get("strokes") or []) if f.get("visible", True)]
        if strokes:
            row["strokes"] = strokes
            row["stroke_weight"] = n.get("strokeWeight")
        if n.get("style"):
            eff, note = effective_text_style(n)
            row["text"] = textstyle(eff)
            if note:
                row["text"]["note"] = note
            # A fill override on the characters beats the node-level fill.
            ovfills = eff.get("fills")
            if ovfills:
                row["fills"] = [paint(f) for f in ovfills if f.get("visible", True)]
        if n.get("characters"):
            row["chars"] = n["characters"][:40]
        rows.append(row)
        for i, c in enumerate(n.get("children", [])):
            walk(c, depth + 1, f"{path}/{i}")

    walk(root, 0, "")
    return rows


def print_spec(rows):
    for r in rows:
        ind = "  " * r["depth"]
        box = (f"{r['w']:>7.2f}x{r['h']:<7.2f} @{r['x']:>8.2f},{r['y']:<8.2f}"
               if "w" in r else " " * 34)
        print(f"{r['id']:<18}{ind}{r['name'][:34]:<36}{r['type']:<11}{box}")
        extra = []
        if r.get("layoutMode"):
            pad = (f"pad {r.get('paddingTop', 0)}/{r.get('paddingRight', 0)}/"
                   f"{r.get('paddingBottom', 0)}/{r.get('paddingLeft', 0)}")
            extra.append(f"{r['layoutMode']} gap={r.get('itemSpacing')} {pad}")
        if r.get("rotation_deg"):
            extra.append(f"rotation {r['rotation_deg']}deg")
        if r.get("clipsContent") is not None:
            extra.append(f"clips={r['clipsContent']}")
        if r.get("text"):
            t = r["text"]
            extra.append(f"{t['family']} {t['weight']} {t['size']}px "
                         f"lh={t.get('line_height')} tr={t.get('tracking_em')}em "
                         f"case={t.get('case', 'ORIGINAL')}"
                         + (f" trim={t['leading_trim']}" if t.get('leading_trim') else "")
                         + (f"  <<{t['note']}>>" if t.get('note') else ""))
        if r.get("fills"):
            extra.append("fill " + " | ".join(r["fills"]))
        if r.get("strokes"):
            extra.append(f"stroke {r['stroke_weight']}px " + " | ".join(r["strokes"]))
        if r.get("chars"):
            extra.append(f'"{r["chars"]}"')
        for e in extra:
            print(f"{'':<18}{ind}    - {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["spec", "raw", "render", "image"])
    ap.add_argument("target")
    ap.add_argument("--json")
    ap.add_argument("--out")
    ap.add_argument("--scale", default="1")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    if a.cmd == "image":
        urls = _get(f"https://api.figma.com/v1/files/{FILE_KEY}/images")["meta"]["images"]
        match = [v for k, v in urls.items() if k.startswith(a.target)]
        if not match:
            sys.exit(f"no image ref starting {a.target}")
        urllib.request.urlretrieve(match[0], a.out or "fill.png")
        print(f"wrote {a.out or 'fill.png'}")
        return

    if a.cmd == "render":
        d = _get(f"https://api.figma.com/v1/images/{FILE_KEY}"
                 f"?ids={a.target}&scale={a.scale}&format=png")
        if d.get("err"):
            sys.exit(d["err"])
        urllib.request.urlretrieve(d["images"][a.target], a.out or "node.png")
        print(f"wrote {a.out or 'node.png'}")
        return

    doc = fetch_node(a.target, a.refresh)
    if a.cmd == "raw":
        out = json.dumps(doc, indent=2)
        (pathlib.Path(a.json).write_text(out) if a.json else print(out))
        return

    rows = flatten(doc)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rows, indent=1))
        print(f"wrote {a.json} ({len(rows)} nodes)")
    else:
        print_spec(rows)


if __name__ == "__main__":
    main()
