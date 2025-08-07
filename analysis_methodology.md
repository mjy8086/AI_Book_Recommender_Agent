# 서울시 공공도서관 대출 데이터 분석 방법론

## 1. 개요
본 문서는 서울시 공공도서관 대출 이력 데이터 분석 프로젝트의 전반적인 기술 과정과 방법론을 설명합니다. 데이터 로드부터 전처리, 분석, 시각화에 이르는 각 단계의 수행 방식과 사용된 도구를 상세히 기술하여 분석의 재현성과 확장성을 보장하는 것을 목적으로 합니다.

- **분석 환경:** Python, Pandas, Matplotlib, Seaborn
- **데이터 경로:** `/DataCommon2/mjy/data/library_data_2022-2024.csv`

## 2. 데이터 처리 및 분석 과정

### 2.1. 대용량 데이터 처리
- **문제점:** 분석 대상 데이터의 크기가 11GB에 달하여, 이를 메모리에 한 번에 로드하는 것은 비효율적이며 시스템에 큰 부하를 줄 수 있습니다.
- **해결책:** `pandas.read_csv` 함수의 `chunksize` 옵션을 사용하여 데이터를 100만 행 단위의 청크(chunk)로 나누어 처리했습니다. 각 청크를 순차적으로 읽어와 필요한 정보를 집계한 후, 모든 청크의 결과를 병합하는 방식을 사용하여 메모리 사용량을 최소화했습니다.

### 2.2. 데이터 탐색 및 전처리 (`01_load_and_explore.py`)
- 분석 초기 단계에서 `nrows=100` 옵션을 사용하여 데이터의 일부(100개 행)만 로드하여 전체적인 구조, 컬럼명, 데이터 타입을 신속하게 파악했습니다.
- 이 과정에서 `성별`, `연령구간`, `시군구` 등의 컬럼에서 결측치가 존재함을 확인하였고, `KDC분류기호`가 숫자형(float)으로 되어 있는 등 데이터 타입의 부적합성을 확인했습니다.

### 2.3. 이용자 특성 분석 (`02_user_analysis.py`)
- 청크 단위로 데이터를 순회하며, 각 도서관을 기준으로 이용자의 **성별, 연령구간, 거주지(시군구)**별 대출 건수를 집계했습니다.
- `collections.defaultdict`를 사용하여 동적으로 도서관별 통계 데이터를 누적하였고, `fillna()` 메소드로 분석 대상 컬럼의 결측치를 '알 수 없음'으로 대체하여 분석의 일관성을 확보했습니다.
- 모든 청크 처리가 완료된 후, 집계된 데이터를 Pandas DataFrame으로 변환하여 `Seoul/analysis_results` 폴더에 다음의 CSV 파일로 저장했습니다.
    - `library_user_gender.csv`
    - `library_user_age.csv`
    - `library_user_location.csv`

### 2.4. 도서 대출 특성 분석 (`03_loan_analysis.py`)
- 동일한 청크 처리 방식으로, 도서관별 **KDC 대분류, 대출 요일, 대출 월, 대출 시간대, 예약 대출 여부**에 따른 대출 건수를 집계했습니다.
- KDC 분류는 `pd.to_numeric`을 사용하여 숫자형으로 변환 후, 첫 번째 자리 숫자를 추출하여 대분류(주류) 정보를 생성했습니다.
- 분석 결과는 `Seoul/analysis_results` 폴더에 다음의 CSV 파일로 저장되었습니다.
    - `library_kdc_main_category_counts.csv`
    - `library_day_counts.csv`
    - `library_month_counts.csv`
    - `library_time_counts.csv`
    - `library_reserve_counts.csv`

### 2.5. 결과 시각화 (`04_visualize_results.py`)
- 앞서 생성된 8개의 분석 결과 CSV 파일을 로드하여 보고서용 시각화 자료를 생성했습니다.
- 전체 대출 건수(`age` 데이터의 총합)를 기준으로 상위 5개 도서관을 선정하여, 도서관별 비교가 용이하도록 했습니다.
- `matplotlib`과 `seaborn` 라이브러리를 사용하여, 성별/연령대별 분포는 **파이 차트**로, 거주지/KDC/요일/월별 분포는 **바 차트**로 시각화했습니다.
- **한글 폰트 처리:** 시스템에 `NanumGothic` 폰트가 설치되어 있지 않아, `try-except` 구문을 사용하여 폰트가 없는 경우에도 코드가 실행되도록 처리했습니다. (결과적으로 시각화 자료의 한글이 깨졌으나, 코드 자체의 실행은 보장됨)
- 모든 시각화 결과물은 `Seoul/visualization_outputs` 폴더에 PNG 이미지 파일로 저장되었습니다.

## 3. 생성된 파일 목록

- **분석 코드:**
    - `Seoul/01_load_and_explore.py`
    - `Seoul/02_user_analysis.py`
    - `Seoul/03_loan_analysis.py`
    - `Seoul/04_visualize_results.py`
- **분석 결과 데이터 (CSV):** `Seoul/analysis_results/` 폴더 내 8개 파일
- **시각화 자료 (PNG):** `Seoul/visualization_outputs/` 폴더 내 6개 파일
- **최종 보고서:**
    - `Seoul/analysis_report.md`
    - `Seoul/analysis_methodology.md` 