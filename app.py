import os
import subprocess
import random
import streamlit as st
import cv2 as cv
import numpy as np
import pandas as pd

from scripts.imageUtils import list_crack, crack2object, list_crack2image

from myapp.DeepSegmentor.options.test_options import TestOptions

PATH = 'myapp/DeepSegmentor/datasets/DeepCrack/'
PATH_SPLIT = 'split/'
TEST_PATH = 'test_img/'

RESULTS_PATH = ['split',
                'myapp/DeepSegmentor/datasets/',
                'myapp/DeepSegmentor/datasets/DeepCrack',
                'myapp/DeepSegmentor/datasets/DeepCrack/test_img',
                'myapp/DeepSegmentor/results',
                'myapp/DeepSegmentor/results/deepcrack',
                'myapp/DeepSegmentor/results/deepcrack/test_latest',
                'myapp/DeepSegmentor/results/deepcrack/test_latest/images']

MAX_PIXELS = 500  # width or height
MIN_PIX_AREA_CRACK = 500  # MAX AREA IN IMAGE

COMMAND_INFERENCE = 'python3 test.py --dataroot myapp/DeepSegmentor/datasets/DeepCrack --name deepcrack --model deepcrack --dataset_mode deepcrack --batch_size 1 --num_classes 1 --norm batch --num_test 10000 --display_sides 1'
COMMAND_PNG2MP4 = 'ffmpeg -framerate 30 -i ' + \
    RESULTS_PATH[-1]+'/' + '%1d_fused.png -vcodec libx264 output.mp4'

METHODS = ['Resize', 'Split (+time)']


def make_abs_path():
    """
    Handle folder myapp as library
    """
    os.path.abspath(os.getcwd())
    return True


def clean_and_create_folders():
    """
    Remove all files in specific paths
    """
    print("----------------CLEAN FILES----------------")

    list_of_paths = RESULTS_PATH

    for path in list_of_paths:


        if not os.path.isdir(path):
            os.mkdir(path)
            print('Creating',path)

        for f in os.listdir(path):
            try:
                print(os.path.join(path, f))
                if ('jpg' or 'png' or 'jpeg' or 'bmp' or 'output') in f:
                    os.remove(os.path.join(path, f))
            except Exception as e:
                print(e)





def clean_other_files_from_results(path=RESULTS_PATH[-1]+'/'):
    """
    Removing all temporal files generated by DeepCrack
    Like _image _label_viz _side1..5
    """
    for f in os.listdir(path):
        if not 'fused' in f:
            print("Removing..."+path+f)
            os.remove(path+f)

    return True


def reduce_dims(width, height, scale_percent):
    """
    Reduce dimensions until fit in less of max_pixels
    """

    while width > MAX_PIXELS or height > MAX_PIXELS:
        st.text('Reescalando: Weight-{} Height-{}'.format(width, height))

        width = int(width * scale_percent / 100)
        height = int(height * scale_percent / 100)
        dim = (width, height)

    return dim


def resize_one_image(filename_path):
    """
    Resize one image with filepath
    """

    temp_img = cv.imread(filename_path)

    scale_percent = 80  # downscale percent
    width = int(temp_img.shape[1])
    height = int(temp_img.shape[0])

    # Resize image to reduce inference time and max virtual memory needed
    reduced_dim = reduce_dims(width, height, scale_percent)

    resized = cv.resize(temp_img, reduced_dim,
                        interpolation=cv.INTER_AREA)
    return resized, reduced_dim


def resize_all_images_from_path(path):
    """
    Resize all images given a path.
    """

    # Resize all images
    for f in os.listdir(path):
        st.text(str(path+f))
        resized, reduced_dim = resize_one_image(path+f)  # Resized
        cv.imwrite(path+f, resized)  # Saved

    return reduced_dim


