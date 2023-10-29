import math
import datetime
# datetime : 파이썬에 내장되어 있는 함수
from flask_pymongo import PyMongo
# 만약 flask_pymongo 인식을 못하면 밑에 3.11.1.적힌 걸 눌러서 한번 클릭해주기
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/local"
# 이전강의에서 사용했던 주소, 추가된 부분(local)- database였음
mongo = PyMongo(app)
# mongo라는 변수를 이용해서 mongodb사용 가능

@app.route('/write', methods=["POST"])
def write():
    name = request.form.get('name')
    content = request.form.get('content')

    mongo.db['wedding'].insert_one({
        "name": name,
        "content": content
    })

    return redirect('/')

@app.route('/')
def index():
    now = datetime.datetime.now()
    # now를 통해서 현재시간을 가져옴
    wedding = datetime.datetime(2023, 6, 18, 0, 0, 0)
    diff = (wedding - now).days

    page = int(request.args.get('page', 1))
    # 없을 떈 기본페이지 보여줌. 그래서 page 뒤에 1
    # 페이지네이션을 위해 쿼리로 페이비 번호을 받을 경우 전달 받은 해당 값을 문자열이라서 숫자형으로 변환해야 함
    limit = 3
    skip = (page - 1) * limit
    # page가 1이면 skip은 ()
    # page가 2이면 skip은 (3)
    # page가 3이면 skip은 (6) 

    count = mongo.db['wedding'].count_documents({})
    # 이안에 몇개가 있는지 갯수를 가지고 오는 코드
    # 몇 개 인지 알면 html에서 몇 개의 page를 보여줘야 되는지 계산 할 수도 있음
    # documents에 모든 문서에 대해서 개수를 세려면 빈 딕셔너리 변수를 넣어주면 됨
    max_page = math.ceil(count / limit)

    pages = range(1, max_page + 1)
    
    guestbooks = mongo.db['wedding'].find().limit(3).skip(skip)
    # limit이란 개수를 제한하는 함수
    # 페이지네이션을 위해서는 limit과 skip을 활용해야 함
    # skip이란 몇개를 건너뛸 지

    return render_template('index.html', diff=diff, guestbooks=guestbooks, pages=pages)
    # def(define) 함수를 만들 때 사용.
    # javascript 땐 function을 사용함
    # 조건문, 반복문 일때 들여쓰기, : 사용

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
    # 0.0.0.0 은 모든 주소를 접속할 수 있다는 것을 뜻한다.
    # port 80은 웹사이트 이용하는데 기본적으로 사용함. 그래야 포트번호를 따로 안적어도 문제가 없음
