
# ¼­¹ö°¡ µ¹¾Æ°¡´Â ¸ÞÀÎ ÆäÀÌÁö
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
import os
from models import data_update, db, get_db_data


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#api = Api(app)

# # ºÐ¸®ÇÑ ÆÄÀÏÀ» api¿¡ µî·Ï
# api.add_namespace(Symspell, '/symspell')
# api.add_namespace(Crawling, '/crawling')


dictionary_path = 'dictionary.txt'
sym_spell.load_dictionary(dictionary_path, 0, 1, separator="$")

# DB
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir °æ·Î¾È¿¡ DBÆÄÀÏ ¸¸µé±â
dbfile = os.path.join(basdir, 'db.sqlite') # D:‚2021‚GradProject‚FlaskServer‚db.sqlite
# SQLAlchemy ¼³Á¤
# ³»°¡ »ç¿ë ÇÒ DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# ºñÁö´Ï½º ·ÎÁ÷ÀÌ ³¡³¯¶§ Commit ½ÇÇà(DB¹Ý¿µ)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# ¼öÁ¤»çÇ×¿¡ ´ëÇÑ TRACK
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

    jsonArray = jsonObject.get("input")
    jsonArray = jsonArray.replace('[', '').replace(']', '').split(',')

    # ´Ü¾î ±³Á¤ °á°ú
    result = symspell(jsonArray)
    print(result)

    # # url ¸®½ºÆ® ¹Þ¾Æ¿À±â
    # count = 2
    # url_list = getURL(result, count)
    # print("oh")
    # print(url_list)
    #
    # # Å°¿öµå¿Í ¼³¸í ¹Þ¾Æ¿À±â
    # jsonDic = {}
    # for i in range(0, len(url_list)):
    #     # ÀÏ´Ü ¿À·ù ¸µÅ© Á¦¿Ü
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

    message = {
        'status': 200,
        'message': 'OK',
        'scores': jsonResp
    }
    resp = jsonify(message)
    resp.status_code = 200
    print(resp)

    return resp


# ¼­¹ö ½ÇÇà
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)