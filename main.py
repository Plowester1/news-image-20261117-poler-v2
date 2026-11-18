"""news-image-20261117 entry (poler v2): copy the bundled image to the
output directory as entry.png.

The image (entry.png, beside this file) is a 1024x1024 light sky-blue
front page summing up Tuesday 17 November 2026 in eight verified stories,
led by Japan scrambling jets. It was composed programmatically with PIL
(see build_image.py). This program is a pure file copy: no network, no
randomness, so repeated runs write identical bytes.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1 << 20  # competition limit: image must be <= 1 MiB


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if not os.path.isfile(SRC):
    raise SystemExit("entry.png missing next to main.py — nothing to copy")
if os.path.getsize(SRC) > MAX_BYTES:
    raise SystemExit("entry.png exceeds the 1 MiB competition limit")

os.makedirs(DST_DIR, exist_ok=True)
DST = os.path.join(DST_DIR, "entry.png")
shutil.copyfile(SRC, DST)

# The competition runs this program twice and both runs must write the
# same bytes, so fail loudly instead of submitting a corrupt copy.
if _sha256(DST) != _sha256(SRC):
    raise SystemExit("entry.png copy mismatch: output differs from source")
print("wrote entry.png (sha256 %s)" % _sha256(DST))
