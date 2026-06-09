---
description: How to cite DeepLens Hyperspectral and the diffractive-optics methods it builds on.
---

# Citation

DeepLens Hyperspectral is an application example built on the [DeepLens](../deeplens/index.md) framework. If you use this code or these ideas in your research, please cite the DeepLens framework paper:

> X. Yang, M. Souza, K. Wang, P. Chakravarthula, Q. Fu, and W. Heidrich,
> "End-to-End Hybrid Refractive-Diffractive Lens Design with Differentiable Ray-Wave Model,"
> in *SIGGRAPH Asia 2024 Conference Papers*, 2024.
> [doi:10.1145/3680528.3687640](https://doi.org/10.1145/3680528.3687640)

```bibtex
@inproceedings{Yang_2024,
  title     = {End-to-End Hybrid Refractive-Diffractive Lens Design with Differentiable Ray-Wave Model},
  author    = {Yang, Xinge and Souza, Matheus and Wang, Kunyi and Chakravarthula, Praneeth and Fu, Qiang and Heidrich, Wolfgang},
  booktitle = {SIGGRAPH Asia 2024 Conference Papers},
  series    = {SA '24},
  pages     = {1--11},
  year      = {2024},
  month     = dec,
  publisher = {ACM},
  doi       = {10.1145/3680528.3687640},
  url       = {https://doi.org/10.1145/3680528.3687640}
}
```

## Methods

The diffractive encoders implemented here are based on:

- **DiffractedRotation** — D. S. Jeon, S.-H. Baek, S. Yi, Q. Fu, X. Dun, W. Heidrich, and M. H. Kim,
  "Compact Snapshot Hyperspectral Imaging with Diffracted Rotation,"
  *ACM Transactions on Graphics (SIGGRAPH)*, 2019.
- **RotationallySymmetric** — X. Dun, H. Ikoma, G. Wetzstein, Z. Wang, X. Cheng, and Y. Peng,
  "Learned rotationally symmetric diffractive achromat for full-spectrum computational imaging,"
  *Optica*, 2020.

For an analysis of how the optical encoder limits data-driven spectral reconstruction, see
*"Limitations of Data-Driven Spectral Reconstruction: An Optics-Aware Analysis"*
([code](https://github.com/vccimaging/OpticsAwareHSI-Analysis)).

## Acknowledgement

The freeform DOE height map (`planar_doe.npy`) was provided by [Jingyue Ma](https://github.com/Jingyue-MA).

## License

DeepLens Hyperspectral is released under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
