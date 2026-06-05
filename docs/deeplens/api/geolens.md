# GeoLens

Differentiable multi-element refractive lens via geometric ray tracing.
`GeoLens` is the primary lens model in DeepLens: it ray-traces through a stack of
optical [surfaces](core.md#surfaces) to compute PSFs, render images, and optimize
lens geometry end-to-end.

::: deeplens.GeoLens

## Components

`GeoLens` uses a mixin architecture — its functionality is split across the
focused classes below. You normally interact only with `GeoLens` itself; these
are documented for reference.

::: deeplens.geolens_pkg.psf_compute.GeoLensPSF

::: deeplens.geolens_pkg.eval.GeoLensEval

::: deeplens.geolens_pkg.optim.GeoLensOptim

::: deeplens.geolens_pkg.optim_ops.GeoLensSurfOps

::: deeplens.geolens_pkg.io.GeoLensIO

::: deeplens.geolens_pkg.vis.GeoLensVis

::: deeplens.geolens_pkg.vis3d.GeoLensVis3D
