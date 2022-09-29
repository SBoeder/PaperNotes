



# [Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D](https://arxiv.org/abs/2008.05711)


Published: 2020-08

Tags: [BEV](../tags/bev.md)

tl;dr: End-to-end differential method for BEV rendering from multi-camera images.
## Summary
End-to-end differential method to train a BEV model from multi-camera images. Trains a model for BEV generation and a downstream task for BEV inference. First, "lift" images into a point cloud via a categorical depth distribution prediction. Then "splat" the point clouds into the BEV frame using camera extrinsincs and the point pillars architecture. Finally, the "shoot" part corresponds to shooting out trajectories for the downstream task. The ground truth of this task is used for supervision of the whole architecture.

## Technical Details
- Using a cumulative sum trick to enable fast differentiable pooling of the pillars
- Symmetric properties of classical multi-view methods are preserved, but in contrast to these the proposed method is fully differentiable. 

## Notes
- Supervision of the "lift" and "splat" components come from the ground truth task (hence, they cannot be learned without the "shoot" part).
- However, training does not require ground truth depth.

## Questions

## Related
[1] [Pseudo-LiDAR from Visual Depth Estimation: Bridging the Gap in 3D Object Detection for Autonomous Driving](https://arxiv.org/abs/1812.07179) [notes](notes/pseudolidar.md)