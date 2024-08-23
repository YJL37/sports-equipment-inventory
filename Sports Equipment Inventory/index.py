import pandas as pd
import os

from flask import Flask, render_template
app = Flask(__name__)

"""@app.route('/')
def hello_world():
    return 'Hello World!'"""

# reading the data in the csv file
df = pd.read_csv('test.csv')
df.to_csv('test.csv', index=None)
  
# route to html page - "table"
# 해당 라우팅 경로로 요청이 왔을 때 실행할 함수를 바로 밑에 작성함
@app.route('/')
def table():
    # converting csv to html
    data = pd.read_csv('test.csv')
    return render_template('index.html', tables=[data.to_html()], titles=[''])

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

