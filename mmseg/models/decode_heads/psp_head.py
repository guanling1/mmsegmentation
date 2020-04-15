import torch
import torch.nn as nn
import torch.nn.functional as F

from mmseg.ops import ConvModule
from ..registry import HEADS
from .decode_head import DecodeHead


@HEADS.register_module
class PSPHead(DecodeHead):
    """Pyramid Scene Parsing Network

        This head is the implementation of PSPHead
        in (https://arxiv.org/abs/1612.01105)
    """

    def __init__(self, pool_scales=(1, 2, 3, 6), **kwargs):
        super(PSPHead, self).__init__(**kwargs)
        self.psp_modules = nn.ModuleList()
        assert isinstance(pool_scales, (list, tuple))
        self.pool_scales = pool_scales
        for pool_scale in pool_scales:
            self.psp_modules.append(
                nn.Sequential(
                    nn.AdaptiveAvgPool2d(pool_scale),
                    ConvModule(
                        self.in_channels,
                        self.channels,
                        1,
                        conv_cfg=self.conv_cfg,
                        norm_cfg=self.norm_cfg)))
        self.bottleneck = ConvModule(
            self.in_channels + len(pool_scales) * self.channels,
            self.channels,
            3,
            padding=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg)

    def forward(self, inputs):
        x = self._transform_inputs(inputs)
        psp_outs = [x]
        for psp_module in self.psp_modules:
            psp_out = psp_module(x)
            upsampled_psp_out = F.interpolate(
                psp_out,
                size=x.size()[2:],
                mode='bilinear',
                align_corners=False)
            psp_outs.append(upsampled_psp_out)
        psp_outs = torch.cat(psp_outs, dim=1)
        output = self.bottleneck(psp_outs)
        output = self.cls_seg(output)
        return output
