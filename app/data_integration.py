import pandas as pd
import glob
import os

def merge_point_files(base_dir, output_file):
    csv_files = glob.glob(os.path.join(base_dir, '*.csv'))
    df_list = []
    for file in csv_files:
        df = pd.read_csv(file, header=None)
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_csv(output_file, index=False, header=False)
    print(f"Merged CSV saved as {output_file}")

def merge_rect_files(base_dir, output_file):
    txt_files = glob.glob(os.path.join(base_dir, '**/*.txt'), recursive=True)
    df_list = []
    for f in txt_files:
        base_filename = os.path.splitext(os.path.basename(f))[0]
        new_filename = base_filename + '.jpeg'
        
        temp_df = pd.read_csv(f, header=None)
        temp_df.insert(0, 'filename', new_filename)
        df_list.append(temp_df)
    
    df = pd.concat(df_list, ignore_index=True)
    df.to_csv(output_file, index=False, header=False)
    print(f"Merged TXT to CSV saved as {output_file}")

def merge_datasets(point_file, rect_file, output_file):
    point_df = pd.read_csv(point_file, header=None)
    point_df['filename'] = point_df[3]

    rect_df = pd.read_csv(rect_file, header=None)
    rect_df.rename(columns={0: 'filename'}, inplace=True)

    merged_df = pd.merge(point_df, rect_df, on='filename', how='inner')

    merged_df.drop('filename', axis=1, inplace=True)

    merged_df.to_csv(output_file, index=False, header=False)
    print(f"Merged data saved as {output_file}")

merge_point_files('data/point/', 'data/point.csv')
merge_rect_files('data/rect/', 'data/rect.csv')
merge_datasets('data/point.csv', 'data/rect.csv', 'data/merged.csv')
