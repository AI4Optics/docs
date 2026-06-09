---
description: How DeepLens Hyperspectral composes a differentiable DOE, a sensor, and a reconstruction network into a snapshot hyperspectral imaging pipeline — and how the wavelength-dependent PSF encodes spectrum.
---

# Architecture

DeepLens Hyperspectral models the full snapshot-HSI pipeline — diffractive optics, sensor response, and neural reconstruction — as a single differentiable graph in PyTorch. Gradients from the reconstruction loss flow back through the network and into the DOE surface, which is what makes optics–algorithm co-design possible.

## The pipeline

[`HSICamera`](https://github.com/AI4Optics/DeepLens_Hyperspectral/blob/main/src/hsi_camera.py) composes a single-DOE `DiffractiveLens` with an `RGBSensor` into one differentiable capture, paired with a reconstruction network:

```
Spectral cube ──▶ [ DiffractiveLens ] ──▶ blurred cube ──▶ [ RGBSensor ] ──▶ RGB capture ──▶ [ NAFNet ] ──▶ Reconstructed cube
 (B, 31, H, W)      per-λ wave-optics PSF    (B, 31, H, W)     response curves   (B, 3, H, W)     reconstruction   (B, 31, H, W)
 400–700 nm         + PSF convolution                          (3 channels)                      network
```

- **Spectral cube** — a ground-truth hyperspectral image with 31 bands spanning 400–700 nm (from the [CAVE](https://www.cs.columbia.edu/CAVE/databases/multispectral/) dataset).
- **DOE optics** — `DiffractiveLens` computes a wavelength-dependent PSF for each band by scalar wave propagation, then convolves each band with its PSF (`HSICamera.render_lens`).
- **Sensor** — `RGBSensor` integrates the blurred spectral cube against the camera's measured spectral response curves (FLIR BFS-U3-200S7C-C), producing a 3-channel RGB raw capture.
- **Network** — a `NAFNet` (`in_chan=3`, `out_chan=31`) reconstructs the full 31-band cube from the RGB capture.

`HSICamera.render(data_dict)` returns `(rgb_capture, spectral_cube)` — the network's input and its reconstruction target. The helper `HSICamera.spectral2rgb` maps a 31-band cube to RGB via the same sensor response, for visualization.

## Spectral encoding by a wavelength-dependent PSF

The DOE is what makes snapshot HSI possible. A diffractive surface with height map $h(x, y)$ imposes a phase on the incident wavefront that depends on wavelength:

$$
\phi(x, y; \lambda) = \frac{2\pi}{\lambda}\,\bigl(n(\lambda) - 1\bigr)\,h(x, y),
$$

and the PSF is the squared magnitude of the field propagated to the sensor,

$$
\mathrm{PSF}(\lambda) = \bigl\lvert\, \mathcal{P}_z\{\, A(x, y)\, e^{\,i\,\phi(x, y;\,\lambda)} \,\}\, \bigr\rvert^2,
$$

where $A$ is the aperture and $\mathcal{P}_z$ is free-space propagation. Because $\phi \propto (n(\lambda) - 1)/\lambda$, the PSF changes with wavelength — so each spectral band leaves a distinct spatial signature in the captured image, and the reconstruction network learns to invert that code.

The strength and *conditioning* of this encoding is set entirely by the DOE design. A well-conditioned encoder spreads the bands into separable signatures; a poorly-conditioned one collapses them, and no amount of network capacity can recover what the optics threw away. See *"Limitations of Data-Driven Spectral Reconstruction: An Optics-Aware Analysis"* ([code](https://github.com/vccimaging/OpticsAwareHSI-Analysis)) for an analysis.

## Diffractive encoders

All three encoders are `DiffractiveSurface` types in DeepLens, selected purely by the lens-config JSON (`camera.lens_file`):

| `type` in JSON | Reference | Learnable parameters | Spectral PSF |
|---|---|---|---|
| `pixel2d` | freeform | full per-pixel height map | compact, wavelength-scaled focus |
| `diffractedrotation` | Jeon et al. 2019 | focal length only (fixed-form) | **rotates** with wavelength |
| `rotationallysymmetric` | Dun et al. 2020 | 1-D radial profile | concentric rings, chromatic focus |

See the [Diffractive Surfaces](examples/diffractive_surfaces.md) example for the phase maps and spectral PSFs of all three.

## Fixed encoder vs. end-to-end design

The same camera and network support two workflows, differing only in *what* is optimized.

### Fixed-DOE reconstruction

The DOE is frozen; only the network trains. Use it to benchmark a known optical encoder.

```python
self.camera = HSICamera(lens_file=..., sensor_file=...)   # DOE frozen
self.optimizer = optim.AdamW(self.model.parameters(), lr=lr)
```

### End-to-end design

The DOE's learnable parameters join the optimizer alongside the network, so the optics are co-designed with the reconstructor.

```python
self.doe = self.camera.lens.surfaces[0]
doe_param_groups = self.doe.get_optimizer_params(lr=doe_lr)   # surface-agnostic
self.optimizer = optim.AdamW(
    [{"params": self.model.parameters(), "lr": lr}] + doe_param_groups
)
```

`get_optimizer_params()` is surface-agnostic — each `DiffractiveSurface` exposes whatever it can learn. A `RotationallySymmetric` or `Pixel2D` surface is a meaningful design target; a `DiffractedRotation` exposes only its focal length, so it is used as a *fixed* encoder rather than a design target.

## Code structure

```
DeepLens_Hyperspectral/
├── 0_hello_deeplens_hsi.py        # Build an HSICamera, visualize DOE + spectral PSF
├── 1_hsi_reconstruction.py        # Train NAFNet against a FIXED DOE
├── 2_end2end_hsi.py               # Jointly design DOE + network (end-to-end)
├── 2_hsi_diffractive_surfaces.py  # Render spectral PSFs of the DOE encoders
├── hsi_dataset.py                 # CaveDataset (CAVE hyperspectral images)
├── configs/                       # Experiment configs (DOE + network + training)
├── lenses/paraxiallens/           # DOE lens files (pixel2d, diffracted_rotation, ...)
├── sensors/flir/                  # Sensor response curves
└── src/
    ├── hsi_camera.py              # HSICamera — DOE + sensor render pipeline
    ├── camera.py                  # Renderer base class
    ├── deeplens/                  # Vendored DeepLens optics engine
    ├── sensor/                    # RGBSensor + ISP
    ├── network/                   # NAFNet reconstruction network
    └── utils.py                   # Seeding, metrics (PSNR/SSIM), logging
```

!!! note "Built on DeepLens"
    The optics engine under `src/deeplens/` is the [DeepLens](../deeplens/index.md)
    library. For the full optics reference — `DiffractiveLens`, diffractive
    surfaces, and PSF computation — see the
    [DeepLens documentation](../deeplens/index.md).

## Next steps

- [Examples](examples/index.md) — from a first HSI camera to end-to-end design
- [Diffractive Surfaces](examples/diffractive_surfaces.md) — the three spectral encoders
- [DeepLens docs](../deeplens/index.md) — the underlying differentiable optics
