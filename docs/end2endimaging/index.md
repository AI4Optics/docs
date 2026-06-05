# End2endImaging

End2endImaging models the full imaging pipeline — optics, sensor, and image processing — as a differentiable computation graph built on PyTorch. This enables gradient-based optimization of camera systems from lens surfaces all the way through neural image reconstruction.

End2end Imaging targets two main applications:

- **High-fidelity image simulation** — physically accurate rendering of camera captures for synthetic dataset generation and physical AI.
- **End-to-end optics–algorithm co-design** — joint optimization of lens surfaces and reconstruction algorithms for computational imaging.

## Architecture

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

See [Architecture](architecture.md) for the full module breakdown.

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
