# Copyright (c) OpenMMLab. All rights reserved.
_base_ = './pspnet_r50-d8_512x512_40k_voc12aug.py'
model = dict(pretrained='open-mmlab://resnet101_v1c', backbone=dict(depth=101))
