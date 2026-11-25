import os
import shutil

# news-image-20261124 v2 — the program copies the vendored entry.png to
# $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png). Standard library
# only, no network, no randomness: two runs write identical bytes.

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
