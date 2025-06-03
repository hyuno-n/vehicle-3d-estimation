import numpy as np
import tensorflow as tf
import cv2
import os
import pandas as pd

# input_bboxes = np.load('/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/traintest_npy/test_bboxes.npy')
# input_types = np.load('/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/traintest_npy/test_types.npy')

# # Assuming you have test data for 3D centers and dimensions as well
# input_3d_centers = np.load("/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/traintest_npy/test_3d_centers.npy")
# input_3d_dims = np.load("/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/traintest_npy/test_3d_dims.npy")
# input_3d_head = np.load("/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/traintest_npy/test_3d_head.npy")

# # Assuming you have test data for 3D centers and dimensions as well
# test_3d_centers = np.load("/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/train_output/testnpy/predicted_3d_centers_epoch1000_fclayer7.npy")
# test_3d_dims = np.load("/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/train_output/testnpy/predicted_3d_dims_epoch1000_fclayer7.npy")
# test_3d_head = np.load("/home/dblab/seong_space2/0000_car_bottom/3d_stop_obj/data/train_output/testnpy/predicted_3d_head_epoch1000_fclayer7.npy")

# print("input image bboxes tupes")
# # print(input_images.shape)
# print(input_bboxes.shape)
# print(input_types.shape)

# print("input 3d_cen 3_ddims")
# print(input_3d_centers.shape)
# print(input_3d_dims.shape)

# print("test 3d_cen 3_ddims")
# print(test_3d_centers.shape)
# print(test_3d_dims.shape)

outputfolder = "/home/dblab/seong_space2/0000_car_bottom/3d_move_obj/data/0014_output/"

# Define column names for your data
column_names = ['class','x','x2','input_image','x3','x4','x5','x6', 'bbox'] # 'bottom_x', 'bottom_y', '3d_width', '3d_length'
# truck,1241,200,T_S_0000_00006.jpg,1920,1080,1.74,5.17,1 0.643669 0.170274 0.053571 0.059163 1221 203 1.74 5.13
# Load data from a CSV file using pandas
csv_file_path = '/home/dblab/seong_space2/0000_car_bottom/3d_move_obj/data/merged.csv'
data = pd.read_csv(csv_file_path, names=column_names, header=None)
# data['bbox'] = data['bbox'].astype(float)
# Load your test data (adjust the paths accordingly)
image_folder = "/home/dblab/seong_space2/0000_car_bottom/3d_move_obj/data/ctb_frame/"

def yolo_to_xyxy(yolo_coords, image_width, image_height):
    yolo_coords = yolo_coords.split()
    # print(yolo_coords)
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

def draw_rotated_rectangle(image, center, size, angle, color, thickness):
    # Calculate the rotated rectangle's bounding box
    rect = ((center[0], center[1]), (size[0], size[1]), angle)
    box = cv2.boxPoints(rect)
    box = np.array(box).astype('int64')

    # Draw the rotated rectangle on the original image
    cv2.polylines(image, [box], isClosed=True, color=color, thickness=thickness)

import math

def calculate_angle(x1, y1, x2, y2):
    # 계산된 아크탄젠트 값을 라디안에서 각도로 변환
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)

    # 각도를 0~360 범위로 조정
    angle_deg = (angle_deg + 360) % 360

    return int(angle_deg)

# bbox_array = np.empty((0, 4), dtype=int)

