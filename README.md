# Instance Segmentation with Tiny PASCAL VOC Dataset
<p align="left">
    <a>
        <img src=https://img.shields.io/badge/python-3.6.12-green>
    </a>
    <a>
        <img src=https://img.shields.io/badge/pytorch-1.7.0-orange>
    </a>
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</p>

This repository gathers is the code for homework in class.
To read the detailed for what is this, please, refer to [my report](https://github.com/purpleFar/instance-segmentation/blob/master/HW3%20Report_0856735.pdf).

## Hardware
The following specs were used to create the original solution.
- Linux
- Intel(R) Xeon(R) Platinum 8260M CPU @ 2.40GHz
- NVIDIA Tesla T4

## Outline
To reproduct my result without retrainig, do the following steps:
1. [Installation](#installation)
2. [Download Data](#download-data)
3. [Download Pretrained models](#pretrained-models)
4. [Inference](#inference)

## Installation
See [this](https://github.com/purpleFar/instance-segmentation/blob/master/orgREADME.md) to know how to use mmdetection.
And [here](https://github.com/purpleFar/instance-segmentation/blob/master/get_started.md) is how to install it.

## Download Data
The Tiny PASCAL VOC Dataset download at [here](https://drive.google.com/drive/folders/1fGg03EdBAxjFumGHHNhMrz2sMLLH04FK?usp=sharing).
Unzip them then you can see following structure:
```
instance-segmentation/
    ├── train_images
    │   ├── 2011_003271.jpg
    │   ├── 2011_003256.jpg
    │   │   .
    │   │   .
    │   │   .
    │   └── 2007_000033.jpg
    ├── test_images
    │   ├── 2011_003146.jpg
    │   ├── 2011_002812.jpg
    │   │   .
    │   │   .
    │   │   .
    │   └── 2007_000629.jpg
    ├── pascal_train.json
    ├── test.json
    │   .
    │   .
    │   .
```

## Preprocessing
To train from scratch, split pascal_train.json into training set and validation set is required. Run following command.
```bash=
$ python cut_train_val.py
```
then there is some file in preprocess_file folder like this
```
instance-segmentation/
    ├── train.json
    ├── val.json
    │   .
    │   .
    │   .
```

## Train models
To train models, run following command.
```bash=
$ python tool/train.py config/cascade_rcnn/cascade_mask_rcnn_x101_32x4d_fpn_hw3.py
```

## Pretrained models
You can download pretrained model that used for my submission from [link](https://drive.google.com/file/d/13GYwPxKHyORyL1_V0OYgLnPPCIePhU8S/view?usp=sharing). 
Unzip them and put then in structure:
```
instance-segmentation/work_dirs/cascade_mask_rcnn_x101_32x4d_fpn_hw3
    └── epoch_28.pth
```

## Inference
If trained weights are prepared, you can create a file containing the bboxes and segmentation for each picture in test set.

Using the pre-trained model, enter the command:
```bash=
$ python inference_demo.py
```
And you can see the 0856735_xx.json in your folder