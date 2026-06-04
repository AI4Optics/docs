# Hello HybridLens

**Script:** [`0_hello_hybridlens.py`](https://github.com/vccimaging/DeepLens/blob/main/0_hello_hybridlens.py)

A hybrid refractive–diffractive lens: coherent ray tracing computes the complex
wavefront at the DOE plane (capturing all geometric aberrations), the DOE phase
modulates it, and ASM propagation carries it to the sensor. Runs in `float64`.

## What it demonstrates

- Loading a `HybridLens` from a JSON file that contains both refractive surfaces
  and a `DOE` block.
- The coherent ray-trace → DOE modulation → ASM propagation pipeline.
- Rendering an image through the hybrid system.

## Run

```bash
python 0_hello_hybridlens.py
```

## Key code

```python
import torch
torch.set_default_dtype(torch.float64)  # required for accurate phase tracing
from deeplens import HybridLens
from deeplens.config import WAVE_RGB
from deeplens.imgsim import conv_psf

lens = HybridLens(filename="./datasets/lenses/hybridlens/a489_doe.json")
lens.refocus(foc_dist=-1000.0)
lens.draw_layout(save_name="./hello_hybridlens_layout.png")

# Coherent ray tracing + DOE modulation + ASM propagation (>= 1e6 samples)
psf = lens.psf(points=[0.0, 0.0, -10000.0], ks=64, spp=1_000_000)

# Image simulation: stack one PSF per RGB wavelength, then convolve a chart
psf_rgb = torch.stack(
    [lens.psf(points=[0.0, 0.0, -10000.0], ks=128, wvln=w, spp=1_000_000) for w in WAVE_RGB],
    dim=0,
).float()
img_render = conv_psf(img, psf_rgb)

print(f"Focal length: {lens.geolens.foclen:.2f} mm")  # refractive part via .geolens
```

## Results

| Lens layout | Rendered image |
|---|---|
| ![Layout](../assets/hello_hybridlens/layout.png) | ![Render](../assets/hello_hybridlens/render.png) |

## See also

- API: [`HybridLens`](../api/hybridlens.md)
- [HybridLens design](design_hybridlens.md) · [Multi-order diffraction](multi_order.md)
