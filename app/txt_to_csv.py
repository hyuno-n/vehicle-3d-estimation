import os
import pandas as pd
import numpy as np

# 폴더 경로 설정
folder_path = './test'

# CSV 파일에 저장할 데이터를 담을 리스트 초기화
data_list = []

# 폴더 내의 모든 파일에 대해 반복
for file_name in os.listdir(folder_path):
    # 텍스트 파일인 경우에만 처리
    if file_name.endswith('.txt'):
        # 확장자를 제거한 파일 이름 추출
        file_name_without_extension = os.path.splitext(file_name)[0]
        file_path = os.path.join(folder_path, file_name)
        
        # 파일 읽기
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            # 한 줄씩 처리
            for line in lines:
                # 공백으로 분리하여 데이터 추출
                parts = line.split()
                
                # 데이터가 충분히 있는 경우에만 처리
                if len(parts) >= 9:
                    # 데이터 추출
                    object_type = int(parts[0])  # 객체 타입
                    x = float(parts[1])  # x 좌표
                    y = float(parts[2])  # y 좌표
                    w = float(parts[3])  # 너비
                    h = float(parts[4])  # 높이
                    center_x = int(parts[5])  # 중심점 x 좌표
                    center_y = int(parts[6])  # 중심점 y 좌표
                    width = float(parts[7])  # 실제 너비
                    length = float(parts[8])  # 실제 길이
                    heading = float(parts[9]) if len(parts) > 9 else 0 # 차량의 방향
                    
                    # 추출한 데이터를 리스트에 추가
                    data_list.append([file_name_without_extension, object_type, x, y, w, h, center_x, center_y, length, width, heading])


# 데이터를 DataFrame으로 변환
df = pd.DataFrame(data_list, columns=['File_Name', 'Object_Type', 'X', 'Y', 'Width', 'Height', 'Center_X', 'Center_Y', 'Real_Length', 'Real_Width', 'Heading'])

# CSV 파일로 저장
csv_file_path = 'output.csv'
df.to_csv(csv_file_path, index=False)

print("CSV 파일이 저장되었습니다.")
