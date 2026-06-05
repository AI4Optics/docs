# Contribute

AI4Optics is an open, community-driven family of differentiable-optics projects —
[DeepLens](https://github.com/vccimaging/DeepLens) for differentiable lens design,
[End2endImaging](https://github.com/vccimaging/End2endImaging) for end-to-end camera
simulation, and more on the way. We build these tools to accelerate optical research,
and contributions of every kind make them better.

Whether you are fixing a typo, filing a bug report, adding a new lens model, or
proposing a research-grade feature, this guide explains **what** you can contribute
and **how** to do it.

## Ways to contribute

<div class="grid cards" markdown>

-   :material-bug:{ .lg .middle } __Report a bug__

    ---

    Something broken or behaving unexpectedly? Open an issue with a minimal
    reproducible example.

    [:octicons-arrow-right-24: Report a bug](#report-a-bug)

-   :material-lightbulb-on:{ .lg .middle } __Suggest a feature__

    ---

    Have an idea for a new capability, lens model, or workflow? Propose it before
    you build it.

    [:octicons-arrow-right-24: Suggest a feature](#suggest-a-feature)

-   :material-book-open-variant:{ .lg .middle } __Improve the docs__

    ---

    Fix unclear wording, add an example, or sharpen an API docstring.

    [:octicons-arrow-right-24: Improve documentation](#improve-documentation)

-   :material-code-braces:{ .lg .middle } __Contribute code__

    ---

    Fix a bug, add a feature, or build a new optical component.

    [:octicons-arrow-right-24: Contribute code](#contribute-code)

</div>

### Report a bug

A good bug report saves everyone time. Before opening one:

1. **Search existing issues** in the relevant repository
   ([DeepLens](https://github.com/vccimaging/DeepLens/issues),
   [End2endImaging](https://github.com/vccimaging/End2endImaging/issues)) — your
   problem may already be tracked.
2. **Open a new issue** with a **minimal, reproducible example**. Include:
    - what you expected to happen versus what actually happened,
    - a short code snippet (and the lens/sensor config or `.json` file, if relevant),
    - the full traceback,
    - your environment — OS, Python version, PyTorch and CUDA versions, and GPU.
3. **Keep each issue focused.** File separate issues for unrelated problems and
   link them rather than combining them into one.

### Suggest a feature

New capabilities are welcome, but a quick discussion first avoids wasted effort:

1. **Search** open issues for a similar request.
2. **Open an issue** describing the **use case** — what you are trying to do, why
   it is valuable, and who benefits. A sketch of the intended API or a link to a
   relevant paper helps a lot.
3. For anything substantial, **align with the maintainers before implementing.**
   This keeps your contribution consistent with the project's direction and far
   more likely to be merged.

### Improve documentation

Documentation lives in two places, depending on what you want to change:

- **Narrative docs** (guides, overviews, examples, this page) live in the
  [AI4Optics-docs](https://github.com/AI4Optics/AI4Optics-docs) repository.
- **API reference** is generated directly from the **docstrings in the source
  repositories** (DeepLens and End2endImaging) — so a docstring fix is a code
  contribution to that project, not to the docs repo.

Small fixes (typos, broken links, clearer phrasing) are perfect first
contributions. See [Building the documentation](#building-the-documentation) to
preview your changes locally.

### Contribute code

Ready to write code?

1. **Find or open an issue.** Comment on it so others know you are working on it
   and to avoid duplicated effort. Issues labelled **good first issue** or
   **help wanted** are great starting points.
2. **For major changes, open an issue first** to discuss the design with the
   maintainers before investing significant time.
3. Follow the [development workflow](#development-workflow) below.

#### Add a new lens, sensor, or network

These projects are designed to be extended with new optical and neural components
— a new lens model, sensor profile, ISP module, or reconstruction network. To add
one:

- Place it in the matching module (e.g. a lens model under `deeplens/`, a sensor
  under `sensor/`, a network under `network/`) and subclass the relevant base
  class so it plugs into the existing pipeline.
- Match the surrounding code's structure, naming, and config-driven style.
- Add a **test** under `test/` and, where it helps users, a small runnable
  **example** script.

## Development setup

Each project is a standalone PyTorch repository. Clone the one you want to work on
and set up a fresh environment (**Python ≥ 3.12**):

| Project | Repository | Editable install |
|---------|-----------|------------------|
| DeepLens | [vccimaging/DeepLens](https://github.com/vccimaging/DeepLens) | `pip install -e ".[dev]"` |
| End2endImaging | [vccimaging/End2endImaging](https://github.com/vccimaging/End2endImaging) | `pip install -r requirements.txt` |

```bash
# Clone the project (DeepLens shown; substitute End2endImaging as needed)
git clone https://github.com/vccimaging/DeepLens.git
cd DeepLens

# Create and activate the conda environment
conda env create -f environment.yml -n deeplens_env
conda activate deeplens_env

# Install in editable mode with development extras
pip install -e ".[dev]"
```

## Development workflow

1. **Fork** the repository and **clone** your fork.
2. **Create a branch** from `main`: `git checkout -b fix/short-description`.
3. **Make your changes**, keeping commits focused and well-described.
4. **Format** your code with [Ruff](https://docs.astral.sh/ruff/):

    ```bash
    ruff format .
    ```

5. **Add tests** for new behaviour and run the suite:

    ```bash
    pytest test/ -v
    # with coverage (use the project's package name)
    pytest test/ --cov=deeplens --cov-report=term-missing      # DeepLens
    pytest test/ --cov=end2end_imaging --cov-report=term-missing  # End2endImaging
    ```

6. **Open a pull request** against `main` (see the guidelines below).

## Pull request guidelines

To make your PR easy to review and quick to merge:

- **Link the issue or discussion** it addresses, so the change has agreed-upon
  motivation.
- **Keep it focused.** A small, single-purpose PR is reviewed far faster than a
  large mixed one.
- **Include tests** for new functionality and bug fixes, and make sure the full
  suite passes.
- **Format with Ruff** and update any affected documentation or docstrings.
- **Write a clear description** of what changed and why.

!!! note "Contributor License Agreement (CLA)"
    Your first pull request to DeepLens or End2endImaging will prompt you to sign a
    Contributor License Agreement, handled automatically by
    [CLA Assistant](https://cla-assistant.io/). You can review the
    [CLA](https://gist.github.com/singer-yang/b2e4214a12a220899ed682d9c24f575b) in
    advance.

## Code style

- **Formatting:** [Ruff](https://docs.astral.sh/ruff/) (`ruff format .`), following
  PEP 8.
- **Type hints** on public functions and methods.
- **Google-style docstrings** — these are rendered into the
  [API reference](deeplens/api/index.md) by mkdocstrings, so clear, complete
  docstrings directly improve the documentation.
- **Config-driven design** — prefer passing configuration objects over scattering
  hard-coded hyperparameters.

## Building the documentation

The documentation site is built with [MkDocs](https://www.mkdocs.org/) and the
[Material](https://squidfunk.github.io/mkdocs-material/) theme. The API reference is
pulled from the source repositories, which are included as git submodules, so clone
recursively:

```bash
git clone --recursive https://github.com/AI4Optics/AI4Optics-docs.git
cd AI4Optics-docs

pip install -r docs/requirements.txt
mkdocs serve   # preview at http://127.0.0.1:8000
```

If you already cloned without `--recursive`, fetch the submodules with
`git submodule update --init`.

## Code of conduct & license

All participation is governed by each project's **Code of Conduct** (see
`CODE_OF_CONDUCT.md` in the [DeepLens](https://github.com/vccimaging/DeepLens) and
[End2endImaging](https://github.com/vccimaging/End2endImaging) repositories). Please
be respectful and constructive.

By contributing, you agree that your contributions are licensed under each project's
**Apache-2.0** license.
