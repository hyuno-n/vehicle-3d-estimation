import pandas as pd
import glob
import os

def merge_rect_files(base_dir, output_file):
    txt_files = glob.glob(os.path.join(base_dir, '**/*.txt'), recursive=True)
    txt_files.sort()
    df_list = []
    for f in txt_files:
        base_filename = os.path.splitext(os.path.basename(f))[0]
        new_filename = base_filename + '.jpg'
        print(f)
        temp_df = pd.read_csv(f, header=None)
        temp_df.insert(0, 'filename', new_filename)
        df_list.append(temp_df)
    
    df = pd.concat(df_list, ignore_index=True)
    df.to_csv(output_file, index=False, header=False)
    print(f"Merged TXT to CSV saved as {output_file}")

merge_rect_files('/home/dblab/seong_space2/0002_move_3d/data/0001_text/', '/home/dblab/seong_space2/0002_move_3d/data/0001_csv/rect.csv')

# 데이터 로드
# column_names = ['class', '3d_base_x', '3d_base_y', 'input_image', 'imgsize_x', 'imgsize_y', '3d_width', '3d_length', '3d_height', 'bbox','3d_head_x','3d_head_y']

# aug_df = pd.DataFrame(columns=column_names)

# for index, record in df.iterrows():

#     new_row = {'class':record['class'], '3d_base_x':int(center_3dx), '3d_base_y':int(center_3dy), 'input_image':f'{aug_name}_'+str(record['input_image']), 
#                 'imgsize_x': 1920, 'imgsize_y': 1080, '3d_width':int(width_3d), '3d_length':int(length_3d), '3d_height':int(height_3d),
#                 'bbox':bbox, '3d_head_x':int(head_3dx), '3d_head_y':int(head_3dy)}

#     aug_df = pd.concat([aug_df, pd.DataFrame([new_row])], ignore_index=True)

# aug_df.to_csv(f'/home/dblab/seong_space2/0001_stop_3d/data/0000_merge414/9999_augmentation_{aug_name}.csv', header=None ,index=False) # csv 증강된 저장
