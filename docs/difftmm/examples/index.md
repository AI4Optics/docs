# Examples

The examples map onto DiffTMM's two main use cases — **forward simulation** of a
film stack's optical response, and **inverse design** of layer thicknesses via
differentiable optimization. Each example corresponds to a notebook in the
repository root.

For accuracy validation against the reference NumPy TMM library and speed/memory
comparisons, see the [Benchmarks](benchmarks.md) page.

## Forward Simulation

Compute the optical response of a known film stack across angle and wavelength,
including real dispersive materials and thick incoherent substrates.

| Example | Notebook | Description |
|---|---|---|
| [Forward Simulation](forward_simulation.md) | `1_forward_simu.ipynb` | Fresnel coefficients vs. angle and wavelength with the isotropic 2×2 solver |
| [Real Materials](real_materials.md) | `3_real_materials.ipynb` | Dispersive `n(λ)`, `k(λ)` materials — AR coatings and surface plasmon resonance |
| [Incoherent Films](incoherent_films.md) | `4_incoherent_film.ipynb` | Thick substrates without unphysical Fabry–Perot ripples |

## Inverse Design

Optimize the film stack with PyTorch autograd, so layer thicknesses are designed
end-to-end to match a target optical response.

| Example | Notebook | Description |
|---|---|---|
| [Inverse Design](inverse_design.md) | `2_inverse_design.ipynb` | Recover five unknown layer thicknesses to sub-nanometer accuracy |
