# Surrogate Networks

Neural networks that learn to predict PSFs from lens parameters, replacing
expensive ray tracing during training. These power [`PSFNetLens`](psfnetlens.md).

Fully-connected network that predicts PSF values from input parameters.

::: deeplens.surrogate.MLP

MLP with convolutional layers for spatial PSF prediction.

::: deeplens.surrogate.MLPConv

Sinusoidal-activation network (SIREN) for representing high-frequency PSF detail.

::: deeplens.surrogate.siren.Siren

SIREN variant with feature modulation for conditioning on lens parameters.

::: deeplens.surrogate.ModulateSiren
