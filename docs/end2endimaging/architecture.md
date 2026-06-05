# Architecture

End2endImaging models the full camera pipeline — differentiable optics, sensor
simulation, and neural image processing — as a single computation graph in
PyTorch. Every stage is differentiable, so gradients flow from a downstream task
loss (reconstruction, classification, detection) back through the network, the
ISP, the sensor noise model, and into the optical design parameters. That is what
makes optics–algorithm co-design possible.

## The pipeline

The [`Camera`](api/camera.md) class is the heart of the framework: it composes a
lens model and a sensor into one differentiable capture, which then pairs with a
reconstruction network.

```
Scene Image → [ DeepLens ] → Spectral Image → [ Sensor ] → Raw Image → [ Network ] → Output Image
                │                               │                        │
                GeoLens                         RGBSensor                UNet
                HybridLens                      MonoSensor               Restormer
                DiffractiveLens                                          NAFNet
                ParaxialLens
                PSFNetLens
```

- **Optics (DeepLens)** turns a scene into a spectrally/aberration-aware image by
  applying the lens PSF (ray tracing or PSF-map convolution).
- **Sensor** converts that optical image into a raw capture — Bayer CFA, read/shot
  noise, and a composable ISP pipeline.
- **Network** reconstructs a clean output image from the degraded raw capture.

## Code structure

```
end2end_imaging/
├── camera.py                    # Camera = Lens + Sensor differentiable pipeline (+ Renderer)
├── utils.py                     # Image I/O, metrics, device selection, logging
│
├── deeplens/                    # Differentiable optics — the DeepLens engine
│   ├── lens.py                  #   Lens — shared interface for all lens models
│   ├── geolens.py               #   GeoLens — refractive ray tracing
│   ├── hybridlens.py            #   HybridLens — refractive + DOE (ray–wave)
│   ├── diffraclens.py           #   DiffractiveLens — pure wave optics
│   ├── defocuslens.py           #   DefocusLens — defocus / circle-of-confusion
│   ├── psfnetlens.py            #   PSFNetLens — neural PSF surrogate
│   ├── geolens_pkg/             #   GeoLens mixins (PSF, eval, optim, I/O, vis)
│   ├── geometric_surface/       #   Refractive surfaces (spheric, aspheric, ...)
│   ├── phase_surface/           #   Phase surfaces (ray optics)
│   ├── diffractive_surface/     #   Diffractive elements (wave optics)
│   ├── light/                   #   Ray and ComplexWave representations
│   ├── material/                #   Glass & plastic catalogs (Sellmeier, AGF)
│   ├── imgsim/                  #   PSF convolution & Monte Carlo rendering
│   └── surrogate/               #   PSF surrogate networks (MLP, SIREN)
│
├── sensor/                      # Sensor simulation
│   ├── sensor.py                #   Sensor — shared base class
│   ├── rgb_sensor.py            #   RGBSensor (Bayer CFA + noise + ISP)
│   ├── mono_sensor.py           #   MonoSensor
│   └── isp_modules/             #   ISP pipeline (demosaic, white balance, gamma, ...)
│
└── network/                     # Neural networks
    ├── reconstruction/          #   Image reconstruction (NAFNet, Restormer, UNet)
    ├── loss/                    #   Training losses (perceptual, PSNR, SSIM)
    ├── dataset.py               #   ImageDataset, PhotographicDataset
    └── depth_estimator.py       #   DepthAnythingV2Estimator (for depth-aware sim)
```

## Optics — `deeplens/`

The optics stage is the [DeepLens](https://github.com/vccimaging/DeepLens) engine,
vendored inside End2endImaging as `end2end_imaging.deeplens`. All lens models
extend a common `Lens` interface and compute PSFs and rendered images in a fully
differentiable way:

| Lens model | Optical method |
|---|---|
| `GeoLens` | Multi-element refractive ray tracing (Zemax / Code V / JSON I/O) |
| `HybridLens` | Refractive lens + DOE — coherent ray trace then ASM wave propagation |
| `DiffractiveLens` | Pure scalar wave optics through diffractive surfaces |
| `PSFNetLens` | Neural surrogate (MLP) wrapping a `GeoLens` for fast PSF prediction |
| `DefocusLens` | Analytic circle-of-confusion / defocus model |

The supporting subpackages — `geometric_surface`, `phase_surface`,
`diffractive_surface`, `light`, `material`, `imgsim`, and `surrogate` — mirror the
standalone DeepLens library. For the full optics reference, see the
[DeepLens documentation](../deeplens/index.md); the
[Optics (DeepLens)](api/optics.md) API page documents the lens models as exposed
through End2endImaging.

## Sensor — `sensor/`

The sensor stage turns the optical image into a physically plausible raw capture.
[`RGBSensor`](api/sensor.md) applies a Bayer color-filter array, a read- + shot-noise
model, and a full **ISP pipeline** (black-level compensation, white balance,
demosaicing, color correction, gamma, tone mapping, and more). [`MonoSensor`](api/sensor.md)
is the monochrome variant. Every ISP stage in `isp_modules/` is an individual,
differentiable `torch.nn.Module`, and the pipeline is invertible (raw ↔ sRGB).

## Network — `network/`

The network stage reconstructs a clean image from the degraded sensor capture.
[`reconstruction/`](api/network.md) provides `NAFNet`, `Restormer`, and `UNet`;
[`loss/`](api/network.md) provides differentiable image-quality objectives
(`PerceptualLoss`, `PSNRLoss`, `SSIMLoss`). `dataset.py` supplies dataset wrappers
(`ImageDataset`, `PhotographicDataset`) and `depth_estimator.py` wraps Depth
Anything V2 for depth-aware simulation (used by the
[defocus deblur](examples/defocus_deblur.md) example).

!!! note "PSF surrogate networks live in DeepLens"
    The PSF surrogate models (MLP, SIREN) are part of the optics engine under
    `deeplens/surrogate/`, not `network/` — `network/` holds the image
    *reconstruction* models. See the DeepLens
    [Surrogate Networks](../deeplens/api/network.md) reference.

## Putting it together

`Camera` composes a lens and a sensor; `Camera.render(data_dict, render_mode=...)`
produces a degraded capture and its ground truth `(data_lq, data_gt)`. A
reconstruction network then maps `data_lq → data_gt`, and because every stage is
differentiable, a single loss optimizes the network and the optics jointly. See
the [Quickstart](quickstart.md) for the minimal loop and the
[Examples](examples/index.md) for complete training scripts.

## Next steps

- [API Reference](api/index.md) — camera, sensor, and network class documentation
- [Examples](examples/index.md) — image simulation, defocus deblur, and end-to-end design
- [Setup](setup.md) — install End2endImaging and run your first simulation
