# Setup

This page takes you from a clean machine to a working DiffTMM environment and
your first thin-film simulation.

## Prerequisites

- **Python ≥ 3.9**
- **PyTorch ≥ 2.0** — the only hard dependency of the solvers.
- **A CUDA-capable GPU** — recommended for batched / large sweeps, but optional.
  DiffTMM runs on CPU too; just set `device="cpu"`.

`numpy`, `scipy`, and `matplotlib` are only needed for the example notebooks and
benchmarks, not for the solvers themselves.

## 1. Clone the repository

```bash
git clone https://github.com/AI4Optics/DiffTMM.git
cd DiffTMM
```

## 2. Create an environment

Any virtual environment works. With conda:

```bash
conda create -n difftmm python=3.11
conda activate difftmm
```

## 3. Install PyTorch

Install PyTorch first so it picks the right build for your platform:

```bash
# Linux / macOS
pip install torch

# Windows / specific CUDA builds — see https://pytorch.org/get-started/locally/
pip install torch --index-url https://download.pytorch.org/whl/cu128
```

## 4. Install DiffTMM

DiffTMM is a packaged project (`difftmm`), so an editable install makes it
importable from anywhere while your local edits still take effect:

```bash
pip install -e .
```

Optional extras pull in the tooling for notebooks, benchmarks, or development:

```bash
pip install -e ".[notebooks]"    # numpy, scipy, matplotlib, jupyter
pip install -e ".[benchmarks]"   # numpy, scipy, matplotlib
pip install -e ".[dev]"          # pytest, ruff, build, twine
```

!!! tip "Clone-and-develop without installing"
    Running scripts from the repository root, the local `difftmm/` package is
    importable directly — so for quick experiments you can skip the install and
    just `pip install torch` (plus `numpy`/`matplotlib` for plotting).

## 5. Verify the install

```python
import torch
from difftmm import IsotropicFilmSolver, list_materials

print(torch.cuda.is_available())     # True if a CUDA GPU is available
print(len(list_materials()), "materials available")
```

## 6. Run your first simulation

This computes the Fresnel coefficients of a three-layer coating across a few
wavelengths and angles, on GPU if available:

```python
import torch
from difftmm import IsotropicFilmSolver

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

solver = IsotropicFilmSolver(
    mat_in=1.5,                          # incident medium
    mat_out=1.5,                         # exit medium
    mat_ls=[2.10, 1.46, 2.10],           # Ta2O5 | SiO2 | Ta2O5
    thickness_ls=[0.080, 0.120, 0.080],  # thicknesses in um
    device=device,
)

angles = torch.linspace(0, 1.2, 100, device=device)         # radians
ts, tp, rs, rp = solver.simulate(theta=angles, wvln=[0.45, 0.55, 0.65])

print(ts.shape)                          # (1, 3, 100) = (batch, n_wvlns, n_angles)
T_s = ts.abs() ** 2                      # transmittance (s-pol)
R_s = rs.abs() ** 2                      # reflectance  (s-pol)
print("T+R at normal incidence:", (T_s + R_s)[0, :, 0])  # ≈ 1 for a lossless stack
```

## 7. Run the example notebooks

The four notebooks in the repository root mirror the [Examples](examples/index.md)
section. With the `notebooks` extra installed:

```bash
jupyter notebook 1_forward_simu.ipynb
```

| Notebook | Topic |
|---|---|
| `1_forward_simu.ipynb` | [Forward simulation](examples/forward_simulation.md) |
| `2_inverse_design.ipynb` | [Inverse design](examples/inverse_design.md) |
| `3_real_materials.ipynb` | [Real materials](examples/real_materials.md) |
| `4_incoherent_film.ipynb` | [Incoherent films](examples/incoherent_films.md) |

## Run the tests (optional)

With the `dev` extra installed, run the test suite from the repository root:

```bash
pytest
```

## Troubleshooting

**`torch.cuda.is_available()` returns `False`:**
Install a CUDA-enabled PyTorch build for your platform from
[pytorch.org](https://pytorch.org/get-started/locally/). DiffTMM still runs on
CPU — pass `device="cpu"` to any solver.

**`ModuleNotFoundError: No module named 'difftmm'`:**
Activate the environment and either `pip install -e .` from the repository root,
or run your script from the repository root so the local `difftmm/` package is on
the path.

**Wildly oscillating spectra on a thick layer:**
A fully-coherent solver produces dense Fabry–Perot ripples on substrates thicker
than the coherence length. Use the
[`IncoherentIsotropicFilmSolver`](api/incoherent.md) and mark the thick layer
incoherent — see [Incoherent Films](examples/incoherent_films.md).

## Next steps

- [Architecture](architecture.md) — how the solvers, functional core, and materials fit together
- [API Reference](api/index.md) — full class and function documentation
- [Examples](examples/index.md) — forward simulation, inverse design, real materials, and benchmarks
