# Quickstart

This guide walks through the two core DiffTMM workflows: **forward simulation** of
a film stack's optical response, and **inverse design** of its layer thicknesses.
Both run on GPU when available and fall back to CPU otherwise. If you haven't
installed DiffTMM yet, start with [Setup](setup.md).

## Forward Simulation

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

The coefficients are complex amplitudes — square the magnitude for power. To use
real dispersive materials, pass names instead of numbers (`mat_in="air"`,
`mat_ls=["TiO2", "SiO2"]`); see [Real Materials](examples/real_materials.md).

## Inverse Design

Because `simulate()` is differentiable, you can recover unknown thicknesses by
matching target coefficients with gradient descent. When the thicknesses live
outside the solver (here a `torch.nn.Parameter`), drive the stack through the
functional core [`create_jones_matrix_isotropic`](api/isotropic.md#functional-api):

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

## Next steps

- [Architecture](architecture.md) — how the solvers, functional core, and materials fit together
- [API Reference](api/index.md) — full class and function documentation
- [Examples](examples/index.md) — forward simulation, inverse design, real materials, and benchmarks
