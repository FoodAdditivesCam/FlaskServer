# -*- coding: cp949 -*-
# 서버가 돌아가는 메인 페이지
import json

from konlpy.tag import Kkma
from newspaper import Article

from Symspell_py import symspell
from GetURL_py import getURL
from crawling_py import getResult

from flask import Flask, request, jsonify
from Symspell import Symspell, sym_spell
from flask import request, jsonify
import json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#api = Api(app)

# # 분리한 파일을 api에 등록
# api.add_namespace(Symspell, '/symspell')
# api.add_namespace(Crawling, '/crawling')


dictionary_path = 'dictionary.txt'
sym_spell.load_dictionary(dictionary_path, 0, 1, separator="$")

@app.route('/result', methods=['POST'])
def post():
    print(request.is_json)
    jsonObject = request.get_json()
    input_terms = []
    result = []

    jsonArray = jsonObject.get("input")
    print(jsonArray)

    for list in jsonArray:
        print(list)
        input_terms.append(list)

    # 단어 교정 결과
    result = symspell(jsonArray)
    print(result)

    # url 리스트 받아오기
    url_list = getURL(result, 2)
    print("oh")
    print(url_list)


    # 키워드와 설명 받아오기
    jsonDic = {}
    for i in range(0, len(url_list)):
        # 일단 오류 링크 제외
        try:
            print(url_list[i])
            article = Article(url_list[i], language='ko')
            article.download()
            article.parse()
            kkma = Kkma()
            sentences = kkma.sentences(article.text)
            for idx in range(0, len(sentences)):
                if len(sentences[idx]) <= 10:
                    sentences[idx - 1] += (' ' + sentences[idx])
                    sentences[idx] = ''
            if len(sentences) < 10:
                continue
        except:
            continue
        dic = {}
        keyword, word, sent = getResult(url_list[i], i)
        dic["word"] = word
        dic["sent"] = sent
        jsonDic[keyword] = dic

    jsonObject = json.dumps(jsonDic, ensure_ascii=False)
    print(jsonObject)

    message = {
        'status': 200,
        'message': 'OK',
        'scores': jsonObject
    }
    resp = jsonify(message)
    resp.status_code = 200
    print(resp)

    return resp


# 서버 실행
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)