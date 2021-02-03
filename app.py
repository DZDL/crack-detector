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


if __name__ == '__main__':

    make_abs_path()

    st.title("Crack detector")

    st.text("Autoras:..")

    uploaded_img = st.file_uploader("Elige una imagen compatible", type=[
                                    'png', 'jpg', 'bmp', 'jpeg'])
    if uploaded_img is not None:
        file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
        image = cv.imdecode(file_bytes, 1)

        create_folders()

        cv.imwrite(path+test_path+'myimg.png', image)

        st.write("This is your uploaded image:")
        st.image(image, caption='La imagen que subiste',
                 channels="BGR", use_column_width=True)

        st.text('Ejecutando red neuronal DeepCrack... ')

        result = os.popen(command_inference).read()
        # inference_args=command_inference.split(' ')
        # result = subprocess.run(inference_args,capture_output=True,text=True).stdout
        st.text(result)

        st.text('Inferencia terminada')

        # boxes, idxs = yolo.runYOLOBoundingBoxes_streamlit(image, yolopath, confidence, threshold)
        # st.write(pd.DataFrame.from_dict({'confidence' : [confidence],
        #                                 'threshold' : [threshold],
        #                                 'Encontrados (Boxes)': [len(boxes)],
        #                                 'Válidos (idxs)': [len(idxs)],}))
        # result_images = GrabCut.runGrabCut(image, boxes, idxs)

        # st.write("Here appears the rectangles that the algorithm recognize:")

        # img_mod=draw_rectangles(image,boxes,idxs)

        # st.image(img_mod, channels="BGR", use_column_width=True)

        # st.write("")
        # st.write("finish grabcut")
        # st.write(f"There are {len(result_images)} segmented fish image. Each listed as below:")
        # for i in range(len(result_images)):
        #     #cv.imwrite(f'grabcut{i}.jpg', result_images[i])
        #     st.image(result_images[i], channels="BGR", use_column_width=True)
