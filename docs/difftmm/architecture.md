# Architecture

DiffTMM is a differentiable thin-film library built on PyTorch. The whole
calculation — Snell's law, Fresnel coefficients, layer propagation, the transfer
matrix product — is expressed in differentiable tensor ops, so gradients flow
from the output Fresnel coefficients back to the layer thicknesses (and any other
tensor input). That is what makes gradient-based inverse design possible.

The code is organized into three parts: a **functional core** of pure TMM
functions, a thin layer of **solver classes** that hold the stack geometry and
the optimizable thicknesses, and a **materials** subsystem that supplies
wavelength-dependent refractive indices.

## Package layout

```
difftmm/
├── __init__.py                  Public API (re-exports the solvers + materials)
│
├── film_solver_isotropic.py     IsotropicFilmSolver (2×2)
│                                  + create_jones_matrix_isotropic()   ← functional core
├── film_solver_anisotropic.py   FilmSolver / AnisotropicFilmSolver (4×4)
│                                  + create_jones_matrix_AOIAz()       ← functional core
├── film_solver_incoherent.py    IncoherentIsotropicFilmSolver (2×2 + incoherent layers)
│                                  + create_intensity_RT_isotropic()   ← functional core
│
└── material/
    ├── materials.py             Material + list_materials() + AGF/JSON catalog loaders
    └── catalogs/                CDGM / SCHOTT / MISC / PLASTIC2022 (.AGF) + thin_film_materials.json

tmm_numpy/                       Reference NumPy TMM (sbyrnes321/tmm) — accuracy validation
benchmarks/                      Accuracy + speed/memory scripts
tests/                           Pytest suite
*.ipynb                          Example notebooks
```

## Two layers: solvers and the functional core

Each solver is a thin, stateful wrapper around a **pure function** that does the
actual transfer-matrix math. The solver holds the stack description and the
optimizable thicknesses and offers a convenient `simulate(theta, wvln)` call; the
function is stateless and takes every quantity explicitly.

| Solver (stateful) | Functional core (pure) | Returns |
|---|---|---|
| [`IsotropicFilmSolver`](api/isotropic.md) | `create_jones_matrix_isotropic()` | complex `ts, tp, rs, rp` |
| [`FilmSolver`](api/anisotropic.md) | `create_jones_matrix_AOIAz()` | complex `ts, tp, rs, rp` |
| [`IncoherentIsotropicFilmSolver`](api/incoherent.md) | `create_intensity_RT_isotropic()` | real `Rs, Rp, Ts, Tp` |

Use the **solver** for ordinary forward simulation and for optimizing the
thicknesses it owns. Reach for the **function** when the thicknesses live outside
the solver — e.g. as a `torch.nn.Parameter` or the output of a network — which is
the natural fit for [inverse design](examples/inverse_design.md). Both paths share
the same math and are equally differentiable.

## Solver class hierarchy

```
IsotropicFilmSolver                     2×2 TMM, isotropic, complex amplitudes
└── IncoherentIsotropicFilmSolver       adds per-layer coherence (c_list); returns real power

FilmSolver  ( = AnisotropicFilmSolver)  4×4 TMM, anisotropic/general, complex amplitudes
```

`IncoherentIsotropicFilmSolver` **subclasses** `IsotropicFilmSolver`: it reuses
the parent's constructor, thickness handling, and checkpoint I/O, adds a `c_list`
that marks each interior layer coherent (`'c'`) or incoherent (`'i'`), and
overrides `simulate()` to return real power coefficients (phase is discarded by
design). `FilmSolver` is an independent 4×4 implementation; `AnisotropicFilmSolver`
is simply an alias for it.

### Shared solver interface

All solvers construct from the same stack description and expose the same methods:

```python
Solver(
    mat_in, mat_out, mat_ls,     # incident medium, exit medium, interior layers
    thickness_ls=None,           # layer thicknesses in um (random if None)
    thickness_min=0.0,           # thickness bounds in um
    thickness_max=0.2,
    batch_size=1,                # number of film stacks evaluated in parallel
    sigmoid_param=False,         # thickness parameterization (see below)
    device=...,
)
```

