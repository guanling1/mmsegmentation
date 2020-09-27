import pytest
import torch
from mmcv.cnn import ConvModule
from mmcv.utils.parrots_wrapper import _BatchNorm
from torch import nn

from mmseg.models.backbones.unet import (BasicConvBlock, DeconvUpsample,
                                         InterpUpsample, UNet, UpConvBlock)


def check_norm_state(modules, train_state):
    """Check if norm layer is in correct train state."""
    for mod in modules:
        if isinstance(mod, _BatchNorm):
            if mod.training != train_state:
                return False
    return True


def test_unet_basic_conv_block():
    with pytest.raises(AssertionError):
        # Not implemented yet.
        dcn = dict(type='DCN', deform_groups=1, fallback_on_stride=False)
        BasicConvBlock(64, 64, dcn=dcn)

    with pytest.raises(AssertionError):
        # Not implemented yet.
        plugins = [
            dict(
                cfg=dict(type='ContextBlock', ratio=1. / 16),
                position='after_conv3')
        ]
        BasicConvBlock(64, 64, plugins=plugins)

    with pytest.raises(AssertionError):
        # Not implemented yet
        plugins = [
            dict(
                cfg=dict(
                    type='GeneralizedAttention',
                    spatial_range=-1,
                    num_heads=8,
                    attention_type='0010',
                    kv_stride=2),
                position='after_conv2')
        ]
        BasicConvBlock(64, 64, plugins=plugins)

    # test BasicConvBlock with checkpoint forward
    block = BasicConvBlock(16, 16, with_cp=True)
    assert block.with_cp
    x = torch.randn(1, 16, 64, 64, requires_grad=True)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 16, 64, 64])

    block = BasicConvBlock(16, 16, with_cp=False)
    assert not block.with_cp
    x = torch.randn(1, 16, 64, 64)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 16, 64, 64])

    # test BasicConvBlock with stride convolution to downsample
    block = BasicConvBlock(16, 16, stride=2)
    x = torch.randn(1, 16, 64, 64)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 16, 32, 32])

    # test BasicConvBlock structure and forward
    block = BasicConvBlock(16, 64, num_convs=3, dilation=3)
    assert block.convs[0].conv.in_channels == 16
    assert block.convs[0].conv.out_channels == 64
    assert block.convs[0].conv.kernel_size == (3, 3)
    assert block.convs[0].conv.dilation == (1, 1)
    assert block.convs[0].conv.padding == (1, 1)

    assert block.convs[1].conv.in_channels == 64
    assert block.convs[1].conv.out_channels == 64
    assert block.convs[1].conv.kernel_size == (3, 3)
    assert block.convs[1].conv.dilation == (3, 3)
    assert block.convs[1].conv.padding == (3, 3)

    assert block.convs[2].conv.in_channels == 64
    assert block.convs[2].conv.out_channels == 64
    assert block.convs[2].conv.kernel_size == (3, 3)
    assert block.convs[2].conv.dilation == (3, 3)
    assert block.convs[2].conv.padding == (3, 3)


def test_deconv_upsamle():
    with pytest.raises(AssertionError):
        # test 2X upsample. only support for 2X upsample, so the stride
        # should be equal to 2.
        DeconvUpsample(64, 32, stride=1)

    with pytest.raises(AssertionError):
        # test 2X upsample. only support for 2X upsample, so the stride
        # should be equal to 2.
        DeconvUpsample(64, 32, stride=3)

    with pytest.raises(AssertionError):
        # test 2X upsample. only support for 2X upsample, so the stride
        # should be equal to 2 and (kernel_size-2*padding-2)=0.
        DeconvUpsample(64, 32, kernel_size=3, stride=2, padding=1)

    with pytest.raises(AssertionError):
        # test 2X upsample. only support for 2X upsample, so the stride
        # should be equal to 2 and (kernel_size-2*padding-2)=0.
        DeconvUpsample(64, 32, kernel_size=4, stride=2, padding=2)

    # test DeconvUpsample with checkpoint forward and upsample 2X.
    block = DeconvUpsample(64, 32, with_cp=True)
    assert block.with_cp
    x = torch.randn(1, 64, 128, 128, requires_grad=True)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    block = DeconvUpsample(64, 32, with_cp=False)
    assert not block.with_cp
    x = torch.randn(1, 64, 128, 128)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test DeconvUpsample with different kernel size for upsample 2X.
    block = DeconvUpsample(64, 32, kernel_size=2, stride=2, padding=0)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    block = DeconvUpsample(64, 32, kernel_size=6, stride=2, padding=2)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])


