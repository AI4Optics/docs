# Installation

There are several ways to use DeepLens. Which one fits depends on whether you
want to **extend the optics engine** or simply **call it as a library**.

## Clone and develop (recommended)

DeepLens is a research framework, and the intended workflow is to design custom
optical systems by writing scripts *inside* a clone of the repository — next to
the bundled examples (`0_hello_geolens.py`, `1_design_geolens.py`, …). You get
the full source to read, extend, and modify, which is what you want when
implementing new surfaces, lens models, or end-to-end pipelines.

```bash
git clone https://github.com/vccimaging/DeepLens.git
cd DeepLens
# create the environment, then write your own script in the repo root
```

When you run a script from the repository root, `import deeplens` resolves to the
local `deeplens/` package, so your edits take effect immediately with no reinstall.

## Install from PyPI

To use DeepLens as a dependency in your own project, install the published
`deeplens-core` package:

```bash
pip install deeplens-core
```

```python
from deeplens import GeoLens
```

Use this when you want the stable API as a library and don't need to modify the
source.

## Install from source

Install the latest (unreleased) code directly from GitHub:

```bash
pip install git+https://github.com/vccimaging/DeepLens.git
```

Or clone and install in editable mode, which combines a clone with a proper
package install so `deeplens` is importable from anywhere while your local edits
still take effect:

```bash
git clone https://github.com/vccimaging/DeepLens.git
cd DeepLens
pip install -e .
```

## Requirements

- Python >= 3.12
- PyTorch (install a CUDA build for GPU acceleration — see [Setup](setup.md))
- A CUDA-capable GPU is recommended but not required

## Verify the install

```python
import torch
from deeplens import GeoLens

print(torch.cuda.is_available())  # True if a CUDA GPU is available
```
