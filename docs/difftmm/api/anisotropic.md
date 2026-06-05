# Anisotropic Solver

The general **4×4 transfer matrix method**, which handles both isotropic and
**anisotropic (birefringent)** media. Use it when one or more layers have
direction-dependent refractive index; each such layer is given as a
`(mat_x, mat_y, mat_z)` tuple of per-axis indices. It is more general (and
heavier) than the [isotropic 2×2 solver](isotropic.md) — for fully isotropic
stacks, prefer the isotropic solver for speed and lower memory.

!!! note "`AnisotropicFilmSolver` is an alias"
    `difftmm.AnisotropicFilmSolver` is an alias for `FilmSolver`; both names refer
    to the same class. The two share the constructor and `simulate(theta, wvln)`
    signature of the isotropic solver, returning complex `(ts, tp, rs, rp)`.

::: difftmm.FilmSolver

## Functional API

Lower-level entry point used by `FilmSolver.simulate()`. It builds the 4×4 Jones
matrix for an anisotropic stack expressed in the angle-of-incidence / azimuth
(AOIAz) frame.

::: difftmm.create_jones_matrix_AOIAz
