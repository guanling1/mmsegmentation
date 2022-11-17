_base_ = ['./dest_simpatt-b0_1024x1024_160k_cityscapes.py']


embed_dims = [64, 128, 250, 320]

model = dict(
    type='EncoderDecoder',
    pretrained=None,
    backbone=dict(
        embed_dims=embed_dims),
    decode_head=dict(
        in_channels=embed_dims))




