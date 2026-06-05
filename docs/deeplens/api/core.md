# Optics Core

Shared building blocks used by every lens model: base classes, optical surfaces,
light/wave representations, and image-simulation utilities.

## Base Classes

Base class for all optical objects. Provides device transfer, dtype conversion,
and cloning by introspecting instance tensors.

::: deeplens.DeepObj

Optical material model (refractive index and dispersion) used by refractive
surfaces.

::: deeplens.Material

## Surfaces

### Geometric Surfaces

Base class for all geometric optical surfaces. Implements surface intersection
(Newton's method with one differentiable step) and differentiable vector Snell's
law refraction.

::: deeplens.geometric_surface.Surface

Spherical surface defined by curvature $c = 1/R$.

::: deeplens.geometric_surface.Spheric

Even-asphere surface: spherical base with polynomial corrections.

::: deeplens.geometric_surface.Aspheric

::: deeplens.geometric_surface.Aperture

### Phase Surfaces

Phase surfaces model flat diffractive optical elements (DOEs) and metasurfaces
via a wavelength-scaled phase profile. All classes inherit from `Phase` and
implement `phi()` (phase map) and `dphi_dxy()` (phase gradient) for the
generalized Snell's law deflection in `diffract()`.

> **Note**: `Phase.diffract()` treats the phase profile as wavelength-independent.
> Only the λ scaling in the generalized Snell's law and the OPL accumulation vary
> with wavelength. For a physical DOE whose phase profile changes with wavelength
> via the height–index relation `(n(λ)−1)·h`, use `DiffractiveSurface` instead.

::: deeplens.phase_surface.Phase

::: deeplens.phase_surface.Binary2Phase

::: deeplens.phase_surface.FresnelPhase

::: deeplens.phase_surface.ZernikePhase

::: deeplens.phase_surface.PolyPhase

::: deeplens.phase_surface.CubicPhase

::: deeplens.phase_surface.GratingPhase

::: deeplens.phase_surface.NURBSPhase

::: deeplens.phase_surface.VortexPhase

## Light

Geometric ray representation carrying origin, direction, wavelength, validity
mask, energy, and optical path length (OPL).

::: deeplens.Ray

Complex electromagnetic field with Angular Spectrum Method (ASM), Fresnel, and
Fraunhofer propagation via `torch.fft`.

::: deeplens.ComplexWave

## Image Simulation

### PSF Rendering

Functions for rendering images with point spread functions.

::: deeplens.imgsim.psf.conv_psf

::: deeplens.imgsim.psf.conv_psf_map

::: deeplens.imgsim.psf.conv_psf_depth_interp

::: deeplens.imgsim.psf.conv_psf_map_depth_interp

::: deeplens.imgsim.psf.conv_psf_occlusion

::: deeplens.imgsim.psf.splat_psf_per_pixel

::: deeplens.imgsim.psf.interp_psf_map

::: deeplens.imgsim.psf.rotate_psf

### Monte Carlo Integrals

Utilities for ray-bundle accumulation and ray-traced image sampling.

::: deeplens.imgsim.monte_carlo.forward_integral

::: deeplens.imgsim.monte_carlo.backward_integral

::: deeplens.imgsim.monte_carlo.assign_points_to_pixels
