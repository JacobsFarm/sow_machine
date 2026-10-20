"""Exports the spot-seeding animation of the overseeder with Cambridge roll for the TT motor page (seeding.html).

Writes seeding/timeline.json (one entry per animation frame: time, speed, phase, motor/flow, rpm, figures) and
seeding/frames/frame_NNNN.jpg (the frames of the preview GIF, which uses the same frames at 4 fps).
Run with FreeCAD 1.1:  freecadcmd.exe export_seeding.py
"""
import json
import os
import sys

SRC = r"F:\veldrobot\aanbouwdelen\overseeding\overseeder with cambridge roll"
OUT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else \
    r"F:\veldrobot\mini doseerbak\code\TT-motor\app\seeding"
sys.path.insert(0, SRC)

import osr_params  # noqa: F401  (puts "cambridge roll" and "overrseeder" on sys.path)
import animate_osr as A
import osr_ground as GR
from PIL import Image

fr = A.frames()
meta = [A.meta(f) for f in fr]
for m, f in zip(meta, fr):
    m["s"] = round(f["s"])
timeline = {"fps": A.FPS, "source": "animate_osr.frames() / meta()", "frames": meta,
            "mini": {"note": "rpm of the 1 m overseeder; the page scales it to the mini hopper"}}
with open(os.path.join(OUT, "timeline.json"), "w", encoding="utf-8") as handle:
    json.dump(timeline, handle)

gif = Image.open(os.path.join(SRC, "previews", "animation_spot_seeding.gif"))
folder = os.path.join(OUT, "frames")
os.makedirs(folder, exist_ok=True)
n = 0
try:
    while True:
        gif.seek(n)
        gif.convert("RGB").save(os.path.join(folder, "frame_%04d.jpg" % n), quality=82)
        n += 1
except EOFError:
    pass
print("timeline frames", len(meta), "gif frames", n, "size", gif.size)
print("motor on frames", sum(1 for m in meta if m["motor"]), "rpm range",
      min(m["rpm"] for m in meta if m["motor"]), max(m["rpm"] for m in meta))
print("v range", min(m["v"] for m in meta), max(m["v"] for m in meta))