def split_one_image_into_small_images(filename_path, filename):
    """
    Split images into small pieces to don't lose
    details in big pictures
    """
    image = cv.imread(filename_path)

    width = int(image.shape[1])
    height = int(image.shape[0])

    divisions_height = 0
    divisions_width = 0
    while(1):
        if (height/(divisions_height+1) > MAX_PIXELS*2):
            divisions_height += 1
        else:
            break

    while(1):
        if (width/(divisions_width+1) > MAX_PIXELS*2):
            divisions_width += 1
        else:
            break

    st.write(f'Dimensiones de la imagen: alto={height}, ancho={width}')
    st.write(f'Divisiones calculadas: alto={divisions_height}, \
        ancho={divisions_width}')

    slice_window_height = int(height/divisions_height)
    slice_window_width = int(width/divisions_width)
    x = 0
    y = 0

    for r in range(0, height, slice_window_height):
        y = 0
        for c in range(0, width, slice_window_width):
            r_c_name = PATH + TEST_PATH + \
                str(filename.split(".")[0])+f"_{x}_{y}." + \
                str(filename.split(".")[-1].lower())
            print(f'Creating {r_c_name}')
            temp_img = image[r:r+slice_window_height,
                             c:c+slice_window_width, :]

            if int(temp_img.shape[0]) > MAX_PIXELS and int(temp_img.shape[1]) > MAX_PIXELS:
                cv.imwrite(r_c_name, temp_img)
            y += 1
        x += 1
    return x, y


def split_all_images_into_small_images(path):
    """
    Crop all frames into small pieces to don't lose
    details in big pictures
    """
    pass


def merge_small_images_to_one_big_image(path_original, filename):

    img_load = cv.imread(path_original)
    height = img_load.shape[0]
    width = img_load.shape[1]
    channels = img_load.shape[2]

    list_files = os.listdir(RESULTS_PATH[-1])
    list_files.sort()
    print(list_files)

    # Check max rows splitted
    max_row, max_col = 0, 0
    for file in list_files:

        row = int(file.split('_')[-3])
        col = int(file.split('_')[-2])
        if max_row < row:
            max_row = row
        if max_col < col:
            max_col = col
    print(max_row, max_col)

    # Merge images into one big image with same shape as original
    img = np.zeros((height, width, 3), dtype=np.uint8)
    iterator = 0
    for r in range(max_row+1):
        for c in range(max_col+1):

            window_height = int(height/(max_row+1))
            window_width = int(width/(max_col+1))

            # print(window_height,window_width)
            # print([window_height*r,window_height*(r+1)])
            # print([window_width*c,window_width*(c+1)])

            load_img = cv.imread(RESULTS_PATH[-1]+'/'+list_files[iterator])

            # print(load_img.shape)

            img[window_height*r:window_height*(r+1),
                window_width*c:window_width*(c+1),
                :] = load_img
            iterator += 1
            # print(r,c)
    # Overlap one to another
    # Taken from https://theailearner.com/2019/03/26/image-overlays-using-bitwise-operations-opencv-python/

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img_gray, 200, 255, cv.THRESH_BINARY_INV)
    mask_inv = cv.bitwise_not(mask)

    cv.imwrite('split/mask.png', mask)
    cv.imwrite('split/mask_inv.png', mask_inv)

    rows, cols, channels = img.shape
    roi = img_load[0:rows, 0:cols]
    img_load_bg = cv.bitwise_and(roi, roi, mask=mask)

    # Taken from https://www.tutorialspoint.com/erosion-and-dilation-of-images-using-opencv-in-python
    kernel = np.ones((3, 3), np.uint8)  # set kernel as 3x3 matrix from numpy
    temp_img = mask_inv

    st.write('- Valores por defecto A, B y C:')

    code = '''
    A,B,C=5,5,15
    for a in range(5):
        temp_img = cv.erode(temp_img, kernel, iterations=5)
        temp_img = cv.dilate(temp_img, kernel, iterations=15)
    '''
    st.code(code, language='python')

    # value_A = st.slider('Selecciona el valor de A:',0, 20, 5)
    # value_B = st.slider('Selecciona el valor de B:',0, 20, 5)
    # value_C = st.slider('Selecciona el valor de C:',0, 20, 15)

    for a in range(5):
        temp_img = cv.erode(temp_img, kernel, iterations=5)
        temp_img = cv.dilate(temp_img, kernel, iterations=15)

    mask_inv = temp_img
    img[:, :, 0:1] = 0
    img_fg = cv.bitwise_and(img, img, mask=mask_inv)

    out_img = cv.add(img_load_bg, img_fg)
    img[0:rows, 0:cols] = out_img

    # Results
    st.subheader('Inferencia terminada: resultados')

    cv.imwrite(PATH_SPLIT+"/output_"+filename, img)
    st.image(img, caption='Superposición de grietas detectadas',
             channels="BGR", use_column_width=True)


def concat_vh(list_2d):

    # return final image
    return cv.vconcat([cv.hconcat(list_h) for list_h in list_2d])


