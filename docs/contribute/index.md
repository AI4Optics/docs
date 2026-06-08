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

There are many ways to help — most of them don't require writing code.

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
  [docs](https://github.com/AI4Optics/docs) repository.
- **API reference** is generated directly from the **docstrings in the source
  repositories** (DeepLens and End2endImaging) — so a docstring fix is a code
  contribution to that project, not to the docs repo.

Small fixes (typos, broken links, clearer phrasing) are perfect first
contributions. See [Building the documentation](documentation.md) to
preview your changes locally.

### Contribute code

Ready to write code?

1. **Find or open an issue.** Comment on it so others know you are working on it
   and to avoid duplicated effort. Issues labelled **good first issue** or
   **help wanted** are great starting points.
2. **For major changes, open an issue first** to discuss the design with the
   maintainers before investing significant time.
3. Follow the [development workflow](setup.md) below.

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
