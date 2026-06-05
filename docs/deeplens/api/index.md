# API Reference

DeepLens exposes a small, composable API. Every optical system is a **lens
model** that shares the common [`Lens`](lens.md) interface — `psf()`,
`render()`, optimization, and file I/O — and is built on optical
[surfaces](core.md#surfaces), [light/wave](core.md#light) representations, and
[image-simulation](core.md#image-simulation) utilities.

Pick the lens model that matches your optical system:

<div class="grid cards" markdown>

-   :material-camera-iris:{ .lg .middle } __GeoLens__

    ---

    Multi-element refractive lens via differentiable geometric ray tracing. The primary model.

    [:octicons-arrow-right-24: GeoLens](geolens.md)

-   :material-layers-triple-outline:{ .lg .middle } __HybridLens__

    ---

    Refractive lens plus a diffractive element — hybrid ray-then-wave propagation to the sensor.

    [:octicons-arrow-right-24: HybridLens](hybridlens.md)

-   :material-sine-wave:{ .lg .middle } __DiffractiveLens__

    ---

    Pure wave-optics lens built from diffractive surfaces and scalar diffraction.

    [:octicons-arrow-right-24: DiffractiveLens](diffraclens.md)

-   :material-brain:{ .lg .middle } __PSFNetLens__

    ---

    Neural surrogate wrapping a `GeoLens` with an MLP for fast, differentiable PSFs.

    [:octicons-arrow-right-24: PSFNetLens](psfnetlens.md)

-   :material-blur:{ .lg .middle } __DefocusLens__

    ---

    Thin-lens / circle-of-confusion model for fast depth-of-field and bokeh.

    [:octicons-arrow-right-24: DefocusLens](defocuslens.md)

</div>

Shared building blocks live in [Optics Core](core.md); neural PSF predictors live
in [Surrogate Networks](network.md).
