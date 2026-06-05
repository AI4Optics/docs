# HybridLens

Combines a [`GeoLens`](geolens.md) with a diffractive optical element (DOE).
`HybridLens` performs coherent ray tracing to the DOE plane, then Angular
Spectrum Method (ASM) propagation to the sensor — a hybrid ray–wave model for
refractive lenses with DOE or metasurface phase elements.

::: deeplens.HybridLens

## DOE Models

The diffractive element is configured by the `DOE` block in the lens JSON; its
`type` field selects one of the phase parameterizations below. All subclass
`DiffractiveSurface`, which defines the shared phase / propagation interface.

::: deeplens.diffractive_surface.DiffractiveSurface

Polynomial (Binary-2) rotationally-symmetric phase profile.

::: deeplens.diffractive_surface.Binary2

Free-form, per-pixel phase map.

::: deeplens.diffractive_surface.Pixel2D

Fresnel-lens (quadratic) phase profile.

::: deeplens.diffractive_surface.Fresnel

Phase parameterized by Zernike polynomials.

::: deeplens.diffractive_surface.Zernike

Linear / blazed grating phase.

::: deeplens.diffractive_surface.Grating
