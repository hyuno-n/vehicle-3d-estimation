import numpy as np
import tensorflow as tf

import cv2

from ultralytics import YOLO
import os

os.environ["CUDA_VISIBLE_DEVICES"]="0"
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

# 모델 로딩
yolo_model = YOLO('./model/best.pt')
prediction_model = tf.keras.models.load_model('./model/0001_01_train.keras', compile=False)

# 이미지 로딩 및 전처리
img = cv2.imread('test_image.jpg')

# 차량 감지
results = yolo_model.predict(img, device ='GPU')

# 감지된 차량 정보 처리
def process_results(results):
    for result in results:
        boxes = result.boxes
        input_type = boxes.cls  # 클래스 추출
        input_bbox = boxes.xyxy  # 경계 상자 좌표 추출

        # 3D 중심 및 치수 예측을 위한 입력 준비
        input_heading = np.array([0])[np.newaxis, :]
        input_type_np = input_type.cpu().numpy()[np.newaxis, :]  # 차원이 2가 되도록 변환
        input_bbox_np = input_bbox.cpu().numpy()

        # 3D 중심 및 치수 예측
        prediction = prediction_model.predict([input_heading, input_bbox_np, input_type_np])
        output_3d_center = prediction[0]
        output_3d_dims = prediction[1]

        # 이미지에 결과 시각화
        for i in range(len(input_bbox)):  # 각 차량에 대해 반복
            bbox = input_bbox[i]
            left_top = tuple(int(x) for x in bbox[:2])
            right_bottom = tuple(int(x) for x in bbox[2:])
            cv2.rectangle(img, left_top, right_bottom, (0, 255, 0), 2) 

            x = output_3d_center[0][0]
            y = output_3d_center[0][1]
            cv2.circle(img, (int(x), int(y)), 5, (255, 0, 0), -1)

            # 텍스트 위치 및 텍스트 백그라운드를 위한 준비
            text = f"W: {output_3d_dims[0][1]:.2f}, L: {output_3d_dims[0][0]:.2f}"
            text_pos = (int(bbox[0]), int(bbox[1] - 10))
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 1)
            text_bg_start = (text_pos[0], text_pos[1] - text_height)
            text_bg_end = (text_pos[0] + text_width, text_pos[1])

            # 텍스트 백그라운드
            cv2.rectangle(img, text_bg_start, text_bg_end, (255, 255, 255), -1)

            # 텍스트 표시
            cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    return img


# 이미지에 결과 시각화
img = process_results(results)

# 이미지 표시 및 종료 처리
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()