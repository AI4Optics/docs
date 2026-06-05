---
description: End2endImaging is a PyTorch framework for end-to-end differentiable computational imaging — joint co-design of optics, sensor, ISP, and neural image reconstruction.
---

# End2endImaging

End2endImaging models the full imaging pipeline — optics, sensor, and image processing — as a differentiable computation graph built on PyTorch. This enables gradient-based optimization of camera systems from lens surfaces all the way through neural image reconstruction.

End2end Imaging targets two main applications:

- **High-fidelity image simulation** — physically accurate rendering of camera captures for synthetic dataset generation and physical AI.
- **End-to-end optics–algorithm co-design** — joint optimization of lens surfaces and reconstruction algorithms for computational imaging.

The imaging pipeline composes three differentiable stages — optics (DeepLens), sensor, and reconstruction network:

```
Scene Image → [ DeepLens ] → Spectral Image → [ Sensor ] → Raw Image → [ Network ] → Output Image
                │                               │                        │
                GeoLens                         RGBSensor                UNet
                HybridLens                      MonoSensor               Restormer
                DiffractiveLens                                          NAFNet
                ParaxialLens
                PSFNetLens
```

## Key Features

- **End-to-End Differentiable Pipeline** — the full camera pipeline (optics, sensor, ISP, and network) as a single differentiable graph. Gradients flow from downstream task losses (reconstruction, detection, classification) back through the network, sensor noise model, and ISP into the optical design parameters, enabling hardware–software co-optimization.
- **Differentiable Optics** — built on [DeepLens](../deeplens/index.md): `GeoLens`, `HybridLens`, `DiffractiveLens`, `PSFNetLens`, and `DefocusLens` for differentiable ray tracing and wave-optics simulation and design.
- **Sensor & ISP Simulation** — physically accurate sensor simulation with a Bayer CFA and a read/shot-noise model, plus a composable, fully differentiable ISP pipeline (black level, white balance, demosaicing, color correction, gamma, tone mapping) where every stage is a `torch.nn.Module`.
- **Neural Networks** — built-in image-reconstruction networks (`NAFNet`, `UNet`, `Restormer`) for restoring clean images from degraded captures, plus PSF surrogate networks (`MLP`, `SIREN`) for fast PSF prediction during training.

## Advanced Features

Additional capabilities, available upon request:

- **GPU Kernel Acceleration** — >10× speedup and >90% GPU memory reduction with custom GPU kernels across NVIDIA and AMD platforms.
- **Distributed Optimization** — distributed simulation and optimization for billions of rays and high-resolution (>100k) diffractive propagation.

## Getting Started

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Setup__

    ---

    Install End2endImaging and run your first camera simulation.

    [:octicons-arrow-right-24: Set up End2endImaging](setup.md)

-   :material-rocket-launch-outline:{ .lg .middle } __Quickstart__

    ---

    Simulate a camera capture and co-design a lens with a network.

    [:octicons-arrow-right-24: Get started](quickstart.md)

-   :material-sitemap-outline:{ .lg .middle } __Architecture__

    ---

    How the optics, sensor, and network stages compose into the pipeline.

    [:octicons-arrow-right-24: Understand the design](architecture.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Full class documentation for the camera, sensor, and networks.

    [:octicons-arrow-right-24: Browse the API](api/index.md)

-   :material-flask-outline:{ .lg .middle } __Examples__

    ---

    Image simulation, defocus deblur, and end-to-end lens design.

    [:octicons-arrow-right-24: See examples](examples/index.md)

</div>
