import torch
from mmcv.ops import CrissCrossAttention

from ..builder import HEADS
from .fcn_head import FCNHead


@HEADS.register_module()
class CCHead(FCNHead):
    """CCNet: Criss-Cross Attention for Semantic Segmentation.

    This head is the implementation of `CCNet
    <https://arxiv.org/abs/1811.11721>`_.

    Args:
        recurrence (int): Number of recurrence of Criss Cross Attention
            module. Default: 2.
    """

    def __init__(self, recurrence=2, **kwargs):
        super(CCHead, self).__init__(num_convs=2, **kwargs)
        self.recurrence = recurrence
        self.cca = CrissCrossAttention(self.channels)

    def forward(self, inputs):
        x = self._transform_inputs(inputs)
        output = self.convs[0](x)
        for _ in range(self.recurrence):
            output = self.cca(output)
        output = self.convs[1](output)
        if self.concat_input:
            output = self.conv_cat(torch.cat([x, output], dim=1))
        output = self.cls_seg(output)
        return output
