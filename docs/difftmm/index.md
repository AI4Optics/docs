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
validate accuracy — see the [Benchmarks](examples/benchmarks.md) page.

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

## Getting Started

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Setup__

    ---

    Install DiffTMM and run your first thin-film simulation.

    [:octicons-arrow-right-24: Set up DiffTMM](setup.md)

-   :material-rocket-launch-outline:{ .lg .middle } __Quickstart__

    ---

    Forward simulation and inverse design in a few lines of code.

    [:octicons-arrow-right-24: Get started](quickstart.md)

-   :material-sitemap-outline:{ .lg .middle } __Architecture__

    ---

    How the solvers, functional core, and materials fit together.

    [:octicons-arrow-right-24: Understand the design](architecture.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Full class and function documentation for the solvers and materials.

    [:octicons-arrow-right-24: Browse the API](api/index.md)

-   :material-flask-outline:{ .lg .middle } __Examples__

    ---

    Forward simulation, inverse design, real materials, and benchmarks.

    [:octicons-arrow-right-24: See examples](examples/index.md)

</div>

## Citation

If you use DiffTMM in your research, please cite the accompanying paper:

> X. Yang, Z. Liu, Z. Nie, Q. Fan, Z. Shi, J. Bonar, and W. Heidrich,
> "End-to-end differentiable design of geometric waveguide displays,"
> *arXiv preprint* [arXiv:2601.04370](https://arxiv.org/abs/2601.04370) (2026).

DiffTMM is released under the [Apache License 2.0](https://github.com/AI4Optics/DiffTMM/blob/main/LICENSE).
