---
description: DeepLens Hyperspectral is an end-to-end snapshot hyperspectral imaging application built on DeepLens — a diffractive optical element encodes spectral cues into a single RGB capture, and a neural network reconstructs the full spectral cube.
---

# DeepLens Hyperspectral

**DeepLens Hyperspectral** (DeepLens HSI) is an end-to-end **snapshot hyperspectral imaging** application built on the [DeepLens](../deeplens/index.md) framework. A diffractive optical element (DOE) encodes spectral information into a single RGB sensor capture, and a neural network reconstructs the full hyperspectral cube — recovering 31 spectral bands across the visible range (400–700 nm) from one shot.

Because the whole pipeline — DOE wave optics, sensor response, and reconstruction network — is differentiable, the optics and the algorithm can be **co-designed end-to-end**: gradients from the reconstruction loss flow all the way back into the DOE surface.

```
Spectral cube  ──▶  [ DOE optics ]  ──▶  RGB capture  ──▶  [ NAFNet ]  ──▶  Reconstructed cube
  31 bands           DiffractiveLens       3 channels       reconstruction       31 bands
 400–700 nm          wavelength-dependent PSF                network
```

## Two workflows

<div class="grid cards" markdown>

-   :material-image-filter-center-focus:{ .lg .middle } __Fixed-DOE reconstruction__

    ---

    Freeze a known DOE and train only the reconstruction network — to benchmark
    an optical encoder (e.g. an analytic diffracted-rotation DOE) on the CAVE
    dataset.

    [:octicons-arrow-right-24: HSI reconstruction](examples/hsi_reconstruction.md)

-   :material-tune-vertical:{ .lg .middle } __End-to-end design__

    ---

    Jointly optimize the DOE *and* the network. The learnable surface parameters
    join the optimizer alongside the network weights, so the optics learn to
    encode exactly what the reconstructor needs.

    [:octicons-arrow-right-24: End-to-end design](examples/end2end_hsi.md)

</div>

## Key features

- **Differentiable DOE optics** — built on DeepLens's `DiffractiveLens` (scalar wave optics). The DOE's per-wavelength PSF is computed differentiably, so it can be optimized with autograd.
- **Multiple DOE parameterizations** — freeform `Pixel2D`, analytic `DiffractedRotation` (Jeon et al. 2019), and a `RotationallySymmetric` achromat (Dun et al. 2020), all interchangeable through a single lens-config file.
- **Hyperspectral camera model** — `HSICamera` renders a spectral cube into an RGB capture through the DOE and a real sensor's measured response curves (FLIR BFS-U3-200S7C-C).
- **Neural reconstruction** — a `NAFNet` maps the 3-channel capture back to a 31-band spectral cube, trained on the [CAVE](https://www.cs.columbia.edu/CAVE/databases/multispectral/) dataset.

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

## Getting started

<div class="grid cards" markdown>

-   :material-flask-outline:{ .lg .middle } __Examples__

    ---

    Build an HSI camera, visualize the three DOE encoders, train a
    reconstructor, and run end-to-end design.

    [:octicons-arrow-right-24: See examples](examples/index.md)

-   :material-github:{ .lg .middle } __Source code__

    ---

    Training scripts, configs, and DOE lens files on GitHub.

    [:octicons-arrow-right-24: AI4Optics/DeepLens_Hyperspectral](https://github.com/AI4Optics/DeepLens_Hyperspectral)

</div>

See the [Citation](citation.md) page for how to cite this work.
