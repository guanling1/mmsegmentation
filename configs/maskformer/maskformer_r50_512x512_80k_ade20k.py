_base_ = [
    '../_base_/datasets/ade20k.py', '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_80k.py'
]
norm_cfg = dict(type='SyncBN', requires_grad=True)
crop_size = (512, 512)
data_preprocessor = dict(
    type='SegDataPreProcessor',
    size=crop_size,
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    bgr_to_rgb=True,
    pad_val=0,
    seg_pad_val=255)
# model_cfg
num_classes = 150
model = dict(
    type='EncoderDecoder',
    data_preprocessor=data_preprocessor,
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        dilations=(1, 1, 1, 1),
        strides=(1, 2, 2, 2),
        norm_cfg=norm_cfg,
        norm_eval=True,
        style='pytorch',
        contract_dilation=True,
        init_cfg=dict(
            type='Pretrained', checkpoint='open-mmlab://resnet50_v1c')),
    decode_head=dict(
        type='mmseg.MaskFormerHead',
        _scope_='mmdet',
        in_channels=[256, 512, 1024, 2048],  # pass to pixel_decoder inside
        feat_channels=256,
        in_index=[0, 1, 2, 3],
        num_classes=150,
        out_channels=256,
        num_queries=100,
        pixel_decoder=dict(
            type='PixelDecoder',
            norm_cfg=dict(type='GN', num_groups=32),
            act_cfg=dict(type='ReLU')),
        enforce_decoder_input_project=False,
        positional_encoding=dict(
            type='SinePositionalEncoding', num_feats=128, normalize=True),
        transformer_decoder=dict(
            type='DetrTransformerDecoder',
            return_intermediate=True,
            num_layers=6,
            transformerlayers=dict(
                type='DetrTransformerDecoderLayer',
                attn_cfgs=dict(
                    type='MultiheadAttention',
                    embed_dims=256,
                    num_heads=8,
                    attn_drop=0.1,
                    proj_drop=0.1,
                    dropout_layer=None,
                    batch_first=False),
                ffn_cfgs=dict(
                    embed_dims=256,
                    feedforward_channels=2048,
                    num_fcs=2,
                    act_cfg=dict(type='ReLU', inplace=True),
                    ffn_drop=0.1,
                    dropout_layer=None,
                    add_identity=True),
                # the following parameter was not used,
                # just make current api happy
                feedforward_channels=2048,
                operation_order=('self_attn', 'norm', 'cross_attn', 'norm',
                                 'ffn', 'norm')),
            init_cfg=None),
        loss_cls=dict(
            type='CrossEntropyLoss',
            use_sigmoid=False,
            loss_weight=1.0,
            reduction='mean',
            class_weight=[1.0] * num_classes + [0.1]),
        loss_mask=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            reduction='mean',
            loss_weight=20.0),
        loss_dice=dict(
            type='DiceLoss',
            use_sigmoid=True,
            activate=True,
            reduction='mean',
            naive_dice=True,
            eps=1.0,
            loss_weight=1.0),
        train_cfg=dict(
            assigner=dict(
                type='HungarianAssigner',
                match_costs=[
                    dict(type='ClassificationCost', weight=1.0),
                    dict(type='FocalLossCost', weight=20.0, binary_input=True),
                    dict(type='DiceCost', weight=1.0, pred_act=True, eps=1.0)
                ]),
            sampler=dict(type='MaskPseudoSampler')),
        test_cfg=dict(
            panoptic_on=False,
            # For now, the dataset does not support
            # evaluating semantic segmentation metric.
            semantic_on=True,
            instance_on=False,
            # max_per_image is for instance segmentation.
            max_per_image=100,
            object_mask_thr=0.8,
            iou_thr=0.8,
            # In MaskFormer's panoptic postprocessing,
            # it will not filter masks whose score is smaller than 0.5 .
            filter_low_score=False)),
    # training and testing settings
    train_cfg=dict(),
    test_cfg=dict(mode='whole'),
)

# optimizer
optimizer = dict(
    type='AdamW', lr=0.0001, betas=(0.9, 0.999), weight_decay=0.0005)
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=optimizer,
    clip_grad=None,
    paramwise_cfg=dict(custom_keys={
        'backbone': dict(lr_mult=0.1),
    }))
