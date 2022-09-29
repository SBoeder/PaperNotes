



# [Plenoxels: Radiance Fields without Neural Networks](https://arxiv.org/abs/2112.05131) ([local](../local/plenoxel.pdf))


Published: 2021-12

Tags: [NeRF](../tags/nerf.md)

tl;dr: System for photorealistic view synthesis via gradient methods. Orders of magnitude faster optimization and rendering compared to NeRF.

## Summary
Given a set of images of an object or scene, a sparse voxel grid is constructed, where each voxel contains density and spherical harmonics coefficients. For each sample point along a ray, these coefficients are computed via trilinear interpolation of neighboring voxels and differentiable volumetric rendering as in NeRF. Afterwards, the voxel coefficients can be optimized via MSE reconstruction loss of all images (plus a regularizer).

## Technical Details
<img src="../images/plenoxel1.PNG" alt="plenoxel system" width="750"/>

## Notes

## Questions

## Related
