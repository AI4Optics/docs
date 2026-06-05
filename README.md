# docs

Documentation site for [DeepLens](https://github.com/singer-yang/DeepLens) — a
differentiable optical lens simulator for end-to-end camera system design with
PyTorch.

Built with [MkDocs](https://www.mkdocs.org/) +
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and published
to GitHub Pages at <https://ai4optics.github.io/docs/>.

## Deployment

Every push to `main` triggers `.github/workflows/deploy.yml`, which checks out the
`deeplens-src` submodule, installs the docs toolchain, and runs `mkdocs gh-deploy`.
`mkdocstrings`/`griffe` renders the API reference by **statically parsing** the
DeepLens source under `deeplens-src/` (via the `paths:` setting in `mkdocs.yml`) —
it does not import `deeplens`, so no torch/runtime install is needed.

`deeplens-src/` is a **git submodule** pinned to a specific
[DeepLens](https://github.com/vccimaging/DeepLens) commit — the version the docs
were written against. To document a newer API, bump the pin:

```bash
git -C deeplens-src fetch origin
git -C deeplens-src checkout <commit-or-branch>
git add deeplens-src && git commit -m "chore: bump DeepLens docs source"
```

After the first successful run, enable GitHub Pages in the repo settings with
**Source: Deploy from a branch → `gh-pages` / `(root)`**.

## Local development

Python ≥ 3.12 recommended (so griffe parses the DeepLens 3.12 source syntax).

```bash
git submodule update --init      # fetch the pinned DeepLens source
pip install -r docs/requirements.txt
mkdocs serve                     # live preview at http://127.0.0.1:8000/
```

The API reference is rendered from `deeplens-src/` by static analysis — no need to
install `deeplens` or its dependencies.

Content lives in `docs/`; navigation and theme are configured in `mkdocs.yml`.
