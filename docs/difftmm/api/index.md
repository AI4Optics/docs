# API Reference

DiffTMM exposes a small, focused API: a set of **film solvers** that compute the
optical response of a multi-layer stack, plus a **`Material`** class that supplies
wavelength-dependent refractive indices.

Every solver follows the same pattern — construct it with the stack geometry
(incident medium, interior layers, exit medium, thicknesses), then call
`simulate(theta, wvln)` to get the Fresnel coefficients:

```python
solver = Solver(mat_in=1.0, mat_out=1.52, mat_ls=[2.1, 1.46], thickness_ls=[0.08, 0.12])
ts, tp, rs, rp = solver.simulate(theta, wvln)   # shape (batch, n_wvlns, n_angles)
```

All thicknesses are in micrometers (μm), angles in radians, and wavelengths in μm.

<div class="grid cards" markdown>

-   :material-flash:{ .lg .middle } __Isotropic Solver__

    ---

    `IsotropicFilmSolver` — the fast 2×2 transfer matrix method for isotropic
    stacks. The default choice for most coatings (~190× faster than NumPy TMM).

    [:octicons-arrow-right-24: Isotropic Solver](isotropic.md)

-   :material-axis-arrow:{ .lg .middle } __Anisotropic Solver__

    ---

    `FilmSolver` (alias `AnisotropicFilmSolver`) — the general 4×4 transfer matrix
    method for birefringent media, with per-axis `(nx, ny, nz)` layers.

    [:octicons-arrow-right-24: Anisotropic Solver](anisotropic.md)

-   :material-layers-triple:{ .lg .middle } __Incoherent Solver__

    ---

    `IncoherentIsotropicFilmSolver` — marks layers coherent/incoherent so thick
    substrates don't produce unphysical Fabry–Perot ripples.

    [:octicons-arrow-right-24: Incoherent Solver](incoherent.md)

-   :material-palette-swatch:{ .lg .middle } __Materials__

    ---

    `Material` — wavelength-dependent complex refractive index from bundled glass
    (Sellmeier) and thin-film (n+k) catalogs, looked up by name.

    [:octicons-arrow-right-24: Materials](material.md)

</div>

## Output convention

The coherent solvers ([isotropic](isotropic.md), [anisotropic](anisotropic.md))
return **complex amplitude** coefficients `ts, tp, rs, rp` — square the magnitude
for power (`T = |t|²`, `R = |r|²`). The [incoherent solver](incoherent.md) returns
**real power** coefficients `Rs, Rp, Ts, Tp` directly, because incoherent
calculations discard phase by design.
