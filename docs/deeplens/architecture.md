# Architecture

DeepLens is a differentiable optics library built on PyTorch. Every optical
object — lens, surface, ray, wave, material — is differentiable, so gradients
flow from the output (a PSF or rendered image) back to any lens parameter. This
is what makes gradient-based lens design and end-to-end optimization possible.

The code is layered: a small foundation (`DeepObj`, config) underpins the
**optical primitives** (surfaces, rays, waves, materials), which are assembled
into **lens models**, which are in turn driven by **PSF computation, image
simulation, evaluation, and optimization**.

## Package layout

```
deeplens/
├── base.py                 DeepObj — device/dtype/clone for every optical object
├── config.py               Default wavelengths, depths, kernel sizes, sample counts
├── lens.py                 Lens — shared interface for all lens models
│
├── geolens.py              GeoLens — geometric ray-tracing lens (primary model)
├── hybridlens.py           HybridLens — refractive lens + DOE (ray-then-wave)
├── diffraclens.py          DiffractiveLens — pure wave-optics lens
├── defocuslens.py          DefocusLens — thin-lens / circle-of-confusion model
├── psfnetlens.py           PSFNetLens — neural PSF surrogate
│
├── geolens_pkg/            GeoLens mixins: PSF, eval, optim, surf-ops, vis, io
├── geometric_surface/      Curved refractive/reflective surfaces (ray optics)
├── phase_surface/          Flat phase plates (generalized Snell's law, ray optics)
├── diffractive_surface/    DOEs that modulate a complex field (wave optics)
├── light/                  Ray and ComplexWave (+ diffraction propagators)
├── imgsim/                 PSF convolution and Monte-Carlo image rendering
├── material/               Material dispersion models and glass catalogs
├── surrogate/              Neural networks for PSF prediction
│
├── loss.py                 PSF design losses
├── ops.py                  Differentiable tensor ops (interpolation, quantization)
└── utils.py                Experiment helpers and image-quality metrics
```

## Foundation

Everything inherits from **`DeepObj`** (`base.py`). It gives each object device
management (`to(device)`), dtype conversion (`astype()`), and deep copy
(`clone()`) by introspecting over instance tensors and nested `DeepObj` objects —
so moving a whole lens to the GPU or to `float64` is a single call.

**`config.py`** is the single source of default constants: design wavelengths
(`DEFAULT_WAVE = 0.587 µm`, `WAVE_RGB`), object depth (`DEPTH = −20000 mm`,
practical infinity), PSF kernel size (`PSF_KS = 64`), and samples-per-pixel for
the various PSF/render paths (`SPP_PSF`, `SPP_RENDER`, …).

## Lens models

All lens models extend **`Lens`** (`lens.py`), which defines the shared
interface: design wavelengths and object depth, sensor configuration
(`set_sensor`, `set_sensor_res`), PSF computation (`psf`, `psf_rgb`, `psf_map`),
and image rendering (`render`, `render_rgbd`). `psf()` is abstract — each model
implements its own optical physics.

| Model | Optical method | Built from | File I/O |
|-------|----------------|------------|----------|
| **`GeoLens`** | Differentiable geometric ray tracing (with optional coherent exit-pupil/ASM and Huygens PSF models) | list of geometric surfaces + materials | JSON, Zemax `.zmx`, Code V `.seq` |
| **`HybridLens`** | Coherent ray trace to the DOE plane → phase modulation → ASM propagation to the sensor | a `GeoLens` + one diffractive surface (DOE) | JSON |
| **`DiffractiveLens`** | Paraxial scalar wave optics: per-surface phase + ASM propagation | a stack of diffractive / phase surfaces | JSON |
| **`DefocusLens`** | Analytic thin-lens / circle-of-confusion blur (achromatic; supports dual-pixel) | focal length, F-number, sensor | none (constructed from scalars) |
| **`PSFNetLens`** | Neural network predicts PSFs from `(field, depth, focus)` | a `GeoLens` + an MLP / conv network | `.pth` checkpoint |

