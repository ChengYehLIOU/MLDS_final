import numpy as np
import json
import os
import skimage
import skimage.io
import scipy.misc
import skimage.transform
from tqdm import tqdm


################################
#     label description        
#     shape = (2,4)
#     label[0,:] = Left Hand Bounding Box
#     label[1,:] = Right Hand Bounding Box
#     if no bounding box for this kind of hand
#     label is [0,0,0,0]     
#     otherwise[x0,y0,x1,y1]
#      ----------------------------->
#      |
#      |     .(x0,y0)____ 
#      |     |           |
#      |     |           |
#      |     |___________.(x1,y1)
#      |
#      |
#      |
#      v
#
#
################################     
def readJSON(filename):
    label = np.zeros((2,4))
    with open(filename) as f:
        lb = json.load(f)
        bb = lb['bbox']
        leftBox = bb.get('L')
        if leftBox is not None:
            label[0,:] = leftBox
        else:
            label[0,:] = [0,0,0,0]
        rightBox = bb.get('R')
        if rightBox is not None:
            label[1,:] = rightBox
        else:
            label[1,:] = [0,0,0,0]
    return label

dataFolder = 'data'
synth1 = os.path.join(os.path.join(dataFolder,'DeepQ-Synth-Hand-01'),'data')
synth2 = os.path.join(os.path.join(dataFolder,'DeepQ-Synth-Hand-02'),'data')

images_list = []
masks_list =[]
labels_list = []
for dataset in [synth1,synth2]:
    for subfold in os.listdir(dataset):
        
        path = os.path.join(dataset,subfold)
        print('reading: ',path)
        img_folder = os.path.join(path,'img')
        label_folder = os.path.join(path,'label')
        mask_folder = os.path.join(path,'mask')
        # img folder
        for i in tqdm(range(len(os.listdir(img_folder)))):
            filename = 'img_'+str(i).zfill(8)+'.png'
            images_list.append(skimage.io.imread(os.path.join(img_folder,filename)))
        # mask folder
        for i in tqdm(range(len(os.listdir(mask_folder)))):
            filename = 'mask_'+str(i).zfill(8)+'.png'
            masks_list.append(skimage.io.imread(os.path.join(mask_folder,filename)))
        # label folder
        for i in tqdm(range(len(os.listdir(label_folder)))):
            filename = 'label_'+str(i).zfill(8)+'.json'
            labels_list.append(readJSON(os.path.join(label_folder,filename)))
    
        # break here to use only s000's data
        break

    # break here to use only Synth-Hand-01's data
    break

images = np.array(images_list,dtype=np.uint8)
masks  = np.array(masks_list,dtype=np.uint8)
labels  = np.array(labels_list,dtype=np.uint8)

# if you want to store to npy file, make store2npy = True
store2npy = False
if store2npy:
    with open('images.npy','wb') as f:
        np.save(f,images)
    with open('masks.npy','wb') as f:
        np.save(f,masks)
    with open('labels.npy','wb') as f:
        np.save(f,labels)
