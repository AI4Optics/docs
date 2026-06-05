# Incoherent Solver

A 2×2 isotropic solver that supports **partly-incoherent stacks**. Real coatings
often sit on a thick substrate (e.g. a 1 mm glass slide) that is far thicker than
the source's coherence length, so light reflected from its two surfaces does not
interfere in practice. A fully-coherent solver would produce dense, unphysical
Fabry–Perot ripples; this solver lets you mark each interior layer as coherent
(`'c'`) or incoherent (`'i'`) via a `c_list`.

`IncoherentIsotropicFilmSolver` subclasses [`IsotropicFilmSolver`](isotropic.md)
and shares its constructor and UX, with two differences:

- it takes an extra `c_list` argument (one `'c'`/`'i'` code per interior layer), and
- `simulate()` returns **real power** coefficients `(Rs, Rp, Ts, Tp)` rather than
  complex amplitudes, because incoherent calculations discard phase by design.

The two semi-infinite media are always treated as incoherent. The solver is fully
differentiable through layer thicknesses, so it can be used for inverse design of
stacks that include thick substrates.

!!! note "Isotropic only"
    Incoherent handling is currently available only for the 2×2 isotropic solver.
    Anisotropic incoherent TMM is tracked as future work.

::: difftmm.IncoherentIsotropicFilmSolver
