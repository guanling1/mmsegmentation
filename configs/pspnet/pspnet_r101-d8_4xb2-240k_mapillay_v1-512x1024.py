_base_ = [
    '../_base_/models/pspnet_r50-d8.py', '../_base_/datasets/mapillary_v1.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_240k.py'
]

crop_size = (512, 1024)
data_preprocessor = dict(size=crop_size)
model = dict(
    data_preprocessor=data_preprocessor,
    pretrained='open-mmlab://resnet101_v1c',
    backbone=dict(depth=101),
    decode_head=dict(num_classes=66),
    auxiliary_head=dict(num_classes=66))
