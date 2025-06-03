import pandas as pd
import numpy as np

# Define column names for your data
column_names = ['input_image', 'bbox', 'heading', 'type','3d_center_x', '3d_center_y', 'real_width', 'real_length']

# Load data from a CSV file using pandas
csv_file_path = '/home/dblab/seong_space2/0002_move_3d/data/0001_csv/0001_01_train.csv'
data = pd.read_csv(csv_file_path, names=column_names, header=None)

train_3d_centers_array = []
train_3d_dims_array = []
train_3d_head_array = []
# np_array 정보 추출
for index, row in data.iterrows():
    bottom_x = row['3d_center_x'] # Labels
    bottom_y = row['3d_center_y']  # Labels
    bottom_cemter = [bottom_x, bottom_y]
    train_3d_centers_array.append(bottom_cemter)

    width = row['real_width'] # Labels
    length = row['real_length'] # Labels
    bottom_size = [width, length]
    train_3d_dims_array.append(bottom_size)

    heading = row['heading']
    train_3d_head_array.append(heading)
    

print(train_3d_centers_array)

# np_array 정보 .npy 파일로 저장
npfolder = '/home/dblab/seong_space2/0002_move_3d/data/npy/1125/'
np.save(npfolder + 'train_3d_centers.npy', train_3d_centers_array)
np.save(npfolder + 'train_3d_dims.npy', train_3d_dims_array)
np.save(npfolder + 'train_3d_head.npy', train_3d_head_array)