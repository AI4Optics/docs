# Pull Requests

## Guidelines

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
  [API reference](../deeplens/api/index.md) by mkdocstrings, so clear, complete
  docstrings directly improve the documentation.
- **Config-driven design** — prefer passing configuration objects over scattering
  hard-coded hyperparameters.
