import streamlit as st
import cv2 as cv
import numpy as np
import pandas as pd
import os
import subprocess

from myapp.DeepSegmentor.options.test_options import TestOptions

path = 'myapp/DeepSegmentor/datasets/DeepCrack/'
test_path = 'test_img/'
command_inference = 'python3 test.py --dataroot myapp/DeepSegmentor/datasets/DeepCrack --name deepcrack --model deepcrack --dataset_mode deepcrack --batch_size 1 --num_classes 1 --norm batch --num_test 10000 --display_sides 1'


results_path = ['myapp/DeepSegmentor/results',
                'myapp/DeepSegmentor/results/deepcrack',
                'myapp/DeepSegmentor/results/deepcrack/test_latest',
                'myapp/DeepSegmentor/results/deepcrack/test_latest/images/']

max_pixels=500

def make_abs_path():
    os.path.abspath(os.getcwd())
    return True


def create_folders():
    # Where images are being stored
    if not os.path.isdir(path):
        os.mkdir(path+test_path)

    for tmp_path in results_path:
        # Where results inference appears
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)


def clean_temp():

    files_to_remove = ['myapp/DeepSegmentor/datasets/DeepCrack/test_img/myimg.png',
                       'results/deepcrack/test_latest/images/myimg_fused.png',
                       'results/deepcrack/test_latest/images/myimg_image.png',
                       'results/deepcrack/test_latest/images/myimg_label_viz.png',
                       'results/deepcrack/test_latest/images/myimg_side1.png',
                       'results/deepcrack/test_latest/images/myimg_side2.png',
                       'results/deepcrack/test_latest/images/myimg_side3.png',
                       'results/deepcrack/test_latest/images/myimg_side4.png',
                       'results/deepcrack/test_latest/images/myimg_side5.png',
                       ]
    try:
        for my_file in files_to_remove:
            if os.path.isfile(my_file):
                os.remove(my_file)
    except Exception as e:
        print(e)

if __name__ == '__main__':

    make_abs_path()
    clean_temp()
    create_folders()

    st.title("Crack detector")

    st.text("Autoras: Liz F., Milagros M.")


    uploaded_img = st.file_uploader("Elige una imagen compatible", type=[
                                    'png', 'jpg', 'bmp', 'jpeg'])
    if uploaded_img is not None:
        file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
        image = cv.imdecode(file_bytes, 1)
        cv.imwrite(path+test_path+'myimg.png', image)


        st.write("This is your uploaded image:")
        st.image(image, caption='La imagen que subiste',
                 channels="BGR", use_column_width=True)

        temp_img=cv.imread(path+test_path+'myimg.png')
        
        scale_percent = 80 # percent of original size
        width = int(temp_img.shape[1])
        height = int(temp_img.shape[0])
        
        while width>max_pixels or height>max_pixels:
            st.text('Reescalando: Weight-{} Height-{}'.format(width,height))

            width = int(width* scale_percent / 100)
            height = int(height * scale_percent / 100)
            dim = (width, height)
        
        # resize image
        resized = cv.resize(image, dim, interpolation = cv.INTER_AREA)


        st.image(resized, caption='La imagen escalada para poder ser procesada en la red neuronal sin saturar',
                 channels="BGR", use_column_width=True)

        cv.imwrite(path+test_path+'myimg.png', resized)

        st.subheader('Ejecutando red neuronal DeepCrack... ')

        result = os.popen(command_inference).read()
        # inference_args=command_inference.split(' ')
        # result = subprocess.run(inference_args,capture_output=True,text=True).stdout
        st.text("GPUS:"+result+"(if null -> cpu) \n")

        st.subheader('Inferencia terminada')
        st.subheader('Resultados')

        result_image = cv.imread('results/deepcrack/test_latest/images/myimg_fused.png')

        st.image(result_image, caption='La imagen que subiste',
                 channels="BGR", use_column_width=True)