def test_interp_upsamle():
    # test InterpUpsample with checkpoint forward and upsample 2X.
    block = InterpUpsample(64, 32, with_cp=True)
    assert block.with_cp
    x = torch.randn(1, 64, 128, 128, requires_grad=False)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    block = InterpUpsample(64, 32, with_cp=False)
    assert not block.with_cp
    x = torch.randn(1, 64, 128, 128)
    x_out = block(x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test InterpUpsample with conv_first=False for upsample 2X.
    block = InterpUpsample(64, 32, conv_first=False)
    x = torch.randn(1, 64, 128, 128)
    x_out = block(x)
    assert isinstance(block.interp_upsample[0], nn.Upsample)
    assert isinstance(block.interp_upsample[1], ConvModule)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test InterpUpsample with conv_first=True for upsample 2X.
    block = InterpUpsample(64, 32, conv_first=True)
    x = torch.randn(1, 64, 128, 128)
    x_out = block(x)
    assert isinstance(block.interp_upsample[0], ConvModule)
    assert isinstance(block.interp_upsample[1], nn.Upsample)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test InterpUpsample with bilinear upsample for upsample 2X.
    block = InterpUpsample(
        64,
        32,
        conv_first=False,
        upsampe_cfg=dict(scale_factor=2, mode='bilinear', align_corners=False))
    x = torch.randn(1, 64, 128, 128)
    x_out = block(x)
    assert isinstance(block.interp_upsample[0], nn.Upsample)
    assert isinstance(block.interp_upsample[1], ConvModule)
    assert x_out.shape == torch.Size([1, 32, 256, 256])
    assert block.interp_upsample[0].mode == 'bilinear'

    # test InterpUpsample with nearest upsample for upsample 2X.
    block = InterpUpsample(
        64,
        32,
        conv_first=False,
        upsampe_cfg=dict(scale_factor=2, mode='nearest'))
    x = torch.randn(1, 64, 128, 128)
    x_out = block(x)
    assert isinstance(block.interp_upsample[0], nn.Upsample)
    assert isinstance(block.interp_upsample[1], ConvModule)
    assert x_out.shape == torch.Size([1, 32, 256, 256])
    assert block.interp_upsample[0].mode == 'nearest'


def test_up_conv_block():
    with pytest.raises(AssertionError):
        # Not implemented yet.
        dcn = dict(type='DCN', deform_groups=1, fallback_on_stride=False)
        UpConvBlock(BasicConvBlock, 64, 32, 32, dcn=dcn)

    with pytest.raises(AssertionError):
        # Not implemented yet.
        plugins = [
            dict(
                cfg=dict(type='ContextBlock', ratio=1. / 16),
                position='after_conv3')
        ]
        UpConvBlock(BasicConvBlock, 64, 32, 32, plugins=plugins)

    with pytest.raises(AssertionError):
        # Not implemented yet
        plugins = [
            dict(
                cfg=dict(
                    type='GeneralizedAttention',
                    spatial_range=-1,
                    num_heads=8,
                    attention_type='0010',
                    kv_stride=2),
                position='after_conv2')
        ]
        UpConvBlock(BasicConvBlock, 64, 32, 32, plugins=plugins)

    # test UpConvBlock with checkpoint forward and upsample 2X.
    block = UpConvBlock(BasicConvBlock, 64, 32, 32, with_cp=True)
    skip_x = torch.rand(1, 32, 256, 256, requires_grad=True)
    x = torch.randn(1, 64, 128, 128, requires_grad=True)
    x_out = block(skip_x, x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test UpConvBlock with upsample=True for upsample 2X. The spatial size of
    # skip_x is 2X larger than x.
    block = UpConvBlock(BasicConvBlock, 64, 32, 32, upsample=True)
    skip_x = torch.rand(1, 32, 256, 256)
    x = torch.randn(1, 64, 128, 128)
    x_out = block(skip_x, x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test UpConvBlock with upsample=False for upsample 2X. The spatial size of
    # skip_x is the same as that of x.
    block = UpConvBlock(BasicConvBlock, 64, 32, 32, upsample=False)
    skip_x = torch.rand(1, 32, 256, 256)
    x = torch.randn(1, 64, 256, 256)
    x_out = block(skip_x, x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test UpConvBlock with different upsample method for upsample 2X.
    # The upsample method is interpolation upsample (bilinear or nearest).
    block = UpConvBlock(
        BasicConvBlock,
        64,
        32,
        32,
        upsample=True,
        upsample_cfg=dict(
            type='interp_up',
            upsampe_cfg=dict(
                scale_factor=2, mode='bilinear', align_corners=False)))
    skip_x = torch.rand(1, 32, 256, 256)
    x = torch.randn(1, 64, 128, 128)
    x_out = block(skip_x, x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test UpConvBlock with different upsample method for upsample 2X.
    # The upsample method is deconvolution upsample.
    block = UpConvBlock(
        BasicConvBlock,
        64,
        32,
        32,
        upsample=True,
        upsample_cfg=dict(
            type='deconv_up2x', kernel_size=4, stride=2, padding=1))
    skip_x = torch.rand(1, 32, 256, 256)
    x = torch.randn(1, 64, 128, 128)
    x_out = block(skip_x, x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    # test BasicConvBlock structure and forward
    block = UpConvBlock(
        conv_block=BasicConvBlock,
        in_channels=64,
        skip_channels=32,
        out_channels=32,
        num_convs=3,
        dilation=3,
        upsample=True,
        upsample_cfg=dict(
            type='interp_up',
            upsampe_cfg=dict(
                scale_factor=2, mode='bilinear', align_corners=False)))
    skip_x = torch.rand(1, 32, 256, 256)
    x = torch.randn(1, 64, 128, 128)
    x_out = block(skip_x, x)
    assert x_out.shape == torch.Size([1, 32, 256, 256])

    assert block.conv_block.convs[0].conv.in_channels == 64
    assert block.conv_block.convs[0].conv.out_channels == 32
    assert block.conv_block.convs[0].conv.kernel_size == (3, 3)
    assert block.conv_block.convs[0].conv.dilation == (1, 1)
    assert block.conv_block.convs[0].conv.padding == (1, 1)

    assert block.conv_block.convs[1].conv.in_channels == 32
    assert block.conv_block.convs[1].conv.out_channels == 32
    assert block.conv_block.convs[1].conv.kernel_size == (3, 3)
    assert block.conv_block.convs[1].conv.dilation == (3, 3)
    assert block.conv_block.convs[1].conv.padding == (3, 3)

    assert block.conv_block.convs[2].conv.in_channels == 32
    assert block.conv_block.convs[2].conv.out_channels == 32
    assert block.conv_block.convs[2].conv.kernel_size == (3, 3)
    assert block.conv_block.convs[2].conv.dilation == (3, 3)
    assert block.conv_block.convs[2].conv.padding == (3, 3)

    assert block.upsample.interp_upsample[1].conv.in_channels == 64
    assert block.upsample.interp_upsample[1].conv.out_channels == 32
    assert block.upsample.interp_upsample[1].conv.kernel_size == (1, 1)
    assert block.upsample.interp_upsample[1].conv.dilation == (1, 1)
    assert block.upsample.interp_upsample[1].conv.padding == (0, 0)


def test_unet():
    with pytest.raises(AssertionError):
        # Not implemented yet.
        dcn = dict(type='DCN', deform_groups=1, fallback_on_stride=False)
        UNet(3, 64, 5, dcn=dcn)

    with pytest.raises(AssertionError):
        # Not implemented yet.
        plugins = [
            dict(
                cfg=dict(type='ContextBlock', ratio=1. / 16),
                position='after_conv3')
        ]
        UNet(3, 64, 5, plugins=plugins)

    with pytest.raises(AssertionError):
        # Not implemented yet
        plugins = [
            dict(
                cfg=dict(
                    type='GeneralizedAttention',
                    spatial_range=-1,
                    num_heads=8,
                    attention_type='0010',
                    kv_stride=2),
                position='after_conv2')
        ]
        UNet(3, 64, 5, plugins=plugins)

    with pytest.raises(AssertionError):
        # Check whether the input image size can be devisible by the whole
        # downsample rate of the encoder. The whole downsample rate of this
        # case is 8.
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=4,
            strides=(1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2),
            dec_num_convs=(2, 2, 2),
            downsamples=(True, True, True),
            enc_dilations=(1, 1, 1, 1),
            dec_dilations=(1, 1, 1))
        x = torch.randn(2, 3, 65, 65)
        unet(x)

    with pytest.raises(AssertionError):
        # Check whether the input image size can be devisible by the whole
        # downsample rate of the encoder. The whole downsample rate of this
        # case is 16.
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=5,
            strides=(1, 1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2),
            downsamples=(True, True, True, True),
            enc_dilations=(1, 1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1))
        x = torch.randn(2, 3, 65, 65)
        unet(x)

    with pytest.raises(AssertionError):
        # Check whether the input image size can be devisible by the whole
        # downsample rate of the encoder. The whole downsample rate of this
        # case is 32.
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=6,
            strides=(1, 1, 1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2, 2),
            downsamples=(True, True, True, True, True),
            enc_dilations=(1, 1, 1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1, 1))
        x = torch.randn(2, 3, 65, 65)
        unet(x)

    with pytest.raises(AssertionError):
        # Check if num_stages matchs strides, len(strides)=num_stages
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=5,
            strides=(1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2),
            downsamples=(True, True, True, True),
            enc_dilations=(1, 1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1))
        x = torch.randn(2, 3, 64, 64)
        unet(x)

    with pytest.raises(AssertionError):
        # Check if num_stages matchs strides, len(enc_num_convs)=num_stages
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=5,
            strides=(1, 1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2),
            downsamples=(True, True, True, True),
            enc_dilations=(1, 1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1))
        x = torch.randn(2, 3, 64, 64)
        unet(x)

    with pytest.raises(AssertionError):
        # Check if num_stages matchs strides, len(dec_num_convs)=num_stages-1
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=5,
            strides=(1, 1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2, 2),
            downsamples=(True, True, True, True),
            enc_dilations=(1, 1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1))
        x = torch.randn(2, 3, 64, 64)
        unet(x)

    with pytest.raises(AssertionError):
        # Check if num_stages matchs strides, len(downsamples)=num_stages-1
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=5,
            strides=(1, 1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2),
            downsamples=(True, True, True),
            enc_dilations=(1, 1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1))
        x = torch.randn(2, 3, 64, 64)
        unet(x)

    with pytest.raises(AssertionError):
        # Check if num_stages matchs strides, len(enc_dilations)=num_stages
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=5,
            strides=(1, 1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2),
            downsamples=(True, True, True, True),
            enc_dilations=(1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1))
        x = torch.randn(2, 3, 64, 64)
        unet(x)

    with pytest.raises(AssertionError):
        # Check if num_stages matchs strides, len(dec_dilations)=num_stages-1
        unet = UNet(
            in_channels=3,
            base_channels=64,
            num_stages=5,
            strides=(1, 1, 1, 1, 1),
            enc_num_convs=(2, 2, 2, 2, 2),
            dec_num_convs=(2, 2, 2, 2),
            downsamples=(True, True, True, True),
            enc_dilations=(1, 1, 1, 1, 1),
            dec_dilations=(1, 1, 1, 1, 1))
        x = torch.randn(2, 3, 64, 64)
        unet(x)

    # test UNet norm_eval=True
    unet = UNet(
        in_channels=3,
        base_channels=64,
        num_stages=5,
        strides=(1, 1, 1, 1, 1),
        enc_num_convs=(2, 2, 2, 2, 2),
        dec_num_convs=(2, 2, 2, 2),
        downsamples=(True, True, True, True),
        enc_dilations=(1, 1, 1, 1, 1),
        dec_dilations=(1, 1, 1, 1),
        norm_eval=True)
    unet.train()
    assert check_norm_state(unet.modules(), False)

    # test UNet forward and outputs. The whole downsample rate is 16.
    unet = UNet(
        in_channels=3,
        base_channels=64,
        num_stages=5,
        strides=(1, 1, 1, 1, 1),
        enc_num_convs=(2, 2, 2, 2, 2),
        dec_num_convs=(2, 2, 2, 2),
        downsamples=(True, True, True, True),
        enc_dilations=(1, 1, 1, 1, 1),
        dec_dilations=(1, 1, 1, 1))

    x = torch.randn(2, 3, 512, 512)
    x_outs = unet(x)
    assert x_outs[0].shape == torch.Size([2, 1024, 32, 32])
    assert x_outs[1].shape == torch.Size([2, 512, 64, 64])
    assert x_outs[2].shape == torch.Size([2, 256, 128, 128])
    assert x_outs[3].shape == torch.Size([2, 128, 256, 256])
    assert x_outs[4].shape == torch.Size([2, 64, 512, 512])

    # test UNet forward and outputs. The whole downsample rate is 8.
    unet = UNet(
        in_channels=3,
        base_channels=64,
        num_stages=5,
        strides=(1, 1, 1, 1, 1),
        enc_num_convs=(2, 2, 2, 2, 2),
        dec_num_convs=(2, 2, 2, 2),
        downsamples=(True, True, True, False),
        enc_dilations=(1, 1, 1, 1, 1),
        dec_dilations=(1, 1, 1, 1))

    x = torch.randn(2, 3, 512, 512)
    x_outs = unet(x)
    assert x_outs[0].shape == torch.Size([2, 1024, 64, 64])
    assert x_outs[1].shape == torch.Size([2, 512, 64, 64])
    assert x_outs[2].shape == torch.Size([2, 256, 128, 128])
    assert x_outs[3].shape == torch.Size([2, 128, 256, 256])
    assert x_outs[4].shape == torch.Size([2, 64, 512, 512])

    # test UNet forward and outputs. The whole downsample rate is 4.
    unet = UNet(
        in_channels=3,
        base_channels=64,
        num_stages=5,
        strides=(1, 1, 1, 1, 1),
        enc_num_convs=(2, 2, 2, 2, 2),
        dec_num_convs=(2, 2, 2, 2),
        downsamples=(True, True, False, False),
        enc_dilations=(1, 1, 1, 1, 1),
        dec_dilations=(1, 1, 1, 1))

    x = torch.randn(2, 3, 512, 512)
    x_outs = unet(x)
    assert x_outs[0].shape == torch.Size([2, 1024, 128, 128])
    assert x_outs[1].shape == torch.Size([2, 512, 128, 128])
    assert x_outs[2].shape == torch.Size([2, 256, 128, 128])
    assert x_outs[3].shape == torch.Size([2, 128, 256, 256])
    assert x_outs[4].shape == torch.Size([2, 64, 512, 512])

    # test UNet forward and outputs. The whole downsample rate is 2.
    unet = UNet(
        in_channels=3,
        base_channels=64,
        num_stages=5,
        strides=(1, 1, 1, 1, 1),
        enc_num_convs=(2, 2, 2, 2, 2),
        dec_num_convs=(2, 2, 2, 2),
        downsamples=(True, False, False, False),
        enc_dilations=(1, 1, 1, 1, 1),
        dec_dilations=(1, 1, 1, 1))

    x = torch.randn(2, 3, 512, 512)
    x_outs = unet(x)
    assert x_outs[0].shape == torch.Size([2, 1024, 256, 256])
    assert x_outs[1].shape == torch.Size([2, 512, 256, 256])
    assert x_outs[2].shape == torch.Size([2, 256, 256, 256])
    assert x_outs[3].shape == torch.Size([2, 128, 256, 256])
    assert x_outs[4].shape == torch.Size([2, 64, 512, 512])

    # test UNet forward and outputs. The whole downsample rate is 1.
    unet = UNet(
        in_channels=3,
        base_channels=64,
        num_stages=5,
        strides=(1, 1, 1, 1, 1),
        enc_num_convs=(2, 2, 2, 2, 2),
        dec_num_convs=(2, 2, 2, 2),
        downsamples=(False, False, False, False),
        enc_dilations=(1, 1, 1, 1, 1),
        dec_dilations=(1, 1, 1, 1))

    x = torch.randn(2, 3, 512, 512)
    x_outs = unet(x)
    assert x_outs[0].shape == torch.Size([2, 1024, 512, 512])
    assert x_outs[1].shape == torch.Size([2, 512, 512, 512])
    assert x_outs[2].shape == torch.Size([2, 256, 512, 512])
    assert x_outs[3].shape == torch.Size([2, 128, 512, 512])
    assert x_outs[4].shape == torch.Size([2, 64, 512, 512])
