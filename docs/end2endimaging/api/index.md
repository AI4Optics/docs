# API Reference

End2endImaging composes a differentiable camera from three building blocks: an
optical **lens** (provided by [DeepLens](../../deeplens/index.md)), an image
**[sensor](sensor.md)**, and — for end-to-end design — a reconstruction
**[network](network.md)**. The **[`Camera`](camera.md)** couples the lens and
sensor into a single differentiable image-capture model.

<div class="grid cards" markdown>

-   :material-camera-iris:{ .lg .middle } __Optics (DeepLens)__

    ---

    Differentiable lens models, optical surfaces, and PSF simulation — provided
    by the DeepLens optics engine.

    [:octicons-arrow-right-24: Optics (DeepLens)](optics.md)

-   :material-image-filter-center-focus:{ .lg .middle } __Sensor__

    ---

    Differentiable RGB/mono sensors with read/shot noise and a full ISP pipeline
    (demosaic, white balance, color correction, gamma).

    [:octicons-arrow-right-24: Sensor](sensor.md)

-   :material-brain:{ .lg .middle } __Network__

    ---

    Image-reconstruction networks (`UNet`, `Restormer`, `NAFNet`) and training
    losses (PSNR, SSIM, perceptual).

    [:octicons-arrow-right-24: Network](network.md)

-   :material-camera:{ .lg .middle } __Camera__

    ---

    The end-to-end model that ties a lens and sensor into one differentiable
    capture for image simulation and co-design.

    [:octicons-arrow-right-24: Camera](camera.md)

</div>

The optical lens models (`GeoLens`, `HybridLens`, `DiffractiveLens`, …) are
documented in the [DeepLens API reference](../../deeplens/api/index.md).
