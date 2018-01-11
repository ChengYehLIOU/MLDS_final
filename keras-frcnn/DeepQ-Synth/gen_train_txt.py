import os

folder = 's000'
img_folder = os.path.join(folder,'images')
with open(os.path.join(folder,'img_name_list.txt'),'w+') as f:
    for i in range(10000):
        #f.write(os.path.join(img_folder,('img_'+ str(i).zfill(8)+'.png')))
        f.write('img_'+ str(i).zfill(8)+'.png')
        f.write('\n')

