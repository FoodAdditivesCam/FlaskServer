# -*- coding: utf-8 -*- #cp949
# 서버가 돌아가는 메인 페이지
import json

from konlpy.tag import Kkma
from newspaper import Article

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from Symspell_py import symspell
from GetURL_py import getURL
from crawling_py import getResult

from flask import Flask, request, jsonify
from Symspell import Symspell, sym_spell
from flask import request, jsonify
import json
import os
from models import data_update, db, get_db_data


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#api = Api(app)

# # 분리한 파일을 api에 등록
# api.add_namespace(Symspell, '/symspell')
# api.add_namespace(Crawling, '/crawling')


dictionary_path = 'dictionary.txt'
sym_spell.load_dictionary(dictionary_path, 0, 1, separator="$", encoding='utf-8')

# DB
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite') # D:\2021\GradProject\FlaskServer\db.sqlite
# SQLAlchemy 설정
# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'd42dc573f4bf3f3f77639b715d6266f1'
db.init_app(app)
db.app = app
db.create_all()

# data update
#data_update()


@app.route('/result', methods=['POST'])
def post():
    print(request.is_json)
    jsonObject = request.get_json()
    input_terms = []
    result = []

    # 임시 질병 가중치 딕셔너리(추후 DB로 변경 필요)
    weight = {"0":"단맛", "2":"혈당조절", "4":"혈당조절", "6":"소화촉진", "7":"혈당조절 단맛", "9":"소화촉진", "11":"골다공증 골격"}

    # 원재료 이름
    jsonArray = jsonObject.get("input")
    jsonArray = jsonArray.replace('[', '').replace(']', '').split(',')

    # 선택한 질병의 인덱스
    jsonArray2 = jsonObject.get("weight")
    jsonArray2 = jsonArray2.replace('[', '').replace(']', '').split(',')
    weightList = []
    for i in jsonArray2 :
        if i in weight.keys():
            li = weight[i].split(" ")
            weightList += li

    # 단어 교정 결과
    result = symspell(jsonArray)
    print(result)

    # # url 리스트 받아오기
    # count = 2
    # url_list = getURL(result, count)
    # print("oh")
    # print(url_list)
    #
    # # 키워드와 설명 받아오기
    # jsonDic = {}
    # for i in range(0, len(url_list)):
    #     # 일단 오류 링크 제외
    #     try:
    #         print(url_list[i])
    #         article = Article(url_list[i], language='ko')
    #         article.download()
    #         article.parse()
    #         kkma = Kkma()
    #         sentences = kkma.sentences(article.text)
    #         for idx in range(0, len(sentences)):
    #             if len(sentences[idx]) <= 10:
    #                 sentences[idx - 1] += (' ' + sentences[idx])
    #                 sentences[idx] = ''
    #         if len(sentences) < 10:
    #             continue
    #     except:
    #         continue
    #     dic = {}
    #     keyword, word, sent = getResult(url_list[i], result[i % count])
    #     dic["word"] = word
    #     dic["sent"] = sent
    #     jsonDic[keyword] = dic
    #
    # jsonObject = json.dumps(jsonDic, ensure_ascii=False)
    # print(jsonObject)

    # get data from db
    jsonObject = get_db_data(result)
    jsonResp = json.dumps(jsonObject, ensure_ascii=False)
    print(jsonResp)
    print(type(jsonObject))

    # 태그만 추출해서 문자열 형식으로 변환 for 워드클라우드 입력형식
    tags = []
    jsonArr = json.loads(jsonResp)
    for i in jsonArr:
        if i["tag1"] is not None:
            tags.append(i["tag1"])
        if i["tag2"] is not None:
            tags.append(i["tag2"])
        if i["tag3"] is not None:
            tags.append(i["tag3"])
        if i["tag4"] is not None:
            tags.append(i["tag4"])
        if i["tag5"] is not None:
            tags.append(i["tag5"])

    # 가중치
    for i in weightList:
        if i in tags:
            tags.append(i)

    print(tags)
    tags = list(set(tags)) # 중복 제거
    text = ""
    for i in tags:
        text += str(i) + " "
    print(text) # ex. text = "혈당조절 신장결석 근육"

    wordcloud = WordCloud(font_path='font/NanumGothic.ttf', background_color='white').generate(text)
    plt.figure(figsize=(22, 22))  # 이미지 사이즈 지정
    plt.imshow(wordcloud, interpolation='lanczos')  # 이미지의 부드럽기 정도
    plt.axis('off')  # x y 축 숫자 제거
    plt.show()
    plt.savefig('./static/picture.png', dpi=300)

    message = {
        'status': 200,
        'message': 'OK',
        'scores': jsonResp,
        'url': 'http://3.35.255.25:80/static/picture.png'
    }
    resp = jsonify(message)
    resp.status_code = 200
    print(resp)

    return resp


# 서버 실행
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)