def split_video_by_frame(video_path, input_drop_path):
    """
    This script will split video into frames with opencv
    """
    # Author: https://gist.github.com/keithweaver/70df4922fec74ea87405b83840b45d57

    cap = cv.VideoCapture(video_path)
    currentFrame = 0
    while(True):
        try:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Saves image of the current frame in jpg file
            name = input_drop_path + str(currentFrame) + '.jpg'
            print('Creating...' + name)

            cv.imwrite(name, frame)

            # To stop duplicate images
            currentFrame += 1
        except Exception as e:
            break
            print(e)

    # When everything done, release the capture
    try:
        cap.release()
        cv.destroyAllWindows()
    except Exception as e:
        print(e)

    return True


def filter_merged_image(image_path):

    imgOriginal = cv.imread(image_path)

    imgBW = cv.cvtColor(imgOriginal, cv.COLOR_BGR2GRAY)
    ret, imgThr = cv.threshold(imgBW,
                               150,
                               255,
                               cv.THRESH_BINARY)
    height = imgThr.shape[0]
    width = imgThr.shape[1]

    num_labels, labels, stats, centroids = crack2object(imgThr)

    df = pd.DataFrame(stats)
    df.columns = ['LEFT', 'TOP', 'WIDHT', 'HEIGHT', 'AREA']

    df = df.sort_values(by='AREA', ascending=False)

    # 0 area is the background
    # area need to be less than the quart of the image
    # area need have a min value
    df = df[(df['AREA'] < (height*width/4)) &
            (df['AREA'] > MIN_PIX_AREA_CRACK)]
    df['COD'] = df.index

    lista_fisuras = list_crack(df, imgThr, labels)

    all_cracks = list_crack2image(lista_fisuras)

    return all_cracks


def overlap_filtered_cracks(imgOrig_path, imgMask_path):

    # https://theailearner.com/2019/03/26/image-overlays-using-bitwise-operations-opencv-python/

    img1 = cv.imread(imgOrig_path)
    img2 = cv.imread(imgMask_path)

    rows, cols, channels = img2.shape
    roi = img1[0:rows, 0:cols]
    img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 200, 255, cv.THRESH_BINARY_INV)
    mask_inv = cv.bitwise_not(mask)
    img2[:, :, 0:1] = 0
    img1_bg = cv.bitwise_and(roi, roi, mask=mask)
    img2_fg = cv.bitwise_and(img2, img2, mask=mask_inv)
    out_img = cv.add(img1_bg, img2_fg)

    img1[0:rows, 0:cols] = out_img

    return img1


