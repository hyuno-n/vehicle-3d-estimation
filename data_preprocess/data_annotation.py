import pandas as pd
import os
import re

def read_text_files(folder_path):
    file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    text_files = []

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as file:
            file_contents = file.read()
            text_files.append({"file_name": file_name, "contents": file_contents})

    return text_files

def add_center_dot(text_files, csv_file_path):
    df = pd.read_csv(csv_file_path)
    combined_data = df.iloc[:, 1:3].values.tolist()
    string_data = list(map(str, combined_data))

    for content, data in zip(text_files, string_data):
        content["contents"] += " " + " ".join(data.strip("[]").split(", "))

    return text_files

def add_car_spec(text_files, csv_file_path):
    df = pd.read_csv(csv_file_path)
    combined_data = df.iloc[:, 1:3].values.tolist()
    string_data = list(map(str, combined_data))

    for index, row in df.iterrows():
        name = row.iloc[0]
        matching_items = [item for item in text_files if re.search(name, item["file_name"])]
        for item in matching_items:
            item["contents"] += " " + " ".join(string_data[index].strip("[]").split(", "))

    return text_files

    
def save_text_files(text_files, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for data in text_files:
        file_name = data['file_name']
        contents = data['contents']
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, 'w') as file:
            file.write(contents)

        print(f"텍스트 파일 '{file_name}'이 생성되었습니다.")

if __name__ == "__main__":
    # select path
    csv_file_path1 = "./center_dot.csv"
    csv_file_path2 = "./car_spec.csv"
    folder_path = "labels"
    output_directory = 'test'
    
    # Load txt file and save as list
    text_files = read_text_files(folder_path)
    
    # Add Vhicle center dot
    text_files = add_center_dot(text_files, csv_file_path1)

    # Add vehicle length width
    text_files = add_car_spec(text_files, csv_file_path2)
    print(text_files)
    # Save as txt file
    save_text_files(text_files, output_directory)
