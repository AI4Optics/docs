# AI4Optics-docs

Documentation site for [DeepLens](https://github.com/singer-yang/DeepLens) — a
differentiable optical lens simulator for end-to-end camera system design with
PyTorch.

Built with [MkDocs](https://www.mkdocs.org/) +
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and published
to GitHub Pages at <https://ai4optics.github.io/AI4Optics-docs/>.

## Deployment

Every push to `main` triggers `.github/workflows/deploy.yml`, which installs the
docs toolchain plus `deeplens-core` (so `mkdocstrings` can render the API
reference) and runs `mkdocs gh-deploy`.

After the first successful run, enable GitHub Pages in the repo settings with
**Source: Deploy from a branch → `gh-pages` / `(root)`**.

## Local development

Requires Python ≥ 3.12 (needed by `deeplens-core`).

```bash
pip install -r docs/requirements.txt
pip install deeplens-core   # required for the API reference pages
mkdocs serve                # live preview at http://127.0.0.1:8000/
```

Content lives in `docs/`; navigation and theme are configured in `mkdocs.yml`.
