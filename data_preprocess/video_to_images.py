import cv2
import os

def extract_frames(video_path, output_folder):
    # VideoCapture 객체 생성
    cap = cv2.VideoCapture(video_path)

    # 총 프레임 수 확인
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 6프레임 단위로 이미지 저장
    frame_interval = 6
    frame_count = 0

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        if not ret:
            break

        # 6프레임마다 이미지 저장
        if frame_count % frame_interval == 0:
            output_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_{frame_count:05d}.jpg"
            output_path = os.path.join(output_folder, output_name)
            cv2.imwrite(output_path, frame)

        frame_count += 1

        # 모든 프레임을 읽으면 종료
        if frame_count == total_frames:
            break

    # VideoCapture 객체 해제
    cap.release()

    print(f"동영상 '{os.path.basename(video_path)}'에서 이미지 저장이 완료되었습니다.")

# 동영상 파일 경로 설정
video_folder = "./video"
output_folder = "./images"

# 저장할 폴더가 없다면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 동영상 파일 리스트 가져오기
video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4'))]

for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)
    extract_frames(video_path, output_folder)
