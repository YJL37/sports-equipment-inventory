from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# 업로드 폴더가 존재하지 않으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# CSV 파일 절대 경로 설정
csv_path = os.path.abspath("./test.csv")

# 데이터프레임과 딕셔너리를 전역 변수로 선언
df = None
name_year_dict = {}

# 초기 데이터프레임 로딩 및 처리
def load_data():
    global df, name_year_dict
    print(f"CSV 파일 경로: {csv_path}")  # 파일 경로 확인용 출력
    if os.path.isfile(csv_path):
        try:
            # CSV 파일 로드
            df = pd.read_csv(csv_path, index_col=None)
            df.reset_index(drop=True, inplace=True)

            # 'Name'과 'Class Year'을 키로 하여 중복 처리한 후, 가장 마지막 No 값만 남기기
            df_sorted = df.sort_values(by=['Name', 'Class Year', 'No'], ascending=[True, True, True])  # Name과 Class Year로 정렬 후 No 오름차순
            df_filtered = df_sorted.drop_duplicates(subset=['Name', 'Class Year'], keep='last')  # 마지막 값만 유지

            # 'Name + Class Year'을 키로 한 딕셔너리로 변환
            for _, row in df_filtered.iterrows():
                key = f"{row['Name']} {row['Class Year']}"  # Name과 Class Year을 결합하여 키 생성
                name_year_dict[key] = row.to_dict()  # 각 행을 딕셔너리로 변환하여 저장

            print("CSV 파일이 성공적으로 로드되었습니다.")
            #print(f"Name + Class Year을 키로 한 딕셔너리: {name_year_dict}")  # 딕셔너리 출력 확인
        except Exception as e:
            print(f"CSV 파일을 로드하는 중 오류 발생: {e}")
    else:
        print("CSV 파일을 찾을 수 없습니다.")  # 파일이 존재하지 않는 경우

def remove_unnecessary():
    for i in name_year_dict.keys():
        a = name_year_dict[i]
        del a['Grade']
        del a['Preferred Name']
        del a['No']
        del a['Remark']
        a['Borrowed'] = 0
        name_year_dict[i] = a
    
    #print(f"Name + Class Year을 키로 한 딕셔너리: {name_year_dict}")

def action_ball(serial_num, action):
    #print(serial_num, action)

    serial_num = str(serial_num)

    for i in name_year_dict.keys():
        if name_year_dict[i][' ID Serial Code'] == serial_num:
            print(i)
            if action == "borrowing":
                name_year_dict[i]['Borrowed'] += 1
                return 0
            elif action == "returning":
                name_year_dict[i]['Borrowed'] -= 1
                return 0

    print("There is no ID Serial with that number")

def track_no_return():
    no_return_students = []

    for i in name_year_dict.keys():
        if name_year_dict[i]['Borrowed'] > 0:
            no_return_students.append(i)
    
    print(no_return_students)

# 메인 페이지 렌더링
@app.route('/')
def index():
    global df
    if df is not None:
        # DataFrame을 HTML 테이블로 변환
        df_html = df.to_html(classes='table table-striped', index=False)
        return render_template('index.html', table=df_html)
    else:
        return "CSV 파일을 찾을 수 없습니다."

# 입력 처리 예시
@app.route('/process_input', methods=['POST'])
def process_input():
    global name_year_dict
    
    # 'Name + Class Year'을 기준으로 딕셔너리에서 찾기
    '''key = f"{a} {request.form.get('class_year')}"  # 입력값을 통해 Name + Class Year로 키 생성
    if key in name_year_dict:  # "key"가 name_year_dict에 존재하는지 확인
        return f"{key}의 정보가 존재합니다: {name_year_dict[key]}"
    else:
        return "해당 이름과 학년 정보를 찾을 수 없습니다."'''

if __name__ == '__main__':
    load_data()  # 데이터 로드
    remove_unnecessary()  #필요 없는 인덱스는 제거
    
    """for i in name_year_dict.keys():
        print(i, name_year_dict[i], end="\n")"""

    for i in range(3):
        a, b = map(str, input().split())
        action_ball(a, b)  #실제로 빌리기/반납하기
    
    track_no_return()  #반납 안한 사람
    #app.run(host='127.0.0.1', port=8000, debug=True)