# -*- coding: utf-8 -*-
"""Inject data/products.json into pipeline/template.html to build the self-contained index.html.

The site ships as a single static HTML file with the dataset embedded inline, so no
runtime fetch or server is required. Rebuild with:  python pipeline/build_html.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "data" / "products.json"
TEMPLATE = ROOT / "pipeline" / "template.html"
OUT = ROOT / "index.html"

data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
blob = blob.replace("</", "<\\/").replace("<!--", "<\\!--")

html = TEMPLATE.read_text(encoding="utf-8")
if "__DATA_JSON__" not in html:
    raise SystemExit("template.html is missing the __DATA_JSON__ placeholder")
html = html.replace("__DATA_JSON__", blob)
OUT.write_text(html, encoding="utf-8")
print("written", OUT, OUT.stat().st_size, "bytes")
