from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
from symspellpy import SymSpell, Verbosity
import json
from flask import make_response

from Symspell import sym_spell

def symspell(input_terms):
    result = []
    count = 0
    print(type(input_terms))

    for i in range(0, len(input_terms)):
        suggestions = sym_spell.lookup(
            input_terms[i], Verbosity.CLOSEST,
            max_edit_distance=2, include_unknown=False)  # include_unknown : 일치하는 결과가 없을 경우 입력 단어 반환

        # 첫 번째 것만 저장함
        for suggestion in suggestions:
            result.append(str(suggestion).split(',')[0])
            break

    return result