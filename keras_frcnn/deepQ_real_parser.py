import os
import json
import cv2
import xml.etree.ElementTree as ET
import numpy as np


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


def get_data(input_path):
    all_imgs = []

    classes_count = {}

    class_mapping = {}

    visualise = False

    folder = os.path.join(input_path,'DeepQ-Vivepaper','data')
    data_paths = [os.path.join(folder,s) for s in ['air','book']]
    
#    folder1 = os.path.join(input_path,'DeepQ-Synth-Hand-01','data')
#    folder2 = os.path.join(input_path,'DeepQ-Synth-Hand-02','data')
#    data_paths = [os.path.join(folder1,s) for s in [ 's000','s001','s002','s003','s004']]
#    for s in ['s005','s006','s007','s008','s009']:
#        data_paths.append(os.path.join(folder2,s))


    print('Having ',len(data_paths),' folder')
    

    print('Parsing annotation files')

    for data_path in data_paths:

        print('data path is:',data_path)
        annot_path = os.path.join(data_path, 'label')
        imgs_path = os.path.join(data_path, 'img')
        
        
        #imgsets_path_trainval = os.path.join(data_path,'img_name_list.txt')
        
        #imgsets_path_test = os.path.join(data_path, 'ImageSets','Main','test.txt')

        trainval_files = []
        test_files = []
        try:
            for i in range(10000):
                s = 'img_'+str(i).zfill(5)+'.png'
                trainval_files.append(s)
            '''    
            with open(imgsets_path_trainval) as f:
                for line in f:
                    trainval_files.append(line.strip())
            '''
        except Exception as e:
            print(e)

        '''
        try:
            with open(imgsets_path_test) as f:
                for line in f:
                    test_files.append(line.strip() + '.jpg')
        except Exception as e:
            if data_path[-7:] == 'VOC2012':
                # this is expected, most pascal voc distibutions dont have the test.txt file
                pass
            else:
                print(e)
        '''
        annots = [os.path.join(annot_path, s) for s in os.listdir(annot_path)]
        for i in range(len(os.listdir(annot_path))):
            try:
                label = readJSON(os.path.join(annot_path,('label_'+str(i).zfill(5)+'.json')))       
                annotation_data = {'filepath': os.path.join(imgs_path, trainval_files[i]), 'width': 240,'height': 320, 'bboxes': []}
                annotation_data['imageset'] = 'trainval'
                for idx,lab in enumerate(label):
                    if idx == 0:
                        class_name = 'L'
                    else:
                        class_name = 'R'

                    if class_name not in classes_count:
                        classes_count[class_name] = 1
                    '''
                    else:
                        classes_count[class_name] += 1
                    '''
                    if class_name not in class_mapping:
                        class_mapping[class_name] = len(class_mapping)

                    x1 = int(lab[0])
                    y1 = int(lab[1])
                    x2 = int(lab[2])
                    y2 = int(lab[3])
                    difficulty = 0
                    if not [x1,y1,x2,y2] == [0,0,0,0]:
                        annotation_data['bboxes'].append({'class': class_name, 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'difficult': difficulty})
                        classes_count[class_name] +=1
                all_imgs.append(annotation_data)

                if visualise:
                    img = cv2.imread(annotation_data['filepath'])
                    for bbox in annotation_data['bboxes']:
                        cv2.rectangle(img, (bbox['x1'], bbox['y1']), (bbox[
                                      'x2'], bbox['y2']), (0, 0, 255))
                    cv2.imshow('img', img)
                    cv2.waitKey(0)

            except Exception as e:
                print(e)
                continue
    return all_imgs, classes_count, class_mapping