# Loop through the images and save each one as a separate image file
for index, row in data.iterrows():
    # 이미지를 읽어옵니다.
    input_image = row['input_image']  # Labels
    image_path = image_folder + input_image
    image = cv2.imread(image_path)
    # print(row)
    input_bbox = row['bbox'][2:37]  # Labels
    print(f'{index}done')
    # break
    yolo_coords = input_bbox  # YOLO format [x, y, w, h]
    image_width = 1920  # Replace with your image width
    image_height = 1080  # Replace with your image height
    xyxy_coords = yolo_to_xyxy(yolo_coords, image_width, image_height)
    # print(xyxy_coords)
    # bbox_array = np.append(bbox_array, [xyxy_coords], axis=0)
    # Define the coordinates [xmin, ymin, xmax, ymax]
    # rect_coordinates = input_bboxes[index]

    # Extract coordinates
    xmin, ymin, xmax, ymax = xyxy_coords

    # Draw a rectangle on the image
    color = (0, 0, 255)  # Color in BGR format (Green in this example)
    thickness = 2  # Line thickness
    #bbox그리기
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

    # 3d 밑면 그리기 정보
    bbox_split = row['bbox'].split() # ['1', '0.643669', '0.170274', '0.053571', '0.059163', '1221', '203', '1.74', '5.13']
    # print(bbox_split)
    # break
    width = object_dimensions = bbox_split[7]
    length = object_dimensions = bbox_split[8]  # Labels
    # x, y = object_center = test_3d_centers[index]
    # x2, y2 = test_3d_head[index]

    # # Calculate the coordinates of the 3D object's bottom rectangle
    # xmin = int(x - width / 2)
    # ymin = int(y - length / 2)
    # xmax = int(x + width / 2)
    # ymax = int(y + length / 2)

    # # Draw the bottom rectangle representing the 3D object
    # bottom_color = (0, 255, 0)  # Color in BGR format (Green in this example)
    # thickness = 2  # Line thickness
    # angle = calculate_angle(x, y, x2, y2) + 90

    # # cv2.rectangle(image, (xmin, ymin), (xmax, ymax), bottom_color, thickness)
    # draw_rotated_rectangle(image, (x,y), (width,length), angle, bottom_color, thickness)


    # draw 3d center
    x = bbox_split[5]
    y = bbox_split[6]
    point = (int(x), int(y))
    # Define the color for the point (e.g., Red in BGR format)
    point_color = (0, 255, 0)

    # Draw the point on the image
    cv2.circle(image, point, radius=3, color=point_color, thickness=-1)

    # # draw 3d heading
    # point = (int(x2), int(y2))

    # # Define the color for the point (e.g., Red in BGR format)
    # point_color = (0, 255, 0)

    # # Draw the point on the image
    # cv2.circle(image, point, radius=3, color=point_color, thickness=-1)


    ## 어노테이션 정보 표시
    ## 어노테이션 사각형 그리기
    # # 3d 밑면 그리기 정보
    # width, length, height = object_dimensions = input_3d_dims[index]
    # width = int(width)
    # length = int(length)
    # height = int(height)
    # x3, y3 = input_3d_centers[index]
    # x3 = int(x3)
    # y3 = int(y3)
    # # print(type(x3))
    # x4, y4 = input_3d_head[index]
    # x4 = int(x4)
    # y4 = int(y4)
    # # Calculate the coordinates of the 3D object's bottom rectangle
    # xmin = int(x - width / 2)
    # ymin = int(y - length / 2)
    # xmax = int(x + width / 2)
    # ymax = int(y + length / 2)

    # # Draw the bottom rectangle representing the 3D object
    # bottom_color = (255, 0, 0)  # Color in BGR format (Green in this example)
    # thickness = 2  # Line thickness
    # angle2 = calculate_angle(x3, y3, x4, y4) + 90

    # # cv2.rectangle(image, (xmin, ymin), (xmax, ymax), bottom_color, thickness)
    # draw_rotated_rectangle(image, (x3,y3), (width,length), angle2, bottom_color, thickness)
    # #####################################################################################
    # # draw 3d center
    # point = (int(x3), int(y3))

    # # Define the color for the point (e.g., Red in BGR format)
    # point_color = (255, 0, 0)

    # # Draw the point on the image
    # cv2.circle(image, point, radius=3, color=point_color, thickness=-1)

    # # draw 3d heading
    # point = (int(x4), int(y4))

    # # Define the color for the point (e.g., Red in BGR format)
    # point_color = (255, 0, 0)

    # # Draw the point on the image
    # cv2.circle(image, point, radius=3, color=point_color, thickness=-1)

    # width   length 표시 putText()
    class_name = row['class']
    text_to_display = f'{class_name}-({width}M, {length}M)'
    text_position = (xmin, ymin-7)  # (x, y) 좌표
    cv2.putText(image, text_to_display, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


    # # 글꼴, 크기 및 두께 설정
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # font_scale = 1
    # font_thickness = 2
    # # 텍스트 크기 계산
    # text_size, baseline = cv2.getTextSize(text_to_display, font, font_scale, font_thickness)

    # # 배경 사각형 그리기
    # rectangle_padding = 5  # 사각형 주위의 여백
    # rectangle_size = (text_size[0] + 2 * rectangle_padding, text_size[1] + 2 * rectangle_padding)
    # rectangle_position = (text_position[0] - rectangle_padding, text_position[1] - text_size[1] - rectangle_padding)
    # rectangle_position = (text_position[0] - rectangle_padding, text_position[1] - text_size[1] - rectangle_padding)
    # cv2.rectangle(image, (rectangle_position[0], rectangle_position[1] + baseline + 5),
    #             (rectangle_position[0] + rectangle_size[0], rectangle_position[1] - rectangle_size[1] + baseline + 5),
    #             (0, 0, 255), cv2.FILLED)

    # # 글씨 표시
    # cv2.putText(image, text_to_display, text_position, font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)


    test_3d_image = image

    output_path = f"{outputfolder}{input_image}" # output_path = f"{outputfolder}{str(index).zfill(4)}_{input_image}"
    cv2.imwrite(output_path, test_3d_image)