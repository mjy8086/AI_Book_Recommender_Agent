import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.font_manager as fm

# 폰트 경로를 직접 지정합니다.
# find / -name "NanumGothic.ttf" 2>/dev/null 명령어로 실제 경로를 확인하고,
# 만약 경로가 다르다면 이 부분을 수정해야 합니다.
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'

# 폰트 프로퍼티를 설정합니다.
try:
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except FileNotFoundError:
    print(f"경고: 폰트 파일 '{font_path}'를 찾을 수 없습니다. 시각화 결과물에서 한글이 깨질 수 있습니다.")
    pass

plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

# 분석 결과 파일이 저장된 디렉토리
input_dir = "Seoul/analysis_results"
# 시각화 결과물을 저장할 디렉토리
output_dir = "Seoul/visualization_outputs"
os.makedirs(output_dir, exist_ok=True)

# 분석 결과 파일 목록
files = {
    "gender": "library_user_gender.csv",
    "age": "library_user_age.csv",
    "location": "library_user_location.csv",
    "kdc": "library_kdc_main_category_counts.csv",
    "day": "library_day_counts.csv",
    "month": "library_month_counts.csv",
    "time": "library_time_counts.csv",
    "reserve": "library_reserve_counts.csv"
}

# 데이터 로드
data = {}
for key, file_name in files.items():
    try:
        data[key] = pd.read_csv(os.path.join(input_dir, file_name), index_col=0)
    except FileNotFoundError:
        print(f"오류: '{file_name}' 파일을 찾을 수 없습니다. 이전 단계가 정상적으로 완료되었는지 확인하세요.")
        continue

# 전체 대출 건수를 기준으로 상위 5개 도서관 선정
if 'age' in data:
    top5_libraries = data['age'].sum(axis=1).nlargest(5).index
    print(f"분석 대상 상위 5개 도서관: {', '.join(top5_libraries)}")
else:
    top5_libraries = []
    print("오류: 이용자 연령 데이터가 없어 상위 도서관을 선정할 수 없습니다.")

# 시각화 함수 정의
def plot_top5_pie_charts(df, column_name, title_prefix):
    """상위 5개 도서관에 대한 파이 차트를 그립니다."""
    if df.empty or top5_libraries.empty:
        return
        
    fig, axes = plt.subplots(1, 5, figsize=(25, 5))
    fig.suptitle(f'{title_prefix} - 상위 5개 도서관', fontsize=16)

    for i, lib in enumerate(top5_libraries):
        if lib in df.index:
            data_to_plot = df.loc[lib].nlargest(5) # 상위 5개 항목만 표시
            axes[i].pie(data_to_plot, labels=data_to_plot.index, autopct='%1.1f%%', startangle=90)
            axes[i].set_title(lib)
        else:
            axes[i].set_visible(False)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_dir, f"pie_chart_{column_name}_top5.png"))
    plt.close()
    print(f"'{title_prefix}' 파이 차트가 저장되었습니다.")


def plot_top5_bar_charts(df, column_name, title_prefix, is_numeric_index=False):
    """상위 5개 도서관에 대한 바 차트를 그립니다."""
    if df.empty or top5_libraries.empty:
        return
        
    fig, axes = plt.subplots(1, 5, figsize=(25, 5), sharey=True)
    fig.suptitle(f'{title_prefix} - 상위 5개 도서관', fontsize=16)

    for i, lib in enumerate(top5_libraries):
        if lib in df.index:
            data_to_plot = df.loc[lib].nlargest(10) # 상위 10개 항목만 표시
            if is_numeric_index:
                data_to_plot.index = data_to_plot.index.astype(str)
            
            sns.barplot(x=data_to_plot.index, y=data_to_plot.values, ax=axes[i])
            axes[i].set_title(lib)
            axes[i].tick_params(axis='x', rotation=45)
        else:
            axes[i].set_visible(False)
            
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_dir, f"bar_chart_{column_name}_top5.png"))
    plt.close()
    print(f"'{title_prefix}' 바 차트가 저장되었습니다.")


# 시각화 실행
if data:
    # 1. 성별 분포 (파이 차트)
    plot_top5_pie_charts(data.get('gender', pd.DataFrame()), 'gender', '도서관별 성별 이용자 분포')
    # 2. 연령대 분포 (파이 차트)
    plot_top5_pie_charts(data.get('age', pd.DataFrame()), 'age', '도서관별 연령대 이용자 분포')
    # 3. 거주지 분포 (바 차트)
    plot_top5_bar_charts(data.get('location', pd.DataFrame()), 'location', '도서관별 이용자 거주지(시군구) 분포')
    # 4. KDC 주류 분포 (바 차트)
    plot_top5_bar_charts(data.get('kdc', pd.DataFrame()), 'kdc', '도서관별 KDC 주류별 대출 분포')
    # 5. 요일별 대출 (바 차트)
    day_order = ['월', '화', '수', '목', '금', '토', '일', '알 수 없음']
    if 'day' in data:
        plot_top5_bar_charts(data['day'].reindex(columns=day_order), 'day', '도서관별 요일별 대출 분포')
    # 6. 월별 대출 (바 차트)
    if 'month' in data:
        month_df = data['month']
        # 월 컬럼을 숫자 순서대로 정렬하기 위해 컬럼명을 int로 변환 시도
        month_df.columns = pd.to_numeric(month_df.columns, errors='coerce').fillna(0).astype(int)
        month_df = month_df.reindex(columns=sorted(month_df.columns))
        plot_top5_bar_charts(month_df, 'month', '도서관별 월별 대출 분포', is_numeric_index=True)

    print("\n모든 시각화 자료 생성이 완료되었습니다.")
    print(f"결과물은 '{output_dir}' 폴더에서 확인하실 수 있습니다.")
else:
    print("데이터가 로드되지 않아 시각화를 진행할 수 없습니다.") 