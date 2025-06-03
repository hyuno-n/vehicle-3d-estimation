import pandas as pd

# 엑셀 파일 경로 지정
input_excel_path = ".\center_dot.xlsx"
output_csv_path = "center_dot.csv"

# 엑셀 파일 불러오기
df = pd.read_excel(input_excel_path)

# 데이터를 CSV 파일로 저장
df.to_csv(output_csv_path, index=False)

print("데이터가 CSV 파일로 저장되었습니다.")
