import os
import math

# 폴더 경로 설정
folder_path = 'test'

# 폴더 내의 파일 목록 가져오기
file_list = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

file_name_x=''
# 각 파일에 대해 반복
for file_name in file_list:
    # 파일 경로 설정
    file_path = os.path.join(folder_path, file_name)

        # 파일 열기
    with open(file_path, 'r', encoding='utf-8') as file:
        # 파일 내용 읽어오기
        file_content = file.read()
        words = file_content.split()

        point1 = int(words[5])
        point2 = int(words[6])

        #전 파일과 같을 경우 헤딩 계산
        if file_name[:9] == file_name_x:    

            heading_angle = math.atan2(point2 - point2_x, point1 - point1_x)
            heading_angle_degrees = math.degrees(heading_angle)

            if heading_angle_degrees<0 :
                heading_angle_degrees=heading_angle_degrees+360

            heading_angle_degrees = round(heading_angle_degrees, 3)
            print(f'파일명: {file_name}, 헤딩 각도: {heading_angle_degrees} 도\n')
            
            # 파일에 헤딩 각도 추가
            with open(file_path, 'a', encoding='utf-8') as file_to_write:
                file_to_write.write(f' {heading_angle_degrees}')

    file_name_x = file_name[:9]
    point1_x = int(words[5])
    point2_x = int(words[6])
