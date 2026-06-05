# Contribute

AI4Optics is a family of differentiable-optics projects. Each one lives in its
own repository, but they all share the same contribution workflow, code style,
and testing conventions described here.

## Development Setup

Clone the project you want to work on and install it in a fresh environment:

| Project | Repository | Install |
|---------|-----------|---------|
| DeepLens | [vccimaging/DeepLens](https://github.com/vccimaging/DeepLens) | `pip install -e ".[dev]"` |
| End2endImaging | [vccimaging/End2endImaging](https://github.com/vccimaging/End2endImaging) | `pip install -r requirements.txt` |

```bash
git clone https://github.com/vccimaging/<project>.git
cd <project>
# then run the project's install command from the table above
```

## Code Style

Format all code with [Ruff](https://docs.astral.sh/ruff/) before submitting:

```bash
ruff format .
```

## Testing

Run the full test suite:

```bash
pytest test/ -v
```

Run a single test file:

```bash
pytest test/test_geolens.py -v
```

Run with coverage — pass the project's package name (`deeplens` or
`end2end_imaging`):

```bash
pytest test/ --cov=<package> --cov-report=term-missing
```

## Pull Request Guidelines

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Run `ruff format .` and `pytest test/ -v` before pushing
4. Open a PR with a clear description of the changes

## Building Documentation

Documentation for every project is centralized in the
[AI4Optics-docs](https://github.com/AI4Optics/AI4Optics-docs) repository. To
preview it locally:

```bash
pip install -r docs/requirements.txt
mkdocs serve  # preview at http://127.0.0.1:8000
```
