---
description: Train a NAFNet to reconstruct a 31-band hyperspectral cube from a single RGB capture taken through a fixed diffractive encoder.
---

# HSI Reconstruction

**Script:** `1_hsi_reconstruction.py`

Train the reconstruction network against a **fixed** DOE encoder. The optics are frozen, so this isolates the network's job: invert a known optical code to recover the spectral cube. It is also the right setup for *benchmarking* an encoder — reconstruction quality is then a property of the optics, not of a still-changing lens.

## Run

```bash
# Pixel2D encoder (default)
python 1_hsi_reconstruction.py --config configs/1_hsi_reconstruction_pixel2d.yml

# DiffractedRotation encoder
python 1_hsi_reconstruction.py --config configs/1_hsi_reconstruction_diffracted_rotation.yml
```

The `--config` file selects the fixed encoder via `camera.lens_file`.

## How it works

Each training step renders an RGB capture from a ground-truth spectral cube, then asks the network to undo it:

```python
self.camera = HSICamera(lens_file=..., sensor_file=...)          # fixed DOE
self.model  = NAFNet(in_chan=3, out_chan=31, width=32, ...)      # 3-channel RGB → 31-band cube

# per step:
rgb_capture, spectral_gt = self.camera.render(data_dict)         # differentiable optics + sensor
spectral_pred = self.model(rgb_capture).clamp(0, 1)
loss = F.l1_loss(spectral_pred, spectral_gt)                     # only the network updates
```

- **Data** — the [CAVE](https://www.cs.columbia.edu/CAVE/databases/multispectral/) dataset (`CaveDataset`), 31 bands over 400–700 nm; 256×256 train crops, 512×512 validation.
- **Network** — `NAFNet`, `in_chan=3`, `out_chan=31`, `width=32`.
- **Objective** — L1 loss on the spectral cube; reported metrics are PSNR and SSIM.

!!! note "The encoder sets the ceiling"
    Because the DOE is frozen, reconstruction quality is bounded by how well the
    encoder conditions the problem — a poorly-conditioned PSF cannot be undone by
    any network. To improve the optics themselves, design them jointly with the
    network in the [end-to-end](end2end_hsi.md) example.

## Next steps

- [End-to-End Design](end2end_hsi.md) — co-optimize the DOE and the network
- [Diffractive Surfaces](diffractive_surfaces.md) — the encoders you can benchmark