`GeoLens` is the primary model and the only one with `.zmx` / `.seq` support.
`HybridLens` and `PSFNetLens` *contain* a `GeoLens` (composition, not
inheritance) — the inner lens supplies the geometric optics.

!!! note "Rendering methods are model-specific"
    The base `Lens.render()` does PSF **convolution** (`method="psf_patch"`, the
    default, or `"psf_map"` for spatially-varying blur). **`GeoLens` overrides
    `render()`** to default to `method="ray_tracing"` and add a direct
    ray-tracing path, so `"ray_tracing"` rendering is available on `GeoLens`
    only. `render_rgbd()` (depth-aware rendering) is further specialized by
    `DefocusLens` (occlusion-aware compositing) and `PSFNetLens` (per-pixel PSF
    splatting).

### GeoLens: a mixin architecture

`GeoLens` is large, so its functionality is split across the **`geolens_pkg`**
subpackage as focused mixin classes that `GeoLens` inherits — each owns one
concern:

| Mixin (module) | Responsibility |
|----------------|----------------|
| `GeoLensPSF` (`psf_compute.py`) | PSF computation: geometric ray-binning, coherent exit-pupil + ASM, Huygens–Fresnel |
| `GeoLensEval` (`eval.py`) | Classical optical analysis: spot diagram, MTF, distortion, vignetting |
| `GeoLensOptim` (`optim.py`) | Gradient-based design: regularization/RMS losses, optimizer, curriculum `optimize()` loop |
| `GeoLensSurfOps` (`optim_ops.py`) | Surface geometry ops: aspheric conversion, aperture pruning, shape correction |
| `GeoLensVis` (`vis.py`) | 2D layout and ray-path plots |
| `GeoLensVis3D` (`vis3d.py`) | 3D mesh visualization and `.obj` export |
| `GeoLensIO` (`io.py`) | Read/write JSON, Zemax `.zmx`, Code V `.seq` |

The subpackage also exports **`create_lens()`** (`optim_init.py`), a factory that
builds a starting-point `GeoLens` from optical specs (FoV, F-number, focal length
/ image height) for automated design.

## Optical surfaces

DeepLens has **three surface families**, each in its own subpackage with its own
base class. They differ in whether they bend *rays* or modulate a *wave field*:

| Family (package) | Base class | Light model | A subclass implements | Used by |
|------------------|-----------|-------------|------------------------|---------|
| `geometric_surface` | `Surface` | rays | sag `z = f(x,y)` + derivatives | `GeoLens` |
| `phase_surface` | `Phase` | rays | phase `φ(x,y)` + gradient `∂φ/∂xy` | phase elements |
| `diffractive_surface` | `DiffractiveSurface` | wave field | a phase/height profile | `HybridLens`, `DiffractiveLens` |

**Geometric surfaces** (`geometric_surface/`) are curved refractive/reflective
elements. The core operation is ray–surface intersection by **Newton's method**:
a non-differentiable loop iterates to the intersection point under
`torch.no_grad()`, followed by **one differentiable Newton step** so gradients
flow to surface parameters. Refraction is a differentiable vector **Snell's
law**; reflection is the mirror operator.
Subclasses: `Spheric`, `Aspheric`, `Aperture`, `Plane`, `Cubic`, `Mirror`,
`Prism`, `QTypeFreeform`, `Spiral`, `ThinLens`.

**Phase surfaces** (`phase_surface/`) are *flat* plates carrying a phase pattern,
traced with **rays**: intersection is a trivial plane crossing, and rays are
deflected by the **generalized Snell's law** using the phase gradient
`∂φ/∂xy` (the phase is also added to the optical path length).
Subclasses: `Binary2Phase`, `FresnelPhase`, `ZernikePhase`, `GratingPhase`,
`PolyPhase`, `CubicPhase`, `NURBSPhase`, `VortexPhase`.

