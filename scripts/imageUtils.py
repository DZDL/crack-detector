import cv2 as cv
import pandas as pd
import numpy as np

def crack2object(image,connectivity=8):
    """
    Detect cracks, split and extracts data to a table with multiple characteristics
    
    Args:
        image (np.array): The image in numpy format with one channel (B/W).
        connectivity (int): [4,8,12] The method that connects cracks on the image.

    Returns:
        num_labels (): no info.
        labels (): no info.
        stats (): stats such as area, location, etc of each object connected.
        centroids (): centroid of each object connected. *2-dimensions
        
    Example:
        Converts a thresholded image from
        
        0 0 0 0 0 0 
        0 1 1 0 0 0
        0 0 0 0 1 1
        0 0 1 0 0 0 
        0 0 0 0 0 0

        to

        0 0 0 0 0 0
        0 1 1 0 0 0
        0 0 0 0 2 2
        0 0 3 0 0 0
        0 0 0 0 0 0
    
    """
    output = cv.connectedComponentsWithStats(image, 
                                            connectivity,
                                            cv.CV_32S)
    num_labels = output[0]   
    labels = output[1]
    stats = output[2]
    centroids = output[3] 
    
    return num_labels,labels,stats,centroids

def list_crack(df_labels_values_cod,image,labels):
    """
    Create a list of cracks filtered ready to be construct a new image
    
    Args:
        df_labels_value_cod (pandas.DataFrame) : dataframe that contains the statistics fields
        image (numpy.array) : array that contains the image in B/W
    
    Returns:
        list of images (numpy.array): list of numpy arrays
    
    """
    df_labels_values_cod=df_labels_values_cod['COD']
    values=df_labels_values_cod.to_numpy()    
    list_crack=[]
    h,w=image.shape[:2]

    for element in values:
        crack_img = np.zeros((h,w),np.uint8)
        pixel_x,pixel_y=np.where(labels==element)
        try:
            crack_img[pixel_x,pixel_y]=255
        except Exception as e:
            print(e)
        list_crack.append(crack_img) 
    print(f"Se ha actualizado lista_crack[]: {len(list_crack)}")
    return list_crack


def list_crack2image(lista_fisuras):
    """
    Create a image with list of cracks
    
    Args:
        lista_fisra (numpy.array) : array that contains each image appended.
    
    Returns:
        sum_temp (numpy.array): one image with all filtered cracks
    
    """
    for m in range(len(lista_fisuras)):
        if m==0:
            sum_temp=lista_fisuras[0]
        if m<(len(lista_fisuras)-1):
            temp=lista_fisuras[m+1]
            sum_temp=np.add(sum_temp,temp)
    try:
        return sum_temp
    except Exception as e:
        print(e)
        print("Error:No se pudo hacer plot, prueba reduciendo area mínima")

