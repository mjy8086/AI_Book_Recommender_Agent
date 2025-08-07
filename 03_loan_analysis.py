import pandas as pd
from collections import defaultdict
import os

# 데이터 파일 경로
file_path = "/DataCommon2/mjy/data/library_data_2022-2024.csv"
# 처리할 청크 크기 설정
chunk_size = 1000000  # 100만 행씩 처리

# 분석 결과를 저장할 딕셔너리 초기화
library_kdc_counts = defaultdict(lambda: defaultdict(int))
library_day_counts = defaultdict(lambda: defaultdict(int))
library_month_counts = defaultdict(lambda: defaultdict(int))
library_time_counts = defaultdict(lambda: defaultdict(int))
library_reserve_counts = defaultdict(lambda: defaultdict(int))

print("도서 대출 특성 분석을 시작합니다. 청크 단위로 처리 중...")

try:
    chunk_iterator = pd.read_csv(file_path, chunksize=chunk_size, low_memory=False)

    for i, chunk in enumerate(chunk_iterator):
        print(f"{i+1}번째 청크 처리 중...")

        # KDC 분류기호의 주류(첫째 자리)를 추출합니다.
        # 결측치나 숫자가 아닌 값을 처리하기 위해 오류를 무시('coerce')하고, 정수형으로 변환 후 문자열로 변환합니다.
        chunk['KDC_main_category'] = pd.to_numeric(chunk['KDC분류기호'], errors='coerce').fillna(0).astype(int).astype(str).str[0]

        # 결측치 처리
        chunk['대출요일'].fillna('알 수 없음', inplace=True)
        chunk['대출월'].fillna('알 수 없음', inplace=True)
        chunk['대출시간대'].fillna('알 수 없음', inplace=True)
        chunk['예약대출'].fillna('N', inplace=True) # 예약대출 여부는 Y/N으로 가정, 결측치는 N으로 처리

        # 1. 도서관별 KDC 주류별 대출 건수
        kdc_counts = chunk.groupby(['도서관명', 'KDC_main_category']).size()
        for (library, kdc), count in kdc_counts.items():
            library_kdc_counts[library][kdc] += count

        # 2. 도서관별 요일별 대출 건수
        day_counts = chunk.groupby(['도서관명', '대출요일']).size()
        for (library, day), count in day_counts.items():
            library_day_counts[library][day] += count
            
        # 3. 도서관별 월별 대출 건수
        month_counts = chunk.groupby(['도서관명', '대출월']).size()
        for (library, month), count in month_counts.items():
            library_month_counts[library][month] += count

        # 4. 도서관별 시간대별 대출 건수
        time_counts = chunk.groupby(['도서관명', '대출시간대']).size()
        for (library, time), count in time_counts.items():
            library_time_counts[library][time] += count

        # 5. 도서관별 예약대출 건수
        reserve_counts = chunk.groupby(['도서관명', '예약대출']).size()
        for (library, reserve), count in reserve_counts.items():
            library_reserve_counts[library][reserve] += count

    print("모든 청크 처리가 완료되었습니다.")

    # DataFrame으로 변환
    print("결과를 DataFrame으로 변환 중...")
    df_kdc = pd.DataFrame(library_kdc_counts).T.fillna(0).astype(int)
    df_day = pd.DataFrame(library_day_counts).T.fillna(0).astype(int)
    df_month = pd.DataFrame(library_month_counts).T.fillna(0).astype(int)
    df_time = pd.DataFrame(library_time_counts).T.fillna(0).astype(int)
    df_reserve = pd.DataFrame(library_reserve_counts).T.fillna(0).astype(int)

    # 분석 결과 저장
    output_dir = "Seoul/analysis_results"
    os.makedirs(output_dir, exist_ok=True)
    
    print("분석 결과를 CSV 파일로 저장합니다...")
    df_kdc.to_csv(f"{output_dir}/library_kdc_main_category_counts.csv")
    df_day.to_csv(f"{output_dir}/library_day_counts.csv")
    df_month.to_csv(f"{output_dir}/library_month_counts.csv")
    df_time.to_csv(f"{output_dir}/library_time_counts.csv")
    df_reserve.to_csv(f"{output_dir}/library_reserve_counts.csv")

    print(f"분석 결과가 '{output_dir}' 폴더에 성공적으로 저장되었습니다.")
    print("\n저장된 파일 목록:")
    print(f"1. {output_dir}/library_kdc_main_category_counts.csv")
    print(f"2. {output_dir}/library_day_counts.csv")
    print(f"3. {output_dir}/library_month_counts.csv")
    print(f"4. {output_dir}/library_time_counts.csv")
    print(f"5. {output_dir}/library_reserve_counts.csv")

except FileNotFoundError:
    print(f"오류: 파일을 찾을 수 없습니다 - {file_path}")
except Exception as e:
    print(f"데이터 처리 중 오류가 발생했습니다: {e}") 