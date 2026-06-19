#!/usr/bin/env python3
"""打包成 .skill 文件，只包含技能相关文件"""

import os, sys, zipfile
from datetime import datetime

SKILL_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "VERSION.md",
    ".gitignore",
    "scripts/",
    "tests/",
    "evals/",
    "config/scheduler_config.json",
]

def package(skill_dir=".", output_dir=None):
    skill_dir = os.path.abspath(skill_dir)
    name = os.path.basename(skill_dir)
    output_dir = output_dir or os.path.join(skill_dir, "release")
    os.makedirs(output_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(output_dir, f"{name}_{ts}.skill")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for item in SKILL_FILES:
            path = os.path.join(skill_dir, item)
            if not os.path.exists(path):
                continue
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    dirs[:] = [d for d in dirs if d != "__pycache__"]
                    for f in files:
                        fp = os.path.join(root, f)
                        z.write(fp, os.path.relpath(fp, skill_dir))
            else:
                z.write(path, item)

    size = os.path.getsize(out)
    print(f"✅ {out} ({size/1024:.1f} KB)")
    return out

if __name__ == "__main__":
    package(sys.argv[1] if len(sys.argv) > 1 else ".")
