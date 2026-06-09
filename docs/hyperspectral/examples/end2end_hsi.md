---
description: Jointly optimize a diffractive optical element together with the NAFNet reconstructor for snapshot hyperspectral imaging.
---

# End-to-End Design

**Script:** `2_end2end_hsi.py`

Design the optics and the algorithm *together*. The DOE's learnable parameters join the optimizer alongside the network, so gradients from the reconstruction loss reshape the DOE — the optics learn to encode exactly what the reconstructor can best invert.

## Run

```bash
# RotationallySymmetric DOE (default); swap the config to choose another surface
python 2_end2end_hsi.py --config configs/2_end2end_hsi_rotational_symmetric.yml
```

## How it works

The camera is built **before** the network so the DOE's parameters can join the optimizer:

```python
self.camera = HSICamera(lens_file=..., sensor_file=...)
self.doe = self.camera.lens.surfaces[0]

# surface-agnostic: each DiffractiveSurface exposes its own learnable params
doe_param_groups = self.doe.get_optimizer_params(lr=doe_lr)
self.optimizer = optim.AdamW(
    [{"params": self.model.parameters(), "lr": lr}] + doe_param_groups
)
```

The training loop is identical to [fixed-DOE reconstruction](hsi_reconstruction.md) — render, reconstruct, L1 loss — but now `loss.backward()` updates both the network *and* the DOE. The script snapshots the DOE phase map before and after training, and reports the baseline-vs-designed validation PSNR along with how far the DOE moved.

- **Joint optimizer** — network at `lr = 1e-4`, DOE at `doe_lr = 0.01` (`AdamW`).
- **Surface-agnostic** — point `camera.lens_file` at any learnable surface (`RotationallySymmetric`, `Pixel2D`).

## Next steps

- [Diffractive Surfaces](diffractive_surfaces.md) — the encoders you can design
- [HSI Reconstruction](hsi_reconstruction.md) — train a network against a fixed encoder
