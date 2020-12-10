# -*- coding: utf-8 -*-
import os
import json
from PIL import Image
from mmdet.apis import init_detector, inference_detector
import numpy as np
from itertools import groupby
from pycocotools import mask as maskutil


def binary_mask_to_rle(binary_mask):
    rle = {'counts': [], 'size': list(binary_mask.shape)}
    counts = rle.get('counts')
    for i, (value, elements) in enumerate(groupby(binary_mask.ravel(order='F'))):
        if i == 0 and value == 1:
            counts.append(0)
        counts.append(len(list(elements)))
    compressed_rle = maskutil.frPyObjects(rle, rle.get('size')[0], rle.get('size')[1])
    compressed_rle['counts'] = str(compressed_rle['counts'], encoding='utf-8')
    return compressed_rle


# Specify the path to model config and checkpoint file
# config_file = 'configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco_hw2.py'
config_file = 'configs/cascade_rcnn/cascade_mask_rcnn_x101_32x4d_fpn_hw3.py'
checkpoint_file = 'work_dirs/cascade_mask_rcnn_x101_32x4d_fpn_hw3/epoch_28.pth'
coco_result = []

with open('test.json') as f:
    test = json.load(f)

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device='cuda:0')

for img_dict in test['images']:
    print(img_dict['file_name'])
    bboxs, segs = inference_detector(model, os.path.join('test_images',img_dict['file_name']))
    for i in range(20):
        for box_indx in range(len(bboxs[i])):
            w, h = segs[i][box_indx].shape
            if sum(sum(segs[i][box_indx])) > w*h/10000:
                coco_result.append({'image_id':img_dict['id'],
                                    'score':float(bboxs[i][box_indx][-1]),
                                    'category_id':i+1,
                                    'segmentation':binary_mask_to_rle(segs[i][box_indx])})

with open('0856735_4.json','w', encoding='utf-8') as f:
   json.dump(coco_result, f, ensure_ascii=False)
# save the visualization results to image files
# model.show_result(img, result, score_thr=0.1, font_scale=0.5, out_file='result.png')
