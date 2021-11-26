# model settings
backbone_norm_cfg = dict(type='LN', eps=1e-6, requires_grad=True)
model = dict(
    type='EncoderDecoder',
    pretrained='pretrain/vit_small_p16_384.pth',
    backbone=dict(
        type='VisionTransformer',
        img_size=(512, 512),
        patch_size=16,
        in_channels=3,
        embed_dims=384,
        num_layers=12,
        num_heads=6,
        drop_path_rate=0.1,
        attn_drop_rate=0.0,
        drop_rate=0.0,
        final_norm=True,
        norm_cfg=backbone_norm_cfg,
        with_cls_token=True,
        interpolate_mode='bicubic',
    ),
    decode_head=dict(
        type='SegmenterLinearHead',
        in_channels=384,
        channels=384,
        num_convs=0,
        num_classes=19,
        dropout_ratio=0.0,
        in_index=-1,
        align_corners=False,
        loss_decode=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
    ),
    test_cfg=dict(mode='slide', crop_size=(512, 512), stride=(480, 480)),
)
