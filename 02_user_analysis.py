import pandas as pd
from collections import defaultdict

# 데이터 파일 경로
file_path = "/DataCommon2/mjy/data/library_data_2022-2024.csv"
# 처리할 청크 크기 설정
chunk_size = 1000000  # 100만 행씩 처리

# 분석 결과를 저장할 딕셔너리 초기화
# defaultdict를 사용하면 키가 없을 때 자동으로 기본값을 생성해줍니다.
library_user_gender = defaultdict(lambda: defaultdict(int))
library_user_age = defaultdict(lambda: defaultdict(int))
library_user_location = defaultdict(lambda: defaultdict(int))

print("대용량 데이터 분석을 시작합니다. 청크 단위로 처리 중...")

# 에러 처리를 위한 try-except 블록
try:
    # chunksize 옵션을 사용하여 데이터를 청크 단위로 읽어옵니다.
    chunk_iterator = pd.read_csv(file_path, chunksize=chunk_size, low_memory=False)

    # 각 청크를 순회하며 분석 수행
    for i, chunk in enumerate(chunk_iterator):
        print(f"{i+1}번째 청크 처리 중...")

        # 분석할 컬럼의 결측치를 '알 수 없음'으로 채웁니다.
        chunk['성별'].fillna('알 수 없음', inplace=True)
        chunk['연령구간'].fillna('알 수 없음', inplace=True)
        chunk['시군구'].fillna('알 수 없음', inplace=True)

        # 1. 도서관별 성별 이용자 수 집계
        gender_counts = chunk.groupby(['도서관명', '성별']).size()
        for (library, gender), count in gender_counts.items():
            library_user_gender[library][gender] += count

        # 2. 도서관별 연령대별 이용자 수 집계
        age_counts = chunk.groupby(['도서관명', '연령구간']).size()
        for (library, age_group), count in age_counts.items():
            library_user_age[library][age_group] += count

        # 3. 도서관별 거주지(시군구)별 이용자 수 집계
        location_counts = chunk.groupby(['도서관명', '시군구']).size()
        for (library, location), count in location_counts.items():
            library_user_location[library][location] += count

    print("모든 청크 처리가 완료되었습니다.")

    # 집계된 데이터를 DataFrame으로 변환
    print("결과를 DataFrame으로 변환 중...")
    df_gender = pd.DataFrame(library_user_gender).T.fillna(0).astype(int)
    df_age = pd.DataFrame(library_user_age).T.fillna(0).astype(int)
    df_location = pd.DataFrame(library_user_location).T.fillna(0).astype(int)

    # 분석 결과를 CSV 파일로 저장
    print("분석 결과를 CSV 파일로 저장합니다...")
    output_dir = "Seoul/analysis_results"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    df_gender.to_csv(f"{output_dir}/library_user_gender.csv")
    df_age.to_csv(f"{output_dir}/library_user_age.csv")
    df_location.to_csv(f"{output_dir}/library_user_location.csv")

    print(f"분석 결과가 '{output_dir}' 폴더에 성공적으로 저장되었습니다.")
    print("\n저장된 파일 목록:")
    print(f"1. {output_dir}/library_user_gender.csv")
    print(f"2. {output_dir}/library_user_age.csv")
    print(f"3. {output_dir}/library_user_location.csv")


except FileNotFoundError:
    print(f"오류: 파일을 찾을 수 없습니다 - {file_path}")
except Exception as e:
    print(f"데이터 처리 중 오류가 발생했습니다: {e}") 