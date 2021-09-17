_base_ = [
    '../_base_/models/icnet_r50-d8.py',
    '../_base_/datasets/cityscapes_832x832.py', '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_80k.py'
]

model = dict(
    backbone=dict(layer_channels=(128, 512), backbone_cfg=dict(depth=18)))
