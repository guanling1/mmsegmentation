# SegNeXt

[SegNeXt: Rethinking Convolutional Attention Design for Semantic Segmentation](https://arxiv.org/abs/2209.08575)

## Introduction

<!-- [ALGORITHM] -->

<a href="https://github.com/visual-attention-network/segnext">Official Repo</a>

<a href="https://github.com/open-mmlab/mmsegmentation/blob/v0.31.0/mmseg/models/backbones/mscan.py#L328">Code Snippet</a>

## Abstract

<!-- [ABSTRACT] -->

We present SegNeXt, a simple convolutional network architecture for semantic segmentation. Recent transformer-based models have dominated the field of semantic segmentation due to the efficiency of self-attention in encoding spatial information. In this paper, we show that convolutional attention is a more efficient and effective way to encode contextual information than the self-attention mechanism in transformers. By re-examining the characteristics owned by successful segmentation models, we discover several key components leading to the performance improvement of segmentation models. This motivates us to design a novel convolutional attention network that uses cheap convolutional operations. Without bells and whistles, our SegNeXt significantly improves the performance of previous state-of-the-art methods on popular benchmarks, including ADE20K, Cityscapes, COCO-Stuff, Pascal VOC, Pascal Context, and iSAID. Notably, SegNeXt outperforms EfficientNet-L2 w/ NAS-FPN and achieves 90.6% mIoU on the Pascal VOC 2012 test leaderboard using only 1/10 parameters of it. On average, SegNeXt achieves about 2.0% mIoU improvements compared to the state-of-the-art methods on the ADE20K datasets with the same or fewer computations. Code is available at [this https URL](https://github.com/uyzhang/JSeg) (Jittor) and [this https URL](https://github.com/Visual-Attention-Network/SegNeXt) (Pytorch).

<!-- [IMAGE] -->

<div align=center>
<img src="https://user-images.githubusercontent.com/24582831/215688018-5d4c8366-7793-4fdf-9397-960a09fac951.png" width="70%"/>
</div>

```bibtex
@article{guo2022segnext,
  title={SegNeXt: Rethinking Convolutional Attention Design for Semantic Segmentation},
  author={Guo, Meng-Hao and Lu, Cheng-Ze and Hou, Qibin and Liu, Zhengning and Cheng, Ming-Ming and Hu, Shi-Min},
  journal={arXiv preprint arXiv:2209.08575},
  year={2022}
}
```

## Pretrained model

The pretrained model could be found [here](https://cloud.tsinghua.edu.cn/d/c15b25a6745946618462/) from [original repo](https://github.com/Visual-Attention-Network/SegNeXt).

## Results and models

### ADE20K

| Method  | Backbone | Crop Size | Lr schd | Mem (GB) | Inf time (fps) | mIoU  | mIoU(ms+flip) | config                                                                                                                               | download                                                                                                                                                                                                                                                                                                                                                                                       |
| ------- | -------- | --------- | ------- | -------- | -------------- | ----- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SegNeXt | MSCAN-T  | 512x512   | 160000  | 999      | 999            | 45.00 | 45.00         | [config](https://github.com/open-mmlab/mmsegmentation/blob/master/configs/segnext/segnext_mscan-t_1x16_512x512_adamw_160k_ade20k.py) | [model](https://download.openmmlab.com/mmsegmentation/v0.5/segmenter/segmenter_vit-t_mask_8x1_512x512_160k_ade20k/segmenter_vit-t_mask_8x1_512x512_160k_ade20k_20220105_151706-ffcf7509.pth) \| [log](https://download.openmmlab.com/mmsegmentation/v0.5/segmenter/segmenter_vit-t_mask_8x1_512x512_160k_ade20k/segmenter_vit-t_mask_8x1_512x512_160k_ade20k_20220105_151706.log.json)         |
| SegNeXt | MSCAN-S  | 512x512   | 160000  | 999      | 999            | 45.00 | 45.00         | [config](https://github.com/open-mmlab/mmsegmentation/blob/master/configs/segnext/segnext_mscan-s_1x16_512x512_adamw_160k_ade20k.py) | [model](https://download.openmmlab.com/mmsegmentation/v0.5/segmenter/segmenter_vit-s_linear_8x1_512x512_160k_ade20k/segmenter_vit-s_linear_8x1_512x512_160k_ade20k_20220105_151713-39658c46.pth) \| [log](https://download.openmmlab.com/mmsegmentation/v0.5/segmenter/segmenter_vit-s_linear_8x1_512x512_160k_ade20k/segmenter_vit-s_linear_8x1_512x512_160k_ade20k_20220105_151713.log.json) |
| SegNeXt | MSCAN-B  | 512x512   | 160000  | 999      | 999            | 45.00 | 45.00         | [config](https://github.com/open-mmlab/mmsegmentation/blob/master/configs/segnext/segnext_mscan-b_1x16_512x512_adamw_160k_ade20k.py) | [model](https://download.openmmlab.com/mmsegmentation/v0.5/segmenter/segmenter_vit-s_mask_8x1_512x512_160k_ade20k/segmenter_vit-s_mask_8x1_512x512_160k_ade20k_20220105_151706-511bb103.pth) \| [log](https://download.openmmlab.com/mmsegmentation/v0.5/segmenter/segmenter_vit-s_mask_8x1_512x512_160k_ade20k/segmenter_vit-s_mask_8x1_512x512_160k_ade20k_20220105_151706.log.json)         |

Note:

- The total batch sizes are 16. We only adopt single GPU training for SegNeXt because SyncBN (mainly in `OverlapPatchEmbed` modules of `MSCAN`) of certain PyTorch version (such as PyTorch 1.9) would result in bad performance.

- To re-implement the same results in training logs with our provided ckpts, the random seeds must be set identically because Non-negative Matrix Factorization (NMF) in `LightHamHead` would generate initialization values by random seed.

- This model performance is sensitive to the seed values used, please refer to the log file for the specific settings of the seed. If you choose a different seed, the results might differ from the table results.