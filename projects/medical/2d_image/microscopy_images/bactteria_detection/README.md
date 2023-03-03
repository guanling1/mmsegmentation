# Bactteria detection with darkfield microscopy

## Description

This project support **`Bactteria detection with darkfield microscopy`**, and the dataset used in this project can be downloaded from [here](https://tianchi.aliyun.com/dataset/94411).

### Dataset Overview

Spirochaeta is a genus of bacteria classified within the phylum Spirochaetes. Included in this dataset are 366 darkfield microscopy images and manually annotated masks which can be used for classification and segmentation purposes. Detecting bacteria in blood could have a huge significance for research in both the medical and computer science field.

It was gathered and annotated by students (hand-on experience)
It has more than just one targeted class (blood cell and bacteria were annotated)
It is highly imbalanced, so naive loss functions would work less properly

### Original Statistic Information

| Dataset name                                                    | Anatomical region | Task type    | Modality   | Num. Classes | Train/Val/Test Images | Train/Val/Test Labeled | Release Date | License                                                         |
| --------------------------------------------------------------- | ----------------- | ------------ | ---------- | ------------ | --------------------- | ---------------------- | ------------ | --------------------------------------------------------------- |
| [Bactteria detection](https://tianchi.aliyun.com/dataset/94411) | bacteria          | segmentation | microscopy | 3            | 366/-/-               | yes/-/-                | 2017         | [CC-BY-NC 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

|  Class Name  | Num. Train | Pct. Train | Num. Val | Pct. Val | Num. Test | Pct. Test |
| :----------: | :--------: | :--------: | :------: | :------: | :-------: | :-------: |
|  background  |    366     |    85.9    |    -     |    -     |     -     |     -     |
| erythrocytes |    345     |   13.03    |    -     |    -     |     -     |     -     |
| spirochaete  |    288     |    1.07    |    -     |    -     |     -     |     -     |

Note:

- `Pct` means percentage of pixels in this category in all pixels.

### Visualization

![bac](https://raw.githubusercontent.com/uni-medical/medical-datasets-visualization/main/2d/semantic_seg/microscopy_images/bactteria_detection/bactteria_detection_dataset.png)

### Prerequisites

- Python v3.8
- PyTorch v1.10.0
- pillow(PIL) v9.3.0
- scikit-learn(sklearn) v1.2.0
- [MIM](https://github.com/open-mmlab/mim) v0.3.4
- [MMCV](https://github.com/open-mmlab/mmcv) v2.0.0rc4
- [MMEngine](https://github.com/open-mmlab/mmengine) v0.2.0 or higher
- [MMSegmentation](https://github.com/open-mmlab/mmsegmentation) v1.0.0rc5

All the commands below rely on the correct configuration of PYTHONPATH, which should point to the project's directory so that Python can locate the module files. In bactteria_detection/ root directory, run the following line to add the current directory to PYTHONPATH:

```shell
export PYTHONPATH=`pwd`:$PYTHONPATH
```

### Dataset preparing

- download dataset from [here](https://tianchi.aliyun.com/dataset/94411) and decompression data to path 'data/'.
- run script `"python tools/prepare_dataset.py"` to format data and change folder structure as below.
- run script `"python ../../tools/split_seg_dataset.py"` to split dataset and generate `train.txt`, `val.txt` and `test.txt`. If the label of official validation set and test set can't be obtained, we generate `train.txt` and `val.txt` from the training set randomly.

```none
  mmsegmentation
  ├── mmseg
  ├── projects
  │   ├── medical
  │   │   ├── 2d_image
  │   │   │   ├── microscopy_images
  │   │   │   │   ├── bactteria_detection
  │   │   │   │   │   ├── configs
  │   │   │   │   │   ├── datasets
  │   │   │   │   │   ├── tools
  │   │   │   │   │   ├── data
  │   │   │   │   │   │   ├── train.txt
  │   │   │   │   │   │   ├── val.txt
  │   │   │   │   │   │   ├── images
  │   │   │   │   │   │   │   ├── train
  │   │   │   │   |   │   │   │   ├── xxx.png
  │   │   │   │   |   │   │   │   ├── ...
  │   │   │   │   |   │   │   │   └── xxx.png
  │   │   │   │   │   │   ├── masks
  │   │   │   │   │   │   │   ├── train
  │   │   │   │   |   │   │   │   ├── xxx.png
  │   │   │   │   |   │   │   │   ├── ...
  │   │   │   │   |   │   │   │   └── xxx.png
```

### Divided Dataset Information

***Note: The table information below is divided by ourselves.***

|  Class Name  | Num. Train | Pct. Train | Num. Val | Pct. Val | Num. Test | Pct. Test |
| :----------: | :--------: | :--------: | :------: | :------: | :-------: | :-------: |
|  background  |    292     |   85.66    |    74    |   86.7   |     -     |     -     |
| erythrocytes |    274     |   13.25    |    71    |  12.29   |     -     |     -     |
| spirochaete  |    231     |    1.09    |    57    |   1.01   |     -     |     -     |

### Training commands

```shell
mim train mmseg ./configs/${CONFIG_PATH}
```

To train on multiple GPUs, e.g. 8 GPUs, run the following command:

```shell
mim train mmseg ./configs/${CONFIG_PATH}  --launcher pytorch --gpus 8
```

### Testing commands

```shell
mim test mmseg ./configs/${CONFIG_PATH}  --checkpoint ${CHECKPOINT_PATH}
```

<!-- List the results as usually done in other model's README. [Example](https://github.com/open-mmlab/mmsegmentation/tree/dev-1.x/configs/fcn#results-and-models)

You should claim whether this is based on the pre-trained weights, which are converted from the official release; or it's a reproduced result obtained from retraining the model in this project. -->

## Results

### Bactteria detection with darkfield microscopy

|     Method      | Backbone | Crop Size |   lr   | mIoU  | mDice |                                                                                                      config                                                                                                      |
| :-------------: | :------: | :-------: | :----: | :---: | :---: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| fcn_unet_s5-d16 |   unet   |  512x512  |  0.01  | 76.48 | 84.68 |  [config](https://github.com/open-mmlab/mmsegmentation/tree/dev-1.x/projects/medical/2d_image/microscopy_images/bactteria_detection/configs/fcn-unet-s5-d16_unet_1xb16-0.01-20k_bactteria-detection-512x512.py)  |
| fcn_unet_s5-d16 |   unet   |  512x512  | 0.001  | 61.06 | 63.69 | [config](https://github.com/open-mmlab/mmsegmentation/tree/dev-1.x/projects/medical/2d_image/microscopy_images/bactteria_detection/configs/fcn-unet-s5-d16_unet_1xb16-0.001-20k_bactteria-detection-512x512.py)  |
| fcn_unet_s5-d16 |   unet   |  512x512  | 0.0001 | 58.87 | 62.42 | [config](https://github.com/open-mmlab/mmsegmentation/tree/dev-1.x/projects/medical/2d_image/microscopy_images/bactteria_detection/configs/fcn-unet-s5-d16_unet_1xb16-0.0001-20k_bactteria-detection-512x512.py) |

## Checklist

- [x] Milestone 1: PR-ready, and acceptable to be one of the `projects/`.

  - [x] Finish the code

  - [x] Basic docstrings & proper citation

  - [x] Test-time correctness

  - [x] A full README

- [x] Milestone 2: Indicates a successful model implementation.

  - [x] Training-time correctness

- [ ] Milestone 3: Good to be a part of our core package!

  - [ ] Type hints and docstrings

  - [ ] Unit tests

  - [ ] Code polishing

  - [ ] Metafile.yml

- [ ] Move your modules into the core package following the codebase's file hierarchy structure.

- [ ] Refactor your modules into the core package following the codebase's file hierarchy structure.