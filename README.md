# AI4Optics-docs

Documentation site for [DeepLens](https://github.com/singer-yang/DeepLens) — a
differentiable optical lens simulator for end-to-end camera system design with
PyTorch.

Built with [MkDocs](https://www.mkdocs.org/) +
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and published
to GitHub Pages at <https://ai4optics.github.io/AI4Optics-docs/>.

## Deployment

Every push to `main` triggers `.github/workflows/deploy.yml`, which checks out the
`_deeplens_src` submodule, installs the docs toolchain plus that DeepLens source
(so `mkdocstrings` can import `deeplens` and render the API reference), and runs
`mkdocs gh-deploy`.

`_deeplens_src/` is a **git submodule** pinned to a specific
[DeepLens](https://github.com/vccimaging/DeepLens) commit — the version the docs
were written against. To document a newer API, bump the pin:

```bash
git -C _deeplens_src fetch origin
git -C _deeplens_src checkout <commit-or-branch>
git add _deeplens_src && git commit -m "chore: bump DeepLens docs source"
```

After the first successful run, enable GitHub Pages in the repo settings with
**Source: Deploy from a branch → `gh-pages` / `(root)`**.

## Local development

Requires Python ≥ 3.12 (needed by DeepLens).

```bash
git submodule update --init      # fetch the pinned DeepLens source
pip install -r docs/requirements.txt
pip install ./_deeplens_src      # required for the API reference pages
mkdocs serve                     # live preview at http://127.0.0.1:8000/
```

Content lives in `docs/`; navigation and theme are configured in `mkdocs.yml`.
