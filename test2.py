import os

def get_file_names(directory):
    file_names = [os.path.splitext(file)[0] for file in os.listdir(directory)]
    return file_names

def find_missing_files(image_folder, txt_folder):
    image_files = get_file_names(image_folder)
    txt_files = get_file_names(txt_folder)

    missing_files = set(image_files) - set(txt_files)
    print(len(image_files))
    print(len(txt_files))
    return missing_files

if __name__ == "__main__":
    image_folder_path = "images"  # 이미지 폴더 경로로 변경
    txt_folder_path = "annotation"  # 텍스트 파일 폴더 경로로 변경

    missing_files = find_missing_files(image_folder_path, txt_folder_path)
    print(len(missing_files))

    if missing_files:
        print("텍스트 파일 폴더에 없는 이미지 파일 이름:")
        for file_name in missing_files:
            print(file_name)
    else:
        print("모든 이미지 파일이 텍스트 파일 폴더에 존재합니다.")