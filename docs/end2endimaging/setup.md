# Setup

This page takes you from a clean machine to a working End2endImaging environment
and your first camera simulation. The intended workflow is to clone the
repository and develop inside it, next to the bundled example scripts
(`0_hello_deeplens.py`, `1_end2end_lens_design.py`, …).

## Prerequisites

- **Python ≥ 3.12**
- **PyTorch ≥ 2.0** (with `torchvision`)
- **Conda** (Miniconda or Anaconda) for environment management
- **A GPU is recommended.** End2endImaging auto-selects the best device —
  CUDA, Apple MPS, or CPU — so it runs anywhere, just faster on a CUDA GPU.

## 1. Clone the repository

```bash
git clone https://github.com/vccimaging/End2endImaging
cd End2endImaging
```

## 2. Create the conda environment

```bash
conda create -n end2end_env python=3.12
conda activate end2end_env
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

This pulls in the imaging, training, and notebook tooling — OpenCV,
scikit-image, matplotlib, `transformers`, `lpips`, `einops`, `timm`, `wandb`,
`tqdm`, and Jupyter.

Or recreate the full environment from the lockfile:

```bash
conda env create -f environment.yml -n end2end_env
```

## 5. Verify the install

Running from the repository root, the local `end2end_imaging/` package is
importable directly — no separate install step is required.

```python
import torch
from end2end_imaging import Camera, init_device

device = init_device()                  # prints and returns CUDA / MPS / CPU
print(torch.cuda.is_available())        # True if a CUDA GPU is available
```

## 6. Run your first demo

`0_hello_deeplens.py` is the quickest end-to-end check — it exercises the
differentiable optics engine bundled inside End2endImaging:

```bash
python 0_hello_deeplens.py
```

To simulate a full camera capture, create a `Camera` (lens + sensor) and render
an input image through it:

```python
from end2end_imaging import Camera

camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)

# data_dict holds the sRGB image, ISO, and field position (see Quickstart)
data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch")
```

See [Computational Photography](examples/comp_photography.md) for a full training
example.

## Example scripts

The numbered scripts in the repository root map onto the
[Examples](examples/index.md) section:

| Script | Topic |
|---|---|
| `0_hello_deeplens.py` | First optics demo |
| `1_end2end_lens_design.py` | [End-to-end lens design](examples/end2end_lens_design.md) |
| `4_tasklens_img_classi.py` | [Task-driven lens design](examples/task_driven.md) |
| `7_comp_photography.py` | [Computational photography](examples/comp_photography.md) |
| `8_defocus_deblur.py` | [Defocus deblur](examples/defocus_deblur.md) |

## Troubleshooting

**`torch.cuda.is_available()` returns `False`:**
Install a CUDA-enabled PyTorch build for your platform from
[pytorch.org](https://pytorch.org/get-started/locally/). End2endImaging still
runs on CPU (or Apple MPS), just slower — `init_device()` selects automatically.

**`FileNotFoundError` for a dataset, lens, or sensor file:**
Run scripts from the repository root so relative paths such as
`datasets/lenses/camera/rf50mm_f1.8.json` resolve correctly.

**`ModuleNotFoundError: No module named 'end2end_imaging'`:**
Activate the `end2end_env` environment and run from the repository root, where
the local `end2end_imaging/` package is importable.

## Next steps

- [Architecture](architecture.md) — how the optics, sensor, and network stages compose
- [API Reference](api/index.md) — camera, sensor, and network class documentation
- [Examples](examples/index.md) — image simulation, defocus deblur, and end-to-end design
