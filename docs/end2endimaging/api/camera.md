# Camera

The `end2end_imaging.camera` module provides the end-to-end camera model that couples an optical lens with an image sensor for differentiable image simulation.

`Camera` ties a lens and a sensor into a single differentiable capture model — it renders a scene through the optics and sensor to produce a simulated raw/RGB image, and is the main entry point for image simulation and end-to-end co-design.

::: end2end_imaging.camera.Camera

## Renderer

Low-level rendering engine that applies the lens PSF to form the sensor image. Used internally by `Camera`; documented here for reference.

::: end2end_imaging.camera.Renderer
