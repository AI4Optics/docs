# Defocus Deblur

End-to-end defocus deblur and aberration correction with depth-conditioned image
simulation. A monocular depth estimator drives depth- and spatially-varying PSF
simulation — capturing both defocus blur and the lens's field-dependent
aberrations — and a restoration network learns to recover the sharp image.

**Script:** `8_defocus_deblur.py`

**Reference:** Xinge Yang, Chuong Nguyen, Wenbin Wang, Kaizhang Kang, Wolfgang Heidrich, Xiaoxing Li, "Efficient Depth- and Spatially-Varying Image Simulation for Defocus Deblur," *ICCV Workshop* 2025.

## Overview

Each training batch is degraded on the fly. Depth is estimated from the RGB image
with [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) and
used to render a depth-varying point spread function
(`render_mode="psf_patch_depth_interp"`), so the simulated capture has realistic,
depth-dependent defocus on top of the lens's spatially-varying aberrations. A
`NAFNet` restoration network is then trained to invert this degradation.

```python
import torch
from end2end_imaging import Camera
from end2end_imaging.network import DepthAnythingV2Estimator, NAFNet

# Camera (lens + sensor), refocused to the scene
camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)
camera.lens.refocus(foc_dist=-10000.0)        # focus distance in mm (object space)

# Frozen monocular depth estimator (Depth Anything V2)
depth_estimator = DepthAnythingV2Estimator(
    model_name="depth-anything/Depth-Anything-V2-Small-hf",
    depth_min_mm=3000.0,
    depth_max_mm=10000.0,
)

# Restoration network; channel layout follows the camera output type
in_chan, out_chan = Camera.output_channels("rggbif")   # -> (6, 4)
network = NAFNet(in_chan=in_chan, out_chan=out_chan)
optimizer = torch.optim.AdamW(network.parameters(), lr=1e-4)

for data_dict in train_loader:
    # 1. Estimate per-pixel depth (mm) from the RGB batch
    data_dict["depth"] = depth_estimator.estimate(data_dict["img"])

    # 2. Depth- and spatially-varying PSF simulation (defocus + lens aberrations)
    inputs, targets = camera.render(
        data_dict, render_mode="psf_patch_depth_interp", output_type="rggbif",
    )

    # 3. Restore the degraded capture
    outputs = network(inputs)
    loss = torch.nn.functional.l1_loss(outputs, targets)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

## Usage

```bash
python 8_defocus_deblur.py --config configs/8_defocus_deblur.yml
```
