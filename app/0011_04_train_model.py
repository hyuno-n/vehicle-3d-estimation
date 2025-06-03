import pandas as pd
import numpy as np
import cv2
import os

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, GlobalAveragePooling2D, concatenate
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# ######################################################
# 모델 생성
# ######################################################
# 모델 입력 설정

num_classes = 1  # 객체 class 번호 (0:car or 1:bus or 2:truck)
input_bbox = Input(shape=(4,), name='input_bbox')  # 바운딩 박스 좌표 (x_min, y_min, x_max, y_max)
input_type = Input(shape=(num_classes,), name='input_type')  # 객체 타입에 대한 원-핫 인코딩 벡터
input_heading = Input(shape=(1,), name='input_heading') # 이전 프레임과 비교한 차량의 이동 방향

# Concatenate inputs
combined_features = concatenate([input_bbox, input_type, input_heading])

# Fully connected layers 추가. 레이어 수는 변경 가능
fc_layer = Dense(4096, activation='relu')(combined_features)

# Add additional hidden layers with more nodes
fc_layer = Dense(2048, activation='relu')(fc_layer)
fc_layer = Dense(1024, activation='relu')(fc_layer)
fc_layer = Dense(512, activation='relu')(fc_layer)
fc_layer = Dense(256, activation='relu')(fc_layer)
fc_layer = Dense(128, activation='relu')(fc_layer)
fc_layer = Dense(64, activation='relu')(fc_layer)
fc_layer = Dense(32, activation='relu')(fc_layer)


# Output Layer
output_3d_center = Dense(2, activation='linear', name='output_3d_center')(fc_layer)  # 중심의 x, y
output_3d_dims = Dense(2, activation='linear', name='output_3d_dims')(fc_layer)  # 넓이, 길이 

# 모델 생성
model = Model(inputs=[input_heading, input_bbox, input_type], # input_depth_map, input_image
            outputs=[output_3d_center, output_3d_dims]) # output_3d_head

# 모델 컴파일
optimizer = Adam(learning_rate=1e-4)
model.compile(optimizer=optimizer,
            loss='mse', metrics=['mae']) # , 'output_3d_head': 'mae'

# 모델 요약 출력
model.summary()

#######################################################

#######################################################
# 학습
#######################################################

def yolo_to_absolute(yolo_coords, image_width, image_height): # yolo형식의 데이터 변환
    x_center, y_center, bbox_width, bbox_height = yolo_coords
    abs_x = int(x_center * image_width)
    abs_y = int(y_center * image_height)
    abs_width = int(bbox_width * image_width)
    abs_height = int(bbox_height * image_height)
    # Calculate absolute coordinates (top-left corner)
    x1 = abs_x - abs_width // 2
    y1 = abs_y - abs_height // 2
    # Calculate absolute coordinates (bottom-right corner)
    x2 = abs_x + abs_width // 2
    y2 = abs_y + abs_height // 2
    return x1, y1, x2, y2

# Load data from a CSV file using pandas
csv_file_path = './output.csv'
column_names = ['File_Name', 'Object_Type', 'X', 'Y', 'Width', 'Height', 'Center_X', 'Center_Y', 'Real_Length', 'Real_Width', 'Heading']
data = pd.read_csv(csv_file_path, names=column_names, header=None)
data = data.iloc[1:]

print(data)
train_bboxes = data[['X','Y', 'Width', 'Height']].astype(float)
train_types = data[['Object_Type']].astype(int)
train_3d_centers = data[['Center_X', 'Center_Y']].astype(float)
train_3d_dims = data[['Real_Length', 'Real_Width']].astype(float)
train_3d_head = data[['Heading']].astype(float)
for index, row in train_bboxes.iterrows():
    image_width = 1920  # 이미지 너비
    image_height = 1080  # 이미지 높이
    yolo_coords = (row['X'], row['Y'], row['Width'], row['Height'])
    x1, y1, x2, y2 = yolo_to_absolute(yolo_coords, image_width, image_height)
    # 변환된 좌표를 데이터프레임에 업데이트
    train_bboxes.at[index, 'X'] = x1
    train_bboxes.at[index, 'Y'] = y1
    train_bboxes.at[index, 'Width'] = x2
    train_bboxes.at[index, 'Height'] = y2
print(train_bboxes)

batch_size = 32
epochs = 100
# Early stopping 설정
early_stopping = EarlyStopping(monitor='mse', patience=10, restore_best_weights=True)
history = model.fit(
    [train_3d_head, train_bboxes, train_types], # , train_depth_maps
    [train_3d_centers, train_3d_dims], # , train_3d_head
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2,
    callbacks=[early_stopping]
)
loss_history = history.history

model.save("./model/0001_01_train.keras")
print("model saved")


import pickle

# Save the training history using pickle
with open('./history/0001_01_train.pkl', 'wb') as file:
    pickle.dump(history.history, file)
print("history saved")
# import matplotlib.pyplot as plt