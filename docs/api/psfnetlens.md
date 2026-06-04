# PSFNetLens

Neural surrogate that wraps a [`GeoLens`](geolens.md) with an MLP to predict
PSFs. It provides fast, differentiable PSF evaluation during end-to-end training,
trading a one-time fitting cost for cheap inference. See also
[Surrogate Networks](network.md).

::: deeplens.PSFNetLens
