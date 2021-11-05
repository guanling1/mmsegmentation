_base_ = [
    '../_base_/models/upernet_r50.py', '../_base_/datasets/ade20k.py',
    '../_base_/default_runtime.py', 'twins_schedule_160k.py'
]
model = dict(
    type='EncoderDecoder',
    pretrained='pretrained/alt_gvt_base.pth',
    backbone=dict(
        type='Twins_alt_gvt',
        patch_size=4,
        embed_dims=[96, 192, 384, 768],
        num_heads=[3, 6, 12, 24],
        mlp_ratios=[4, 4, 4, 4],
        qkv_bias=True,
        norm_cfg=dict(type='LN'),
        depths=[2, 2, 18, 2],
        wss=[7, 7, 7, 7],
        sr_ratios=[8, 4, 2, 1],
        extra_norm=True,
        drop_path_rate=0.2,
        style='pytorch'),
    decode_head=dict(num_classes=150, in_channels=[96, 192, 384, 768]),
    auxiliary_head=dict(num_classes=150, in_channels=384))

optimizer = dict(
    _delete_=True,
    type='AdamW',
    lr=0.00006,
    betas=(0.9, 0.999),
    weight_decay=0.01,
    paramwise_cfg=dict(custom_keys={
        'pos_block': dict(decay_mult=0.),
        'norm': dict(decay_mult=0.)
    }))

lr_config = dict(
    _delete_=True,
    policy='poly',
    warmup='linear',
    warmup_iters=1500,
    warmup_ratio=1e-6,
    power=1.0,
    min_lr=0.0,
    by_epoch=False)

# By default, models are trained on 8 GPUs with 2 images per GPU
data = dict(samples_per_gpu=2)
