---
name: docs-sync
description: >-
  Sync the AI4Optics-docs site to an updated DeepLens repo. Use this whenever the
  user wants to refresh, update, or regenerate the documentation against a newer
  version of DeepLens — phrases like "update the docs", "bump deeplens", "the
  DeepLens API changed", "re-sync the API reference", "point docs at the latest
  DeepLens", or "deeplens-src is out of date". The docs render the API reference
  from a pinned `deeplens-src` git submodule via mkdocstrings/griffe static
  analysis, so "syncing" means bumping that submodule pin, verifying the
  documented symbols still resolve, handling docstring-markup regressions, and
  redeploying. Reach for this skill before manually editing the submodule or CI.
---

# Docs sync — refresh AI4Optics-docs against an updated DeepLens

## What this repo is (the mental model)

This is a **standalone docs site** for [DeepLens](https://github.com/vccimaging/DeepLens),
published to GitHub Pages at <https://ai4optics.github.io/AI4Optics-docs/> via a
`mkdocs gh-deploy` GitHub Action on every push to `main`.

The only thing coupled to DeepLens source is the **API Reference**: ~50 autodoc
blocks like `::: deeplens.GeoLens` in `docs/api/*.md`. They are rendered by
**mkdocstrings → griffe**, which **statically parses** the DeepLens `.py` files —
it does *not* import them. That is why CI needs no torch and why the source is a
plain git submodule rather than a pip install.

Key facts that make syncing safe and cheap:

- `deeplens-src/` is a **git submodule** pinned to a specific DeepLens commit.
  The docs reflect *that* commit's docstrings, frozen until you bump the pin.
- `mkdocs.yml` points griffe at it with `paths: [deeplens-src]` and
  `allow_inspection: false` (pure static, no import).
- Everything else (prose, `docs/assets/`, example pages, stylesheets) is
  self-contained; example links are absolute GitHub URLs.

So "sync the docs" almost always means: **bump the submodule pin, make sure the
API still resolves, redeploy.** Prose only changes if the user asks.

## The procedure

Work from the repo root. Create a TodoWrite item per step.

### 1. Pick the target DeepLens version

Ask the user (or infer from their request) what to sync to: a branch tip
(`origin/dev`, `origin/main`) or a specific commit/tag. **Prefer a specific
commit** — submodules pin a SHA, and a moving branch tip just means "whatever it
was when you ran this." A tag or release commit is the most reproducible.

### 2. Bump the submodule pin

```bash
git -C deeplens-src fetch origin
git -C deeplens-src checkout <commit-or-branch>   # e.g. origin/main, a tag, or a SHA
```

Note the old and new SHAs so you can summarize what changed:

```bash
git -C deeplens-src log --oneline -1
```

### 3. Pre-flight: verify the documented API still resolves

This is the step that prevents a broken deploy. Renames/moves/removals upstream
make `::: deeplens.X` blocks silently fail. Run the bundled checker (static, no
deps), which mirrors how griffe resolves symbols:

```bash
python .claude/skills/docs-sync/scripts/check_api_symbols.py docs/api deeplens-src
```

- **Exit 0 / "All symbols resolve"** → good, continue.
- **Unresolved symbols** → the printed report tells you which. For each, decide:
  the object was *renamed/moved* (update the `::: ...` path in the relevant
  `docs/api/*.md`), or *removed* (drop that block and its nav entry in
  `mkdocs.yml`), or you pinned the wrong commit. Fix, then re-run until clean.

### 4. Check for docstring-markup regressions (the recurring gotcha)

mkdocstrings uses Google-style docstrings and does **not** understand Sphinx
cross-reference roles. If upstream wrote new docstrings using `:meth:`,
`:class:`, or `:func:` roles, they render as ugly raw text (e.g. literal
`` :class:`~deeplens.geolens.GeoLens` ``) in the API pages. Detect them:

```bash
grep -rnE ':(meth|class|func|mod|attr|obj):`' deeplens-src/deeplens --include='*.py'
```

If there are hits, those docstrings need cleaning to plain Markdown backticks
(`` :class:`~deeplens.geolens.GeoLens` `` → `` `GeoLens` ``). The durable fix is
**upstream**, in DeepLens — porting it into the docs repo isn't possible because
the source is a submodule, not editable here. See
`references/docstring-fix.md` for how this was handled before (cherry-pick the
cleanup commit onto the DeepLens branch, push, then bump the submodule to it).
If the user is fine with a few raw-markup spots for now, you can proceed and note
it.

### 5. Optional: update prose / examples / nav

Only if the user asked, or if step 3 surfaced added/removed models. New lens
model or API surface → add a `docs/api/<model>.md` with the `::: deeplens.X`
block and a nav entry in `mkdocs.yml`; mirror the existing pages' style. Removed
model → delete the page and nav entry.

### 6. Commit, push, and let CI deploy

```bash
git add deeplens-src mkdocs.yml docs        # whatever changed
git commit -m "docs: sync to DeepLens <short-sha or tag>"
git push
```

The push triggers `.github/workflows/deploy.yml`. Pushing to the `AI4Optics-docs`
SSH remote may need the Bash sandbox disabled in this environment (the SSH key
isn't reachable inside the sandbox) — that's an environment quirk, not a repo
problem.

### 7. Verify the live deploy (don't trust green CI alone)

```bash
gh run list --limit 1 --json status,conclusion,displayTitle   # both deploy + pages build should be success
gh run view <deploy-run-id> --log | grep -iE 'ERROR|could not collect|abort'   # expect nothing
```

Then hit the live site (Pages takes ~30–60s after the run):

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://ai4optics.github.io/AI4Optics-docs/
curl -s -o /dev/null -w "%{http_code}\n" https://ai4optics.github.io/AI4Optics-docs/api/geolens/
# confirm no raw Sphinx markup leaked into a rendered API page:
curl -s https://ai4optics.github.io/AI4Optics-docs/api/geolens/ | grep -cE ':class:`~deeplens|:meth:`'   # expect 0
```

Report the version delta (old SHA → new SHA), any `::: ...` references you had to
update, and the live verification result.

## Gotchas worth remembering

- **Don't pip-install `deeplens-src`.** griffe reads it statically; installing it
  would drag in torch and slow CI for no benefit. The `paths:` setting is what
  wires it up.
- **Never rename the submodule dir to `deeplens`.** It contains the real
  `deeplens/` package; a dir named `deeplens` at repo root becomes a namespace
  package that *shadows* the documented one and breaks the build. `deeplens-src`
  (hyphen → non-importable) is deliberate.
- **Submodule SHA must stay reachable.** Pin to a commit on `dev`/`main`/a tag,
  not a throwaway branch that might be squash-merged and GC'd later.
- **Anyone cloning** must run `git submodule update --init` (CI does this via
  `submodules: recursive` in the checkout step).

## Bundled resources

- `scripts/check_api_symbols.py` — static resolver for the `::: deeplens.X`
  blocks (step 3). No imports, no deps.
- `references/docstring-fix.md` — how the Sphinx-role docstring cleanup was
  landed upstream and pinned (read when step 4 finds hits).