if __name__ == '__main__':

    make_abs_path()  # Handle folder as library
    clean_and_create_folders()  # Clean temporal files on each upload

    # General description

    st.title("Crack detector")
    st.text("Parte de tesis2, esta red neuronal permite detectar \nfisuras en diferentes materiales que automatizan \nprocesos de las inspecciones.")

    st.text("Red neuronal: DeepCrack - Liu, 2019")
    st.text("Aplicación web: Liz F., Milagros M.")
    st.text("Versión: 0.2.0")

    # Method to process video
    st.subheader("1. Method to process video")
    methods = st.radio(
        "",
        (METHODS[0], METHODS[1]))

    # Upload file
    st.subheader("2. Elige una imagen o video")
    uploaded_file = st.file_uploader("Elige una imagen compatible", type=[
        'png', 'jpg', 'bmp', 'jpeg', 'mp4'])

    if uploaded_file is not None:  # File > 0 bytes

        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type,
                        "FileSize": uploaded_file.size}
        st.write(file_details)

        #######################
        # VIDEO UPLOADED FILE
        #######################
        if file_details['FileType'] == 'video/mp4':

            with open('temporal.mp4', 'wb') as f:
                f.write(uploaded_file.getbuffer())

            split_video_by_frame('temporal.mp4', PATH+TEST_PATH)

            random_filename = random.choice(os.listdir(PATH+TEST_PATH))

            st.image(PATH+TEST_PATH+random_filename,
                     caption='Imagen al azar del video',
                     channels="BGR",
                     use_column_width=True)

            # Applying neural network: DeepCrack - Liu, 2019
            st.subheader('Ejecutando red neuronal DeepCrack... ')

            # Resize all images
            reduced_dim = resize_all_images_from_path(PATH+TEST_PATH)

            # INFERENCE
            result = os.popen(COMMAND_INFERENCE).read()

            # For CPU NN Inference we need to be sure that no gpu is being used by
            # the general script
            st.text(result)
            st.text("GPUS:"+"(if null -> cpu) \n")

            # Clean other files
            clean_other_files_from_results()  # default on result path

            # JPG -> MP4
            result = os.popen(COMMAND_PNG2MP4).read()
            st.text(result)

            # Display video
            st.subheader("Video procesado")
            st.video('output.mp4')

        #######################
        # IMAGE UPLOADED FILE
        #######################
        elif (file_details['FileType'] == 'image/png' or
              file_details['FileType'] == 'image/jpg' or
              file_details['FileType'] == 'image/jpeg' or
              file_details['FileType'] == 'image/bmp'):

            file_bytes = np.asarray(
                bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv.imdecode(file_bytes, 1)

            if methods == METHODS[0]:
                #######################################
                # IMAGE UPLOADED FILE - RESIZE METHOD
                #######################################

                cv.imwrite(PATH+TEST_PATH+uploaded_file.name, image)

                st.write("This is your uploaded image:")
                st.image(image, caption='La imagen que subiste',
                         channels="BGR", use_column_width=True)

                resized, reduced_dim = resize_one_image(
                    PATH+TEST_PATH+uploaded_file.name)

                # Display rezized image
                st.subheader("Redimensionando imagen...")
                st.image(resized, caption='La imagen escalada para poder ser procesada en la red neuronal sin saturar',
                         channels="BGR", use_column_width=True)
                cv.imwrite(PATH+TEST_PATH+uploaded_file.name, resized)

                # Applying neural network: DeepCrack - Liu, 2019
                st.subheader('Ejecutando red neuronal DeepCrack... ')

                # INFERENCE
                result = os.popen(COMMAND_INFERENCE).read()

                # For CPU NN Inference we need to be sure that no gpu is being used by
                # the general script
                st.text("GPUS:"+result+"(if null -> cpu) \n")

                # Results
                st.subheader('Inferencia terminada: resultados')

                # Get result image and display
                # st.text("Abriendo {}".format(RESULTS_PATH[-1]+uploaded_file.name[:-4]+"_fused.png"))
                result_image = cv.imread(
                    RESULTS_PATH[-1]+'/'+uploaded_file.name[:-4]+"_fused.png")
                st.image(result_image,
                         caption='La imagen que subiste',
                         channels="BGR",
                         use_column_width=True)

            elif methods == METHODS[1]:
                #######################################
                # IMAGE UPLOADED FILE - SPLIT METHOD
                #######################################

                cv.imwrite(PATH_SPLIT+uploaded_file.name, image)

                st.write("This is your uploaded image:")
                st.image(image,
                         caption='La imagen que subiste',
                         channels="BGR",
                         use_column_width=True)

                # resized, reduced_dim = resize_one_image(PATH+TEST_PATH+uploaded_file.name)
                x, y = split_one_image_into_small_images(
                    PATH_SPLIT+uploaded_file.name, uploaded_file.name)

                # Display rezized image
                st.subheader(
                    "Imagen dividida en pequeñas images para procesar...")
                # st.image(resized,
                #          caption='La imagen escalada para poder ser procesada en la red neuronal sin saturar',
                #          channels="BGR",
                #          use_column_width=True)
                # cv.imwrite(PATH+TEST_PATH+uploaded_file.name, resized)

                # Applying neural network: DeepCrack - Liu, 2019
                st.subheader('Ejecutando red neuronal DeepCrack... ')

                # INFERENCE
                result = os.popen(COMMAND_INFERENCE).read()

                # For CPU NN Inference we need to be sure that no gpu is being used by
                # the general script
                st.text("GPUS:"+result+"(if null -> cpu) \n")

                # Clean other files
                clean_other_files_from_results()

                # Merge small images
                image_out = merge_small_images_to_one_big_image(PATH_SPLIT+uploaded_file.name,
                                                                uploaded_file.name)

                # Small cracks filtered
                filtered_image = filter_merged_image('split/mask_inv.png')

                # Overlap two images
                image_filtered = overlap_filtered_cracks(PATH_SPLIT+uploaded_file.name,
                                                         PATH_SPLIT+'mask_inv.png')

                st.image(image_filtered,
                         caption='Imagen con cracks filtrados',
                         channels="BGR",
                         use_column_width=True)
