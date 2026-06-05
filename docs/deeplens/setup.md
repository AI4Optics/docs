# Setup

This page takes you from a clean machine to a working DeepLens environment and
your first successful lens simulation. The recommended way to work with DeepLens
is to clone the repository and develop inside it — see [Installation](installation.md)
for the full set of options.

## Prerequisites

- **Python >= 3.12**
- **Conda** (Miniconda or Anaconda) for environment management
- **NVIDIA GPU with CUDA** — recommended. DeepLens also runs on CPU, but ray
  tracing and wave propagation are much faster on a GPU.

## 1. Clone the repository

```bash
git clone https://github.com/vccimaging/DeepLens.git
cd DeepLens
```

## 2. Create the conda environment

```bash
conda create -n deeplens python=3.12
conda activate deeplens
```

## 3. Install PyTorch

Install PyTorch first so it picks up the right build for your platform:

```bash
# Linux / macOS
pip install torch torchvision

# Windows (CUDA 12.8 build)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

## 4. Install the remaining dependencies

```bash
pip install -r requirements.txt
```

## 5. Verify the install

Running from the repository root, the local `deeplens/` package is importable
directly — no `pip install` step is required for the clone-and-develop workflow.

```python
import torch
from deeplens import GeoLens

print(torch.cuda.is_available())  # True if a CUDA GPU is available
```

## 6. Run your first demo

`0_hello_geolens.py` loads a cellphone lens, runs the classical optical analyses
(layout, spot, MTF, distortion, vignetting), and renders an image with both ray
tracing and PSF-map simulation:

```bash
python 0_hello_geolens.py
```

On success, these files are written to the repository root:

| File | Description |
|------|-------------|
| `lens.png` | Lens cross-section layout |
| `lens_spot.png` | Spot diagram |
| `lens_mtf.png` | MTF curves |
| `lens_distortion.png` | Distortion plot |
| `lens_vignetting.png` | Relative illumination (vignetting) |
| `render_ray_tracing.png` | Image rendered by ray tracing |
| `render_psf_map.png` | Image rendered by PSF-map convolution |

See [Hello GeoLens](examples/hello_geolens.md) for a line-by-line walkthrough of
this script.

## Troubleshooting

**`torch.cuda.is_available()` returns `False`:**
Install a CUDA-enabled PyTorch build for your platform from
[pytorch.org](https://pytorch.org/get-started/locally/). DeepLens still runs on
CPU, just slower.

**`FileNotFoundError` for a dataset file:**
Run the script from the repository root so relative paths such as
`./datasets/lenses/cellphone/cellphone80deg.json` resolve correctly.

**`ModuleNotFoundError: No module named 'deeplens'`:**
Make sure the `deeplens` environment is active and that you are running from the
repository root (or that you installed the package with `pip install -e .`).

## Next steps

- [Quickstart](quickstart.md) — the core API workflow in a few lines
- [Architecture](architecture.md) — how the simulator is organized
- [Installation](installation.md) — other ways to install and use DeepLens
