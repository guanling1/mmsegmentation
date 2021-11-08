_base_ = './bisenetv1_r50-d32_lr5e3_4x4_512x512_160k_coco-stuff164k.py'

model = dict(
    backbone=dict(
        backbone_cfg=dict(
            init_cfg=dict(
                type='Pretrained', checkpoint='open-mmlab://resnet50_v1c'))))
