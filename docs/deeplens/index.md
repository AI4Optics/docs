# DeepLens

DeepLens is a PyTorch-based differentiable optical lens simulator for end-to-end computational imaging, supporting multiple optical models — geometric ray tracing, diffractive wave propagation, hybrid ray-wave, and surrogate PSF networks. It can be used for end-to-end optics-algorithm co-design, gradient-based automated optical design, and synthetic dataset generation via image simulation, letting researchers rapidly prototype and optimize custom optical systems.

DeepLens computes the point spread function (PSF) of an optical lens in a fully differentiable manner:

```
Point source → [ DeepLens ] → PSF
```

DeepLens also serves as the differentiable optics engine in an end-to-end computational imaging pipeline such as [End2endImaging](https://github.com/vccimaging/End2endImaging), where the optics, sensor, and a reconstruction network form a single differentiable graph that can be optimized jointly:

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

- **Differentiable Optics** — differentiable optical simulation for accurate, efficient gradient computation, enabling lens inverse design.
- **Automated Design** — fully automated optical design via gradient-based and advanced optimization, shortening the development cycle for a wide range of systems (highly aspherical lenses, metasurfaces, AR/VR displays).
- **Multiple Optical Models** — geometric ray tracing (`GeoLens`), hybrid ray-wave (`HybridLens`), pure diffractive (`DiffractiveLens`), neural surrogate (`PSFNetLens`), and defocus (`DefocusLens`) models.
- **Image Simulation** — photorealistic rendering with spatially-varying, depth-dependent aberrations, closing the sim-to-real gap when combined with [End2endImaging](https://github.com/vccimaging/End2endImaging).

## Advanced Features

Additional capabilities, customizable upon request:

- **GPU Kernel Acceleration** — custom GPU kernels deliver >10× speedup and >90% memory reduction across NVIDIA and AMD platforms, making deployment on local laptops practical.
- **Polarization Ray Tracing** — polarization ray tracing and inverse design of thin films via [DiffTMM](https://github.com/AI4Optics/DiffTMM).
- **Non-Sequential Ray Tracing** — differentiable non-sequential ray tracing for stray-light analysis and optimization.
- **Distributed Optimization** — distributed simulation and optimization for billion-scale ray tracing and high-resolution (>100k × 100k) diffractive propagation.

## Getting Started

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Setup__

    ---

    Create the environment and run your first lens demo.

    [:octicons-arrow-right-24: Set up DeepLens](setup.md)

-   :material-rocket-launch-outline:{ .lg .middle } __Quickstart__

    ---

    Load a lens, compute a PSF, and render an image in minutes.

    [:octicons-arrow-right-24: Get started](quickstart.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Full class and function documentation for the optics engine.

    [:octicons-arrow-right-24: Browse the API](api/index.md)

-   :material-flask-outline:{ .lg .middle } __Examples__

    ---

    Lens design, end-to-end optimization, and image simulation.

    [:octicons-arrow-right-24: See examples](examples/index.md)

</div>
