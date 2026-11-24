"""Check that the three language files are valid and line up.

Usage:  python tools/validate.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["en", "ar", "ur"]
REQUIRED = ["id", "title", "commentary", "notes", "hijri-date", "start", "period",
            "date-precision", "date-basis", "references", "source"]
SHARED = ["start", "end", "period", "date-precision", "date-basis", "source"]
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ENUMS = {
    "period": {"pre-prophethood", "makkah", "madinah"},
    "date-precision": {"day", "month", "year", "approximate"},
    "date-basis": {"book", "calculated"},
}
REF_TYPES = {"quran", "hadith", "seerah"}


def ref_key(r):
    """The language-neutral part of a reference."""
    return (r.get("type"), r.get("surah"), r.get("ayat"))

errors = []
data = {}
for lang in LANGS:
    path = ROOT / f"Seerah_Timeline_{lang}.json"
    with open(path, encoding="utf-8") as f:
        data[lang] = json.load(f)

en = data["en"]
ids = [e["id"] for e in en]
if len(ids) != len(set(ids)):
    errors.append("duplicate ids in en")
if [e["start"] for e in en] != sorted(e["start"] for e in en):
    errors.append("en events are not sorted by start date")

for lang in LANGS:
    for i, e in enumerate(data[lang]):
        where = f"{lang}[{i}] {e.get('id')}"
        for k in REQUIRED:
            if k not in e:
                errors.append(f"{where}: missing {k}")
        if not e.get("title") or not e.get("hijri-date"):
            errors.append(f"{where}: empty title or hijri-date")
        if not e.get("commentary") or not all(c.strip() for c in e["commentary"]):
            errors.append(f"{where}: empty commentary")
        for k in ("start", "end"):
            if k in e and not DATE.match(e[k]):
                errors.append(f"{where}: bad {k} {e[k]}")
        if "end" in e and e["end"] < e["start"]:
            errors.append(f"{where}: end before start")
        refs = e.get("references", [])
        if not isinstance(refs, list):
            errors.append(f"{where}: references must be a list")
            refs = []
        for r in refs:
            if r.get("type") not in REF_TYPES or not r.get("citation", "").strip():
                errors.append(f"{where}: bad reference {r}")
            if r.get("type") == "quran" and (not isinstance(r.get("surah"), int)
                                             or not 1 <= r["surah"] <= 114 or not r.get("ayat")):
                errors.append(f"{where}: quran reference needs surah 1-114 and ayat: {r}")
        for k, allowed in ENUMS.items():
            if e.get(k) not in allowed:
                errors.append(f"{where}: {k}={e.get(k)!r} not in {sorted(allowed)}")
    if lang == "en":
        continue
    if [e["id"] for e in data[lang]] != ids:
        errors.append(f"{lang}: ids or order differ from en")
        continue
    for a, b in zip(en, data[lang]):
        for k in SHARED:
            if a.get(k) != b.get(k):
                errors.append(f"{lang} {a['id']}: {k} differs from en")
        if len(a["commentary"]) != len(b["commentary"]):
            errors.append(f"{lang} {a['id']}: commentary has {len(b['commentary'])} items, en has {len(a['commentary'])}")
        if [ref_key(r) for r in a["references"]] != [ref_key(r) for r in b["references"]]:
            errors.append(f"{lang} {a['id']}: references differ from en in type, surah or ayat")
        if bool(a["notes"]) != bool(b["notes"]):
            errors.append(f"{lang} {a['id']}: notes present in one language only")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(ids)} events, languages {', '.join(LANGS)} aligned")
