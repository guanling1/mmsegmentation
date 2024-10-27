_base_ = [
    '../_base_/models/deeplabv3plus_r50-d8.py', '../_base_/datasets/hots_v1_640x480.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_20k.py'
]
crop_size = (640, 480)
data_preprocessor = dict(size=crop_size)
model = dict(
    pretrained='torchvision://resnet18',
    backbone=dict(depth=18),
    decode_head=dict(
        c1_in_channels=64,
        c1_channels=12,
        in_channels=512,
        channels=128,
        num_classes=46
    ),
    auxiliary_head=dict(
        in_channels=256, 
        channels=64,
        num_classes=46),
    data_preprocessor=data_preprocessor)
