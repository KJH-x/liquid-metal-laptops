# -*- coding: utf-8 -*-
"""Validate the built index.html: embedded JSON parses and the app script is valid JS.

Rebuild first, then run:  python pipeline/validate.py
Requires Node.js on PATH for the JavaScript syntax check.
"""
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"

h = HTML.read_text(encoding="utf-8")
m = re.search(r'<script id="app-data" type="application/json">(.*?)</script>', h, re.S)
if not m:
    raise SystemExit("index.html has no embedded app-data JSON block")
d = json.loads(m.group(1).replace("<\\/", "</"))

style = "flat" if "border-radius:0" in h else "rounded"
print("index.html products=%d sources=%d style=%s" % (
    len(d["products"]), len(d["sources"]), style))

node = shutil.which("node")
if not node:
    print("node not found; skipping JavaScript syntax check")
    raise SystemExit(0)

js = re.findall(r"<script>(.*?)</script>", h, re.S)[-1]
with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
    f.write(js)
    tmp = f.name
try:
    r = subprocess.run([node, "--check", tmp], capture_output=True, text=True)
    print("node --check returncode=%d" % r.returncode)
    if r.returncode:
        print(r.stderr[:1500])
        raise SystemExit(1)
finally:
    Path(tmp).unlink(missing_ok=True)
