from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIRECTORIES = [
    "data/raw",
    "data/processed",
    "models",
    "notebooks",
    "src",
    "configs",
    "logs",
    "evidence",
]

for relative in DIRECTORIES:
    path = ROOT / relative
    path.mkdir(parents=True, exist_ok=True)

for relative in [
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "models/.gitkeep",
    "src/__init__.py",
    "configs/.gitkeep",
]:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print(f"Project root: {ROOT}")
print("\nGenerated directory tree:")
for path in sorted(ROOT.rglob("*")):
    if any(part in {".git", "aipdd_env", "__pycache__"} for part in path.parts):
        continue
    indent = "  " * (len(path.relative_to(ROOT).parts) - 1)
    marker = "[D]" if path.is_dir() else "[F]"
    print(f"{indent}{marker} {path.name}")
