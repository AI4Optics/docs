---
description: DeepLens Hyperspectral Imaging examples — build an HSI camera, visualize the three diffractive encoders, train a reconstructor against a fixed DOE, and run end-to-end design.
---

# Examples

These examples walk from a first hyperspectral camera to full end-to-end design. Each corresponds to a script in the [repository root](https://github.com/AI4Optics/DeepLens_Hyperspectral).

## Build & visualize

Set up the differentiable HSI camera and inspect how each DOE encodes the spectrum into its PSF.

| Example | Script | Description |
|---|---|---|
| [Diffractive Surfaces](diffractive_surfaces.md) | `0_hello_deeplens_hsi.py` | The three DOE encoders — phase maps and wavelength-dependent PSFs |

## Train & design

Train the reconstruction network — against a fixed encoder, or jointly with the optics.

| Example | Script | Description |
|---|---|---|
| [HSI Reconstruction](hsi_reconstruction.md) | `1_hsi_reconstruction.py` | Train `NAFNet` to recover the spectral cube from a **fixed**-DOE capture |
| [End-to-End Design](end2end_hsi.md) | `2_end2end_hsi.py` | **Jointly** optimize the DOE and the reconstruction network |
