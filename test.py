import os
from pathlib import Path

ctb_frame_folder = "ctb_frame"
images_folder = "images"

# ctb_frame 폴더의 이미지 파일 목록 가져오기
ctb_frame_images = [file.name for file in Path(ctb_frame_folder).glob("*") if file.is_file()]

# images 폴더에서 ctb_frame 폴더에 있는 이미지 파일 제외
for image in ctb_frame_images:
    image_path = os.path.join(images_folder, image)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"{image} 제외 완료.")

print("이미지 파일 제외가 완료되었습니다.")