"""
generate_index.py — Generate index.json for AI Karyashala certificate verification.

Scans docs/bootcamp/kiet/ for valid certificate folders (those containing index.html),
excludes the 'verify' folder, and writes an index.json array of certificate IDs.

Usage:
    python generate_index.py

Output:
    docs/bootcamp/kiet/index.json
"""

import json
import os
import sys

# ── Configuration ──────────────────────────────────────────────
KIET_DIR   = os.path.join("docs", "bootcamp", "kiet")
OUTPUT     = os.path.join(KIET_DIR, "index.json")
EXCLUDE    = {"verify", "assets", ".git"}   # folders to skip

def main():
    if not os.path.isdir(KIET_DIR):
        print(f"ERROR: Directory not found: {KIET_DIR}")
        sys.exit(1)

    ids = []
    for entry in sorted(os.listdir(KIET_DIR)):
        # Skip excluded folders and non-directories
        if entry in EXCLUDE:
            continue
        folder = os.path.join(KIET_DIR, entry)
        if not os.path.isdir(folder):
            continue
        # Only include if it has an index.html
        if os.path.isfile(os.path.join(folder, "index.html")):
            ids.append(entry)

    # Write JSON
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(ids, f, indent=None)

    print(f"Generated {OUTPUT}")
    print(f"Total certificate IDs: {len(ids)}")

if __name__ == "__main__":
    main()
