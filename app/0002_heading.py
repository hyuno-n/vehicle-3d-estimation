import cv2
import numpy as np

def calculate_angle(point1, point2):
    # 두 점 간의 변화 계산
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]

    # 아크탄젠트를 이용하여 각도 계산 (라디안)
    angle_rad = np.arctan2(delta_y, delta_x)

    # 라디안을 도(degree)로 변환
    angle_deg = np.degrees(angle_rad)

    # 각도가 음수일 경우 보정 (0~360 범위로)
    angle_deg = (angle_deg + 360) % 360

    return angle_deg

# 두 점의 좌표 입력
point1 = (100, 100)
point2 = (150, 150)

# 각도 계산
angle = calculate_angle(point1, point2)

# 결과 출력
print(f"두 점 간의 각도: {angle}도")