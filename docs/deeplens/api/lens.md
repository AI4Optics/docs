# Lens

Abstract base class for every lens model in DeepLens. `Lens` defines the shared
interface — `psf()`, `psf_rgb()`, `render()`, sensor configuration, and file
I/O — that [`GeoLens`](geolens.md), [`HybridLens`](hybridlens.md),
[`DiffractiveLens`](diffraclens.md), [`PSFNetLens`](psfnetlens.md), and
[`DefocusLens`](defocuslens.md) all inherit.

::: deeplens.Lens
