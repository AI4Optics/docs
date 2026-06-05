# DiffTMM

DiffTMM is a differentiable [Transfer Matrix Method](https://en.wikipedia.org/wiki/Transfer-matrix_method_(optics))
(TMM) solver for multi-layer thin films, built on PyTorch. It models how light
reflects and transmits through a stack of optical coatings — and because the
whole calculation is differentiable, you can run gradient-based **inverse design**
to recover layer thicknesses or optimize a coating for a target spectral response.

DiffTMM supports two main use cases:

- **Forward simulation** — compute the Fresnel coefficients (`ts`, `tp`, `rs`, `rp`)
  of a film stack across angle and wavelength, on GPU and in batch.
- **Inverse design** — optimize layer thicknesses (and stack geometry) end-to-end
  with PyTorch autograd to match measured or target optical properties.

---

## Why DiffTMM

The transfer matrix method is the standard tool for multi-layer thin-film optics,
but classic implementations are CPU-only and non-differentiable. DiffTMM
reimplements TMM in PyTorch so the entire pipeline is GPU-accelerated, batched,
and autograd-friendly.

| Feature | NumPy TMM | DiffTMM |
|---|---|---|
| Differentiable (autograd) | No | **Yes** |
| GPU acceleration | No (CPU only) | **Yes** (CUDA) |
| Batch processing | No (sequential) | **Yes** (vectorized) |
| Anisotropic materials | No | **Yes** (4×4 transfer matrix) |
| Speed (batch = 16) | 1× baseline | **~190×** (isotropic 2×2), **~134×** (anisotropic 4×4) |

Benchmarks are measured against the reference NumPy library
[sbyrnes321/tmm](https://github.com/sbyrnes321/tmm), which DiffTMM also uses to
validate accuracy (surface plasmon resonance, energy conservation, reciprocity).

---

## Solvers

DiffTMM ships three solvers that share the same `Solver(...).simulate(theta, wvln)`
interface:

| Solver | Method | Use it for |
|---|---|---|
| [`IsotropicFilmSolver`](api/isotropic.md) | 2×2 transfer matrix | Isotropic stacks — fastest path (~190×) |
| [`FilmSolver`](api/anisotropic.md) (alias `AnisotropicFilmSolver`) | 4×4 transfer matrix | Anisotropic / birefringent media (also handles isotropic) |
| [`IncoherentIsotropicFilmSolver`](api/incoherent.md) | 2×2 + incoherent layers | Stacks with thick substrates (≫ coherence length) |

Refractive indices can be plain numbers, complex values (with loss), or real
[material names](api/material.md) (`"N-BK7"`, `"SiO2"`, `"Ag"`, …) resolved to
wavelength-dependent dispersion from bundled catalogs.

---

## Code Structure

```
difftmm/
├── __init__.py                     # Public API
├── film_solver_isotropic.py        # IsotropicFilmSolver — 2×2 TMM (fast)
├── film_solver_anisotropic.py      # FilmSolver — 4×4 TMM (anisotropic / general)
├── film_solver_incoherent.py       # IncoherentIsotropicFilmSolver — thick substrates
└── material/                       # Wavelength-dependent materials
    ├── materials.py                #   Material class + list_materials()
    └── catalogs/                   #   Bundled glass (AGF) + thin-film n+k tables
```

---

## Installation

**Prerequisites:** Python ≥ 3.9, PyTorch ≥ 2.0 (a CUDA-capable GPU is recommended
but not required — DiffTMM runs on CPU too).

```bash
git clone https://github.com/AI4Optics/DiffTMM.git
cd DiffTMM
pip install torch numpy matplotlib scipy
```

The solvers require only `torch`; `numpy`, `matplotlib`, and `scipy` are used by
the example notebooks and benchmarks.

---

## Quickstart

### Forward Simulation

Define a film stack by its refractive indices and thicknesses, then compute the
Fresnel coefficients across angle and wavelength:

```python
import torch
from difftmm import IsotropicFilmSolver

# Film stack: Glass | Ta2O5 | SiO2 | Ta2O5 | Glass
solver = IsotropicFilmSolver(
    mat_in=1.5,                          # incident medium
    mat_out=1.5,                         # exit medium
    mat_ls=[2.10, 1.46, 2.10],           # interior layer indices
    thickness_ls=[0.080, 0.120, 0.080],  # thicknesses in um
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
)

angles = torch.linspace(0, 1.2, 100, device=solver.device)  # radians
ts, tp, rs, rp = solver.simulate(theta=angles, wvln=[0.45, 0.55, 0.65])
# Each coefficient has shape (batch_size, n_wvlns, n_angles)

# Power coefficients (transmittance / reflectance):
T_s = ts.abs() ** 2
R_s = rs.abs() ** 2
```

### Inverse Design

Because `simulate()` is differentiable, you can recover unknown thicknesses by
matching target coefficients with gradient descent:

```python
import torch
from difftmm import create_jones_matrix_isotropic

n_list = torch.tensor([2.10, 1.46, 2.10, 1.46, 2.10], device="cuda")
d_param = torch.nn.Parameter(torch.randn(5, device="cuda") * 0.5)

def param_to_thickness(p):
    return torch.sigmoid(p) * 0.19 + 0.01  # map to [0.01, 0.20] um

optimizer = torch.optim.Adam([d_param], lr=0.02)
for step in range(3000):
    optimizer.zero_grad()
    d = param_to_thickness(d_param)
    pred = forward_tmm(n_list, d, n_in=1.0, n_out=1.52, inp=inp)
    diff = pred - target
    loss = (diff.real ** 2 + diff.imag ** 2).mean()
    loss.backward()
    optimizer.step()
```

See the [Inverse Design example](examples/inverse_design.md) for a complete,
runnable walkthrough that recovers five layer thicknesses to sub-nanometer
accuracy.

---

## Next Steps

- [API Reference](api/index.md) — solver and material class documentation
- [Examples](examples/index.md) — forward simulation, inverse design, real materials, and thick substrates
- [Contribute](../contribute.md) — development setup and guidelines

## Citation

If you use DiffTMM in your research, please cite the accompanying paper:

> X. Yang, Z. Liu, Z. Nie, Q. Fan, Z. Shi, J. Bonar, and W. Heidrich,
> "End-to-end differentiable design of geometric waveguide displays,"
> *arXiv preprint* [arXiv:2601.04370](https://arxiv.org/abs/2601.04370) (2026).

DiffTMM is released under the [Apache License 2.0](https://github.com/AI4Optics/DiffTMM/blob/main/LICENSE).
