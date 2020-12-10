import json
import random

with open('pascal_train.json') as f:
    coco = json.load(f)
print(type(coco))
for key in coco:
    print(key)

train_set = {'annotations':[], 'images':[], 'categories':coco['categories']}
val_set = {'annotations':[], 'images':[], 'categories':coco['categories']}

imgs_bbox = {}
categories_num = {}
imgs_bbox_list = {}

#count number for each category
for bbox in coco['annotations']:
    if not bbox['image_id'] in imgs_bbox:
        imgs_bbox[bbox['image_id']] = []
        imgs_bbox_list[bbox['image_id']] = []
    imgs_bbox[bbox['image_id']].append(bbox['id'])
    imgs_bbox_list[bbox['image_id']].append(bbox['category_id'])
    if not bbox['category_id'] in categories_num:
        categories_num[bbox['category_id']] = 0
    categories_num[bbox['category_id']] += 1

print(categories_num)
categories_train_num = {key:categories_num[key] for key in categories_num}
categories_val_num = {key:0 for key in categories_num}
val_img_list = []

random.shuffle(coco['images'])
for img in coco['images']:
    for bbox in imgs_bbox_list[img['id']]:
        if categories_num[bbox]//10 > categories_val_num[bbox]:
            val_img_list.append(img['id'])
            val_set['images'].append(img)
            for bbox in imgs_bbox_list[img['id']]:
                categories_val_num[bbox] +=1
                categories_train_num[bbox] -= 1
            break
    else:
        train_set['images'].append(img)
print(categories_train_num)
print(categories_val_num)
print(len(train_set['images']))
print(len(val_set['images']))

for bbox in coco['annotations']:
    if bbox['image_id'] in val_img_list:
        val_set['annotations'].append(bbox)
    else:
        train_set['annotations'].append(bbox)

with open('train.json', 'w') as f:
    json.dump(train_set, f)
with open('val.json', 'w') as f:
    json.dump(val_set, f)
