# Network

The `end2end_imaging.network` module provides image reconstruction networks and loss functions for end-to-end training.

!!! note "Looking for PSF surrogate networks?"
    The PSF surrogate models (MLP, SIREN, etc.) are part of DeepLens — see
    [Surrogate Networks](../../deeplens/api/network.md) in the DeepLens API reference.

## Reconstruction Networks

Image restoration networks that recover a clean image from a degraded (aberrated) sensor capture.

::: end2end_imaging.network.NAFNet

::: end2end_imaging.network.UNet

::: end2end_imaging.network.Restormer

## Loss Functions

Differentiable image-quality losses for training reconstruction networks.

::: end2end_imaging.network.PerceptualLoss

::: end2end_imaging.network.PSNRLoss

::: end2end_imaging.network.SSIMLoss
