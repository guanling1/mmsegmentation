from .ann_head import ANNHead
from .aspp_head import ASPPHead
from .cc_head import CCHead
from .da_head import DAHead
from .fcn_head import FCNHead
from .gc_head import GCHead
from .nl_head import NLHead
from .ocr_head import OCRHead
from .psa_head import PSAHead
from .psp_head import PSPHead
from .uper_head import UPerHead

__all__ = [
    'FCNHead', 'PSPHead', 'ASPPHead', 'PSAHead', 'NLHead', 'GCHead', 'CCHead',
    'UPerHead', 'ANNHead', 'DAHead', 'OCRHead'
]
