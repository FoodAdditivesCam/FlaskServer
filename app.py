# 서버가 돌아가는 메인 페이지
from flask import Flask
from flask_restx import Resource, Api
from Symspell import Symspell


app = Flask(__name__)
api = Api(app)

# 분리한 파일을 api에 등록
api.add_namespace(Symspell, '/symspell')

# 서버 실행
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)