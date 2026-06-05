#!/usr/bin/env python3
"""Verify every ``::: deeplens.X`` autodoc reference in the docs resolves
against a DeepLens source tree — by *static* analysis, the same way
mkdocstrings/griffe renders the API pages.

This is the single most important pre-flight check when syncing the docs to a
new DeepLens version: if a class/function was renamed, moved, or removed
upstream, the autodoc block silently fails and the API page renders empty (or
the whole build aborts). Running this against the freshly-bumped submodule
catches that before you ever push.

It does not import anything (no torch, no runtime deps) — it parses the .py
files with ``ast``, mirroring how griffe finds objects.

Usage:
    python check_api_symbols.py [DOCS_API_DIR] [SOURCE_ROOT]

Defaults assume you run it from the repo root:
    DOCS_API_DIR = docs/deeplens/api  (where the ::: blocks live)
    SOURCE_ROOT  = deeplens-src       (the submodule that holds the deeplens/ package)

Exit code 0 = every symbol resolves; 1 = one or more problems (printed).
"""

import ast
import os
import re
import sys


def collect_references(docs_api_dir: str) -> set[str]:
    """Find every dotted identifier referenced via a ``:::`` autodoc block."""
    refs: set[str] = set()
    for dirpath, _, filenames in os.walk(docs_api_dir):
        for name in filenames:
            if not name.endswith(".md"):
                continue
            with open(os.path.join(dirpath, name), encoding="utf-8") as fh:
                for line in fh:
                    match = re.match(r"\s*:::\s*([\w.]+)", line)
                    if match:
                        refs.add(match.group(1))
    return refs


def top_level_names(module_path: str) -> set[str]:
    """Names defined OR imported at a module's top level (griffe follows both,
    so a re-export like ``from .geolens import GeoLens`` counts)."""
    try:
        tree = ast.parse(open(module_path, encoding="utf-8").read())
    except (OSError, SyntaxError):
        return set()
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add((alias.asname or alias.name).split(".")[0])
    return names


def resolve(dotted: str, source_root: str) -> tuple[str, str]:
    """Resolve ``deeplens.a.b.Symbol`` -> module ``deeplens/a/b`` + attr ``Symbol``."""
    parts = dotted.split(".")
    module_parts, attr = parts[:-1], parts[-1]
    pkg_init = os.path.join(source_root, *module_parts, "__init__.py")
    module_py = os.path.join(source_root, *module_parts) + ".py"
    path = pkg_init if os.path.exists(pkg_init) else (
        module_py if os.path.exists(module_py) else None
    )
    if path is None:
        return ("NO_MODULE", "/".join(module_parts))
    if attr in top_level_names(path):
        return ("OK", path)
    return ("MISSING_ATTR", f"{attr} not found in {path}")


def main() -> int:
    docs_api_dir = sys.argv[1] if len(sys.argv) > 1 else "docs/deeplens/api"
    source_root = sys.argv[2] if len(sys.argv) > 2 else "deeplens-src"

    if not os.path.isdir(docs_api_dir):
        print(f"ERROR: docs API dir not found: {docs_api_dir}", file=sys.stderr)
        return 2
    if not os.path.isdir(source_root):
        print(
            f"ERROR: source root not found: {source_root}\n"
            "Did you run `git submodule update --init`?",
            file=sys.stderr,
        )
        return 2

    refs = collect_references(docs_api_dir)
    problems = []
    for ref in sorted(refs):
        status, info = resolve(ref, source_root)
        if status != "OK":
            problems.append((ref, status, info))

    print(f"Checked {len(refs)} autodoc symbols against {source_root!r}")
    if not problems:
        print("All symbols resolve. ✓")
        return 0

    print(f"\n{len(problems)} unresolved symbol(s):")
    for ref, status, info in problems:
        print(f"  ✗ {ref}  [{status}]  {info}")
    print(
        "\nEach of these would render an empty API page or abort the build.\n"
        "Either the symbol was renamed/moved/removed upstream (update the\n"
        "`::: ...` reference in docs/api/), or you pinned the wrong commit."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
