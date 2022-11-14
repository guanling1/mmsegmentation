# MaskFormer

[MaskFormer: Per-Pixel Classification is Not All You Need for Semantic Segmentation](https://arxiv.org/abs/2107.06278)

## Introduction

<!-- [ALGORITHM] -->

<a href="https://github.com/facebookresearch/MaskFormer/">Official Repo</a>

<a href="https://github.com/open-mmlab/mmdetection/blob/dev-3.x/mmdet/models/dense_heads/maskformer_head.py#L21">Code Snippet</a>

## Abstract

<!-- [ABSTRACT] -->

Modern approaches typically formulate semantic segmentation as a per-pixel classification task, while instance-level segmentation is handled with an alternative mask classification. Our key insight: mask classification is sufficiently general to solve both semantic- and instance-level segmentation tasks in a unified manner using the exact same model, loss, and training procedure. Following this observation, we propose MaskFormer, a simple mask classification model which predicts a set of binary masks, each associated with a single global class label prediction. Overall, the proposed mask classification-based method simplifies the landscape of effective approaches to semantic and panoptic segmentation tasks and shows excellent empirical results. In particular, we observe that MaskFormer outperforms per-pixel classification baselines when the number of classes is large. Our mask classification-based method outperforms both current state-of-the-art semantic (55.6 mIoU on ADE20K) and panoptic segmentation (52.7 PQ on COCO) models.

<!-- [IMAGE] -->

<div align=center>
<img src="https://user-images.githubusercontent.com/24582831/199215459-ea507126-aafe-4823-8eb1-ae6487509d5c.png" width="90%"/>
</div>

```bibtex
@article{cheng2021per,
  title={Per-pixel classification is not all you need for semantic segmentation},
  author={Cheng, Bowen and Schwing, Alex and Kirillov, Alexander},
  journal={Advances in Neural Information Processing Systems},
  volume={34},
  pages={17864--17875},
  year={2021}
}
```

### Usage

- MaskFormer model needs to install [MMDetection](https://github.com/open-mmlab/mmdetection) first.

```shell
pip install "mmdet>=3.0.0rc4"
```

If related MMDetection version unfounded, you can modify [related code](https://github.com/open-mmlab/mmdetection/blob/dev-3.x/mmdet/models/dense_heads/maskformer_head.py#L106) like [MMDetection PR](https://github.com/open-mmlab/mmdetection/pull/9176) on your own to fix its bug:

From

```python
if pixel_decoder_type == 'PixelDecoder' and (
        self.decoder_embed_dims != in_channels[-1]
        or enforce_decoder_input_project):
```

to

```python
if type(self.pixel_decoder) == PixelDecoder and (
        self.decoder_embed_dims != in_channels[-1]
        or enforce_decoder_input_project):
```

Which would treat `mmdet.PixelDecoder` the same with `PixelDecoder` in this MMDetection `if` conditional statement.

## Results and models

### ADE20K

| Method     | Backbone  | Crop Size | Lr schd | Mem (GB) | Inf time (fps) | mIoU  | mIoU(ms+flip) | config                                                                                                                                       | download                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------- | --------- | --------- | ------- | -------- | -------------- | ----- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| MaskFormer | R-50-D32  | 512x512   | 160000  | 3.29     | 42.20          | 44.29 | -             | [config](https://github.com/open-mmlab/mmsegmentation/blob/dev-1.x/configs/maskformer/maskformer_r50-d32_8xb2-160k_ade20k-512x512.py)        | [model](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_r50-d32_8xb2-160k_ade20k-512x512/maskformer_r50-d32_8xb2-160k_ade20k-512x512_20221030_182724-cbd39cc1.pth) \| [log](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_r50-d32_8xb2-160k_ade20k-512x512/maskformer_r50-d32_8xb2-160k_ade20k-512x512_20221030_182724.json)                             |
| MaskFormer | R-101-D32 | 512x512   | 160000  | 4.12     | 34.90          | 45.11 | -             | [config](https://github.com/open-mmlab/mmsegmentation/blob/dev-1.x/configs/maskformer/maskformer_r101-d32_8xb2-160k_ade20k-512x512.py)       | [model](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_r101-d32_8xb2-160k_ade20k-512x512/maskformer_r101-d32_8xb2-160k_ade20k-512x512_20221031_223053-c8e0931d.pth) \| [log](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_r101-d32_8xb2-160k_ade20k-512x512/maskformer_r101-d32_8xb2-160k_ade20k-512x512_20221031_223053.json)                         |
| MaskFormer | Swin-T    | 512x512   | 160000  | 3.73     | 40.53          | 46.99 | -             | [config](https://github.com/open-mmlab/mmsegmentation/blob/dev-1.x/configs/maskformer/maskformer_swin-t_upernet_8xb2-160k_ade20k-512x512.py) | [model](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_swin-t_upernet_8xb2-160k_ade20k-512x512/maskformer_swin-t_upernet_8xb2-160k_ade20k-512x512_20221102_111617-4f158299.pth) \| [log](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_swin-t_upernet_8xb2-160k_ade20k-512x512/maskformer_swin-t_upernet_8xb2-160k_ade20k-512x512_20221102_111617.json) |
| MaskFormer | Swin-S    | 512x512   | 160000  | 5.33     | 26.98          | 49.75 | -             | [config](https://github.com/open-mmlab/mmsegmentation/blob/dev-1.x/configs/maskformer/maskformer_swin-s_upernet_8xb2-160k_ade20k-512x512.py) | [model](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_swin-s_upernet_8xb2-160k_ade20k-512x512/maskformer_swin-s_upernet_8xb2-160k_ade20k-512x512_20221103_013242-3bec1052.pth) \| [log](https://download.openmmlab.com/mmsegmentation/v0.5/maskformer/maskformer_swin-s_upernet_8xb2-160k_ade20k-512x512/maskformer_swin-s_upernet_8xb2-160k_ade20k-512x512_20221103_013242.json) |

Note:

- All experiments of MaskFormer are implemented with 8 V100 (32G) GPUs with 2 samplers per GPU.
- The results of MaskFormer are relatively not stable, variance of `R-101-D32` is 44.7 to 46.0, variance of `Swin-S` is 49.0 to 49.8.
- The ResNet backbones utilized in MaskFormer models are standard `ResNet` rather than `ResNetV1c`.
- `MultiScaleFlipAug` is not supported in MMSegmentation 1.x version yet, we would add "ms+flip" results as soon as possible.