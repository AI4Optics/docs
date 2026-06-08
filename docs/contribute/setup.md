# Development Setup

## Setup

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

## Workflow

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

6. **Open a pull request** against `main` (see the [PR guidelines](pull-requests.md)).
