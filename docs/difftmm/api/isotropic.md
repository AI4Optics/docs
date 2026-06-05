# Isotropic Solver

The standard **2×2 transfer matrix method** for isotropic multi-layer films. This
is the fastest solver in DiffTMM (~190× faster than NumPy TMM) and the right
default whenever every layer is isotropic. It computes the complex Fresnel
coefficients `(ts, tp, rs, rp)` with full phase, and supports bidirectional
propagation — angles in `[0, π/2]` are forward (top → bottom), angles in
`[π/2, π]` are reverse (bottom → top).

::: difftmm.IsotropicFilmSolver

## Functional API

The solver is a thin wrapper around a pure function. Use `create_jones_matrix_isotropic`
directly when you want to differentiate through the film stack without holding
solver state — for example, when the thicknesses are an external
`torch.nn.Parameter` in an [inverse-design](../examples/inverse_design.md) loop.

::: difftmm.create_jones_matrix_isotropic
