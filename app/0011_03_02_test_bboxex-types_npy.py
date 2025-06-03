import cv2
import pandas as pd
import numpy as np

def yolo_to_xyxy(yolo_coords, image_width, image_height):
    yolo_coords = yolo_coords.split()
    x, y, w, h = [float(coord) for coord in yolo_coords]
    x_center = x * image_width
    y_center = y * image_height
    half_w = w * image_width / 2
    half_h = h * image_height / 2

    xmin = int(x_center - half_w)
    ymin = int(y_center - half_h)
    xmax = int(x_center + half_w)
    ymax = int(y_center + half_h)

    return [xmin, ymin, xmax, ymax]

# Define column names for your data
column_names = ['input_image', 'bbox', 'heading', 'type','3d_center_x', '3d_center_y', 'real_width', 'real_length']

# Load data from a CSV file using pandas
csv_file_path = '/home/dblab/seong_space2/0002_move_3d/data/0001_csv/0001_01_test.csv'
data = pd.read_csv(csv_file_path, names=column_names, header=None)

image_folder = "/home/dblab/seong_space2/0002_move_3d/data/0001_image/"
# outputfolder = "/home/dblab/seong_space2/0000_car_bottom/bmb_bottom_lab/bmb_bottom/bmb_frame/0001_crop_all/"
outputfolder = "/home/dblab/seong_space2/0002_move_3d/data/1125_test_crop/"

bbox_array = np.empty((0, 4), dtype=int)
# image_array = np.empty((0, 224, 224), dtype=int)
type_array = np.empty((0, 1), dtype=int)

for index, row in data.iterrows():
    # print(index, row["bbox"][1:])
    input_bbox = row['bbox'][1:]  # Labels
    input_image = row['input_image']  # Labels
    image_path = image_folder + input_image
    # print(input_bbox[1:])
    # print(input_image)
    # print(type(input_image))
    # print(input_type)
    # print(type(input_type))

    # Example usage:
    yolo_coords = input_bbox  # YOLO format [x, y, w, h]
    image_width = 1920  # Replace with your image width
    image_height = 1080  # Replace with your image height

    xyxy_coords = yolo_to_xyxy(yolo_coords, image_width, image_height)
    # print(xyxy_coords)
    bbox_array = np.append(bbox_array, [xyxy_coords], axis=0)
    
    input_type = row['bbox'][:1]
    input_type = input_type.split()
    type_array = np.append(type_array, [input_type], axis=0)

    # print(xyxy_coords)  # This will give you [340, 270, 460, 330]
    

    # 이미지를 읽어옵니다.
    image = cv2.imread(image_path)
    # 크롭할 영역의 좌표 계산
    x1, y1, x2, y2 = xyxy_coords

    # 이미지를 크롭합니다.
    cropped_image = image[y1:y2, x1:x2]
    # cropped_image_resize = cv2.resize(cropped_image, (224, 224))
    # cropped_image_resize.split()
    # image_array = np.append(image_array, [cropped_image_resize], axis=0)
    # 크롭된 이미지를 파일로 저장합니다.
    output_path = f"{outputfolder}{str(index).zfill(4)}_{input_image}"
    cv2.imwrite(output_path, cropped_image)
npfolder = '/home/dblab/seong_space2/0002_move_3d/data/npy/1125/'
np.save(npfolder + 'test_bboxes.npy', bbox_array)
# np.save('path_to_train_images.npy', image_array)
type_array = type_array.astype(int)
np.save(npfolder + 'test_types.npy', type_array)


import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import glob
import numpy as np

image_paths = glob.glob(outputfolder + '*.jpg')
image_data = []
for path in image_paths:
    image = load_img(path)
    image = tf.image.resize(image, (224, 224))
    image_data.append(img_to_array(image))
image_data_np = np.array(image_data)
np.save(f'{npfolder}test_images.npy', image_data_np)