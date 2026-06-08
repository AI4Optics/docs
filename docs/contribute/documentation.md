# Building the Documentation

The documentation site is built with [MkDocs](https://www.mkdocs.org/) and the
[Material](https://squidfunk.github.io/mkdocs-material/) theme. The API reference is
pulled from the source repositories, which are included as git submodules, so clone
recursively:

```bash
git clone --recursive https://github.com/AI4Optics/docs.git
cd docs

pip install -r docs/requirements.txt
mkdocs serve   # preview at http://127.0.0.1:8000
```

If you already cloned without `--recursive`, fetch the submodules with
`git submodule update --init`.
