# model settings
norm_cfg = dict(type='SyncBN', eps=1e-03, requires_grad=True)
model = dict(
    type='EncoderDecoder',
    backbone=dict(
        type='CGNet',
        norm_cfg=norm_cfg,
        in_channels=3,
        num_channels=[32, 64, 128],
        num_blocks=[3, 21],
        dilation=[2, 4],
        reduction=[8, 16]),
    decode_head=dict(
        type='CGHead',
        in_channels=256,
        channels=256,
        norm_cfg=norm_cfg,
        num_classes=19,
        in_index=-1,
        dropout_ratio=0,
        loss_decode=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0, \
            class_weight=[2.5959933, 6.7415504, 3.5354059, 9.8663225, 9.690899,
                          9.369352, 10.289121, 9.953208, 4.3097677, 9.490387,
                          7.674431, 9.396905, 10.347791, 6.3927646, 10.226669,
                          10.241062, 10.280587, 10.396974, 10.055647])))
# model training and testing settings
train_cfg = dict(sampler=None)
test_cfg = dict(mode='whole')