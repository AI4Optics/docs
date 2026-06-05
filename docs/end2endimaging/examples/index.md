# Examples

The examples map onto End2endImaging's two main applications: generating
high-fidelity synthetic datasets, and end-to-end co-design of optics and
algorithms. Each example corresponds to a script in the repository root.

## High-Fidelity Image Simulation

Simulate physically accurate camera captures — lens aberrations, defocus, sensor
noise, and ISP — to generate **synthetic training data** for image-restoration
networks. The optics are fixed; only the network is trained.

| Example | Script | Description |
|---------|--------|-------------|
| [Computational Photography](comp_photography.md) | `7_comp_photography.py` | Train a restoration network with camera simulation |
| [Defocus Deblur](defocus_deblur.md) | `8_defocus_deblur.py` | Depth-aware defocus deblur with depth-varying PSF simulation |

## Optics–Algorithm Co-Design

Optimize the **lens together with the downstream network or task**, so the optics
and the algorithm are designed end-to-end and the lens learns to capture what the
algorithm needs.

| Example | Script | Description |
|---------|--------|-------------|
| [End-to-End Lens Design](end2end_lens_design.md) | `1_end2end_lens_design.py` | Optics-network co-design with image quality loss |
| [Task-Driven Lens Design](task_driven.md) | `4_tasklens_img_classi.py` | Design a lens optimized for image classification |