**Diffractive surfaces** (`diffractive_surface/`) are DOEs modeled with **wave
optics**: they multiply an incoming `ComplexWave` by `exp(i·φ)`, where the phase
map is derived from a physical height profile and is therefore
**wavelength-dependent** (it rescales with the material's dispersion), with
fabrication concerns like quantization and undersampling handled explicitly.
Subclasses: `Binary2`, `Fresnel`, `Zernike`, `Grating`, `Pixel2D`, `Rank1`,
`RotationallySymmetric`, `DiffractedRotation`, `ThinLens`.

!!! note "`phase_surface` vs. `diffractive_surface`"
    These model the *same* kind of optical element with two different engines.
    A **phase surface** is the fast ray-optics approximation — its phase profile
    is treated as wavelength-independent (only the λ factor in the Snell term
    varies). A **diffractive surface** is the full wave-optics model — its phase
    comes from a height map and changes with wavelength via `(n(λ)−1)·h`. Use
    `phase_surface` inside ray-traced lenses and `diffractive_surface` when
    diffraction and dispersion matter.

## Light: rays and waves

The **`light/`** subpackage defines the two light representations that flow
through the surfaces above.

**`Ray`** is a batched ray bundle carrying origins `o`, unit directions `d`,
wavelength, a validity mask, energy, and (in coherent mode) accumulated optical
path length. It can propagate to a plane, compute its centroid and RMS spot
size, and is fully differentiable.

**`ComplexWave`** is a monochromatic complex scalar field on a uniform grid
(amplitude `u`, wavelength, pixel pitch, position `z`). It can be created as a
point, plane, or image wave, and propagated between planes by several scalar
diffraction methods — `prop()` auto-selects one by distance:

| Propagator | Regime |
|------------|--------|
| `AngularSpectrumMethod` (ASM) | near field, rigorous up to the Nyquist sampling limit |
| `BandLimitedASM` | near + intermediate field (default for short/medium distances) |
| `FresnelDiffraction` | far field, single FFT |
| `FraunhoferDiffraction` | far field |
| `RayleighSommerfeld(Integral)` | brute-force reference — accurate but slow |

Helpers such as `Nyquist_ASM_zmax` and `Fresnel_zmin` express the sampling
limits that decide which propagator is valid.

## Image simulation

The **`imgsim/`** subpackage turns PSFs and rays into rendered images.

- **`psf.py`** — PSF convolution: `conv_psf` (one global kernel),
  `conv_psf_map` (spatially-varying via grid patches),
  `splat_psf_per_pixel` (full per-pixel variation), the depth-interpolated
  variants `conv_psf_depth_interp` / `conv_psf_map_depth_interp`,
  `conv_psf_occlusion` (occlusion-aware bokeh), plus `interp_psf_map` and
  `rotate_psf` helpers.
- **`monte_carlo.py`** — Monte-Carlo integration for ray-traced rendering:
  `forward_integral` (bin ray hits into a PSF/spot image),
  `backward_integral` (sample the object image along traced rays), and
  `assign_points_to_pixels` (scatter sampled points onto a grid).

## Materials

**`material/`** provides the **`Material`** model: a wavelength-dependent
refractive index supporting Sellmeier, Schott, and Cauchy dispersion formulas,
interpolation tables, and an "optimizable" mode (learnable `n`, `V`) for
differentiable material selection. **`MATERIAL_data`** is the merged glass
catalog loaded from the bundled `.AGF` files (Schott, CDGM, plastics, misc).

## Surrogate networks

**`surrogate/`** holds neural networks that predict PSFs in place of ray
tracing. `PSFNetLens` uses **`MLP`** (predicts a flattened PSF vector) or
**`PSFNet_MLPConv`** (a conditioner + convolutional decoder producing a
spatially-varying PSF). `MLPConv`, `Siren`, and `ModulateSiren` are also
provided as building blocks.

## Support modules

- **`loss.py`** — PSF design objectives: `PSFLoss` (spot concentration +
  achromatic alignment) and `PSFStrehlLoss` (Strehl-like peak intensity).
- **`ops.py`** — differentiable tensor ops whose gradients must flow through the
  simulation: interpolation/sampling (`interp1d`, `grid_sample_xy`) and
  straight-through quantization (`diff_quantize`).
- **`utils.py`** — experiment helpers: image I/O, quality metrics
  (PSNR / SSIM / LPIPS), seeding, and logging.
