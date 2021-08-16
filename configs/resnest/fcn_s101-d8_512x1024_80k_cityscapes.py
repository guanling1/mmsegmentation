# Copyright (c) OpenMMLab. All rights reserved.
_base_ = '../fcn/fcn_r101-d8_512x1024_80k_cityscapes.py'
model = dict(
    pretrained='open-mmlab://resnest101',
    backbone=dict(
        type='ResNeSt',
        stem_channels=128,
        radix=2,
        reduction_factor=4,
        avg_down_stride=True))
