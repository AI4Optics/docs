# Quickstart

This guide walks through the two core End2endImaging workflows: **simulating a
camera capture** from an input image, and **end-to-end co-design** of a lens and a
reconstruction network. If you haven't installed End2endImaging yet, start with
[Setup](setup.md).

## Simulate an Image

First, create a `Camera` — which couples a lens and a sensor into a single differentiable capture model:

```python
from end2end_imaging import Camera

camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)
```

Then render a physically accurate capture from an input image, including lens aberrations, sensor noise, and ISP processing:

```python
# Prepare input data
data_dict = {
    "img": img_srgb,             # sRGB image, shape (B, 3, H, W), range [0, 1]
    "iso": iso,                  # ISO value, shape (B,)
    "field_center": field_center, # field position, shape (B, 2), range [-1, 1]
}

# Simulate camera capture (lens aberration + sensor noise)
data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch")
```

## End-to-End Camera Design

Jointly optimize a lens and a neural image processing network. The `Camera` generates training data by simulating realistic image degradation, and the network learns to restore the image:

```python
import torch
from end2end_imaging import Camera
from end2end_imaging.network import NAFNet

# Initialize camera and restoration network
camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)
network = NAFNet(in_chan=3, out_chan=3)
optimizer = torch.optim.Adam(network.parameters(), lr=1e-4)

for step in range(num_steps):
    optimizer.zero_grad()

    # Simulate camera capture
    data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch")

    # Restore the degraded image
    restored = network(data_lq)
    loss = torch.nn.functional.l1_loss(restored, data_gt)

    loss.backward()
    optimizer.step()
```

See `7_comp_photography.py` for a full training example, walked through on the
[Computational Photography](examples/comp_photography.md) page.

## Next steps

- [Architecture](architecture.md) — how the optics, sensor, and network stages compose
- [API Reference](api/index.md) — camera, sensor, and network class documentation
- [Examples](examples/index.md) — image simulation, defocus deblur, and end-to-end design
