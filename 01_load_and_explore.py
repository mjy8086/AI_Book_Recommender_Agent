import pandas as pd

# 데이터 파일 경로
file_path = "/DataCommon2/mjy/data/library_data_2022-2024.csv"

# 데이터의 처음 100개 행만 읽어와서 구조를 확인합니다.
try:
    df_sample = pd.read_csv(file_path, nrows=100)
    print("데이터 샘플 (처음 100개 행):")
    print(df_sample.head())
    print("\n데이터 정보:")
    df_sample.info()
    print("\n데이터 컬럼:")
    print(df_sample.columns)
except FileNotFoundError:
    print(f"오류: 파일을 찾을 수 없습니다 - {file_path}")
except Exception as e:
    print(f"데이터를 읽는 중 오류가 발생했습니다: {e}") 