import numpy as np
import cv2 as cv
import os

path='myapp/DeepSegmentor/results/deepcrack/test_latest/images/'

def concat_vh(list_2d):
    
      # return final image
    return cv.vconcat([cv.hconcat(list_h)  for list_h in list_2d])



images=[]
for f in os.listdir(path):
    print(path+f)
    
    images.append(path+f)

images.sort()


x=4
y=2
t=0
array=[[0]*(y+1)]*(x+1)
for m in range(x+1):
    for n in range(y+1):
        print(f'array [{m}],[{n}]')
        print(f'Reading {path+f}')
        array[m][n]=cv.imread(path+f.split('_')[-1])
        t+=1

array=np.array(array)

img_tile = concat_vh(array)

# cv.imwrite('ga.png',img_tile)