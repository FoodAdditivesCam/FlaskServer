# Symspell 결과 반환
from flask import request, jsonify
from flask_restx import Resource, Namespace
from symspellpy import SymSpell, Verbosity
import json
from flask import make_response

# 이 페이지의 이름이 Symspell이라고 정의해주는 것.
Symspell = Namespace('Symspell')

sym_spell = SymSpell()
dictionary_path = 'dictionary.txt'
sym_spell.load_dictionary(dictionary_path, 0, 1, separator="$")

# 3.35.255.25/Symsepll/<input_term> 주소가 들어왔을 때 실행
@Symspell.route('/<string:input_term>')
class TodoPost(Resource):
    def get(self, input_term):
        # input_term 오타 교정
        suggestions = sym_spell.lookup(
            input_term, Verbosity.CLOSEST,
            max_edit_distance=2, include_unknown=False)  # include_unknown : 일치하는 결과가 없을 경우 입력 단어 반환

        result = {}
        count = 0
        for suggestion in suggestions:
            result[count] = str(suggestion)
            count += 1

        message = {
            'status': 200,
            'message': 'OK',
            'scores': result
        }
        resp = jsonify(message)
        resp.status_code = 200
        print(resp)

        # json 형식으로 반환
        return resp