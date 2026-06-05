# Materials

Real materials have a wavelength-dependent complex refractive index — a real part
`n` (dispersion) and an imaginary part `k` (absorption). The `Material` class
supplies these to the solvers, resolving material names against bundled catalogs.

You rarely construct `Material` objects by hand: every solver auto-wraps the
values you pass in `mat_in`, `mat_out`, and `mat_ls`. You can freely mix:

- **scalars** — `1.5`, `2.10` (constant, lossless index)
- **complex** — `2.40 + 0.001j` (constant index with loss)
- **names** — `"air"`, `"N-BK7"` (Sellmeier glass), `"SiO2"`, `"TiO2"`, `"Ag"`
  (thin-film n+k tables), resolved case-insensitively

```python
from difftmm import IsotropicFilmSolver, Material, list_materials

print(len(list_materials()), "materials available")

solver = IsotropicFilmSolver(
    mat_in="air",
    mat_out="N-BK7",                 # Sellmeier dispersion (AGF catalog)
    mat_ls=["TiO2", "SiO2"],         # n+k tables for thin-film materials
    thickness_ls=[0.06, 0.10],
)
```

Two dispersion models are supported: **Sellmeier** (analytical, real `n`, from the
bundled CDGM / SCHOTT / MISC / PLASTIC AGF glass catalogs) and **linear
interpolation** (complex `n + ik` lookup tables, for thin-film materials). For the
4×4 [anisotropic solver](anisotropic.md), per-axis dispersion is expressed as a
`(mat_x, mat_y, mat_z)` tuple per layer.

## `Material`

::: difftmm.Material

## `list_materials`

::: difftmm.list_materials
