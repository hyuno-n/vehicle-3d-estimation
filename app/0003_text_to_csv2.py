import pandas as pd
import glob
import os

# 데이터 로드
column_names = ['input_image', 'csv']
column_names2 = ['input_image', 'bbox', 'heading', 'type','3d_center_x', '3d_center_y', 'real_width', 'real_length']
csv_file_path = '/home/dblab/seong_space2/0002_move_3d/data/0001_csv/rect.csv'
df = pd.read_csv(csv_file_path, names=column_names, header=None)
aug_df = pd.DataFrame(columns=column_names2)
print(df)

for index, record in df.iterrows():
    input_image = record['input_image']
    input_csv = record['csv']  # Labels
    input_csv = input_csv.split()
    bbox = f'{input_csv[0]} {input_csv[1]} {input_csv[2]} {input_csv[3]} {input_csv[4]}'
    center_3d_x = f'{input_csv[5]}'
    center_3d_y = f'{input_csv[6]}'
    center_3d = [int(center_3d_x), int(center_3d_y)]
    real_width = f'{input_csv[7]}'
    real_length = f'{input_csv[8]}'
    heading = f'{input_csv[9]}'
    type = f'{input_csv[0]}'
    print(input_csv)

    new_row = {'input_image':input_image,'bbox':bbox, 'heading':int(round(float(heading))), 'type':type,'3d_center_x':center_3d_x,'3d_center_y':center_3d_y, 'real_width':float(real_width), 'real_length':float(real_length)}
#     new_row = {'class':record['class'], '3d_base_x':int(center_3dx), '3d_base_y':int(center_3dy), 'input_image':f'{aug_name}_'+str(record['input_image']), 
#                 'imgsize_x': 1920, 'imgsize_y': 1080, '3d_width':int(width_3d), '3d_length':int(length_3d), '3d_height':int(height_3d),
#                 'bbox':bbox, '3d_head_x':int(head_3dx), '3d_head_y':int(head_3dy)}

    aug_df = pd.concat([aug_df, pd.DataFrame([new_row])], ignore_index=True)

aug_df.to_csv(f'/home/dblab/seong_space2/0002_move_3d/data/0001_csv/rect2.csv', header=None ,index=False) # csv 증강된 저장