| Method | Purpose |
|---|---|
| `simulate(theta, wvln)` / `__call__` | Evaluate the stack at angles (rad) and wavelengths (µm) |
| `get_film_thickness()` | Current physical thicknesses `(batch, n_layers)` in µm |
| `to(device)` | Move the solver (and its materials) to a device |
| `save_ckpt(path)` / `load_ckpt(path)` | Persist / restore thicknesses + material specs |

## Differentiable thicknesses

The optimizable state of a solver is not the thickness directly but an internal
`film_params` tensor. `get_film_thickness()` maps it to a physical thickness in
micrometers, clamped to `[thickness_min, thickness_max]`:

- **Linear** (default) — `film_params` is the normalized thickness, clamped to the
  valid range.
- **Sigmoid** (`sigmoid_param=True`) — thickness is `sigmoid(film_params)` rescaled
  into the range, so the parameter is unconstrained and the thickness can never
  leave its physical bounds during optimization.

Because `get_film_thickness()` is part of the autograd graph, attaching an
optimizer to `film_params` and stepping on a loss computed from `simulate()` is a
complete inverse-design loop. (The default `thickness_max` is `0.2` µm for thin
coatings; the incoherent solver raises it to `1000` µm so substrate-sized layers
fit without extra configuration.)

## Materials

A solver never sees raw numbers internally — every entry of `mat_in`, `mat_out`,
and `mat_ls` is wrapped in a [`Material`](api/material.md), which resolves a
wavelength-dependent **complex** refractive index. `Material` accepts:

| Input | Dispersion model |
|---|---|
| `float` / `complex` (e.g. `1.5`, `2.4 + 0.001j`) | `constant` |
| Sellmeier glass name (e.g. `"N-BK7"`, `"air"`) | `sellmeier` (from bundled AGF catalogs) |
| Thin-film name (e.g. `"SiO2"`, `"TiO2"`, `"Ag"`) | `interp` (complex n+k lookup table) |

`Material.ior(wvln)` returns a `torch.complex64` index — always complex, even for
lossless materials, because beyond the critical angle the layer's `cos θ` becomes
imaginary (evanescent waves). For the 4×4 [`FilmSolver`](api/anisotropic.md), a
birefringent layer is given as a `(mat_x, mat_y, mat_z)` tuple and each axis gets
its own `Material`.

## Physics and conventions

- **2×2 vs 4×4** — the isotropic solver uses the standard 2×2 transfer matrix and
  avoids eigen-decomposition entirely (fast). The anisotropic solver uses the
  general 4×4 formulation needed for birefringent media and full polarization
  (Jones) coupling.
- **Bidirectional propagation** — angles in `[0, π/2]` propagate forward (incident
  → exit medium); angles in `[π/2, π]` propagate in reverse. The reverse case is
  internally converted to an equivalent forward problem with swapped media and
  reversed layer order.
- **Coherent vs incoherent** — coherent solvers track complex amplitudes and
  return `ts, tp, rs, rp`. The incoherent solver groups layers by coherence,
  propagates **intensities** across incoherent boundaries, and returns real power
  `Rs, Rp, Ts, Tp` (the two semi-infinite media are always incoherent).
- **Output convention** — square the magnitude of a coherent amplitude for power
  (`T = |t|²`, `R = |r|²`); the incoherent solver already returns power in `[0, 1]`.

## Validation

DiffTMM bundles the reference NumPy TMM library
([sbyrnes321/tmm](https://github.com/sbyrnes321/tmm)) under `tmm_numpy/` and
checks its solvers against it — surface plasmon resonance, the anisotropic
isotropic-limit, energy conservation, cross-polarization, reciprocity, and the
incoherent thick-substrate case. The scripts and results live on the
[Benchmarks](examples/benchmarks.md) page.

## Next steps

- [API Reference](api/index.md) — full class and function documentation
- [Examples](examples/index.md) — forward simulation, inverse design, real materials, and benchmarks
- [Setup](setup.md) — install DiffTMM and run your first simulation
