# Crawling 결과 반환
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import json
from flask import make_response
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
# -*- coding: cp949 -*-
from krwordrank.sentence import summarize_with_sentences
from krwordrank.word import KRWordRank
from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
# todo: install krwordrank

from data_list import get_stopwords

# 이 페이지의 이름이 Crawling이라고 정의해주는 것.
Crawling = Namespace('Crawling')

# 3.35.255.25/crawling/<keyword>/<size> 주소가 들어왔을 때 실행
@Crawling.route('/<string:keyword>/<int:size>')
class Search(Resource):
    def get(self, keyword, size):
        # crawling
        keywords=[]  # 검색어 리스트
        keywords.append(keyword)
        search_filtering = ' -유튜브, -아프리카티비, -지마켓, -옥션, -쇼핑몰, -TV'
        search_words = ['', ' 사전', ' 효능', ' 부작용']  # 검색어 option list
        result = []
        for keyword in keywords:
            for search_word in search_words:
                final_search_word = keyword + search_word+search_filtering
                result+=self.crawling(final_search_word, size)

        # tokenize
        url = result # url list
        sentences = []
        sent_tokenize = SentenceTokenizer()
        for i in range(0, len(url)):
            sentences += (sent_tokenize.url2sentences(url[i]))
        print(sentences)
        nouns = sent_tokenize.get_nouns(sentences)
        print(nouns)

        # train KR-WordRank model
        wordrank_extractor = KRWordRank(
            min_count=5,  # 단어의 최소 출현 빈도수 (그래프 생성 시)
            max_length=10,  # 단어의 최대 길이
            verbose=True
        )

        beta = 0.85  # PageRank의 decaying factor beta
        max_iter = 10
        keywords, rank, graph = wordrank_extractor.extract(sentences, beta, max_iter)
        stopwords = get_stopwords()

        # Check top 30 keywords with corresponding score
        for word, r in sorted(keywords.items(), key=lambda x: -x[1])[:30]:
            if not (word in stopwords):
                print('%8s : %.4f' % (word, r))

        # 핵심 문장 추출하기
        # remove stopwords
        passwords = {word: score for word, score in sorted(
            keywords.items(), key=lambda x: -x[1])[:300] if not (word in stopwords)}

        print('num passwords = {}'.format(len(passwords)))

        penalty = lambda x: 0 if (25 <= len(x) <= 80 and not '마지막' in x) else 1,
        keywords, sents = summarize_with_sentences(
            sentences,
            penalty=penalty,
            stopwords=stopwords,
            diversity=0.5,
            num_keywords=100,
            num_keysents=10,
            verbose=False
        )

        for i in sents:
            print(i)

        # 결과 json으로 출력
        message = {
            'status': 200,
            'message': 'OK',
            'content': sents
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

    # crawling method: output is link list
    def crawling(self, keyword, size):
        baseUrl = 'https://www.google.com/search?q='
        url = baseUrl + quote_plus(keyword)

        # todo: webdriver option 설정
        path = '/home/ubuntu/FlaskServer/chromedriver' # chromedriver.exe /home/ubuntu/FlaskServer/chromedriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
        chrome_options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome(path,options=chrome_options)
        driver.get(url)

        # todo: 읽어온 페이지의 html 코드 받아오기
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        link_result = {}  # 검색 결과의 리스트 저장, key=문서이름, value=문서링크
        link_result_2 = [] # 리스트만
        lists = soup.select('#rso > .g')

        # 가져올 사이트 개수 조정
        cur_doc_count = 0

        # todo: 검색 결과의 리스트 저장
        for list in lists:
            name = list.select_one('.LC20lb.DKV0Md').text
            link = list.a.attrs['href']
            link_result[name] = link
            link_result_2.append(link)
            cur_doc_count += 1
            # 가져올 사이트 개수 조정
            if cur_doc_count >= size:
                break
        print(link_result_2)

        return link_result_2


class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        self.twitter = Twitter()
        self.stopwords = ['중인' ,'만큼', '마찬가지', '꼬집었', "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자"
        ,"아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가",]
    def url2sentences(self, url):
        article = Article(url, language='ko')
        article.download()
        article.parse()
        sentences = self.kkma.sentences(article.text)

        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

    def text2sentences(self, text):
        sentences = self.kkma.sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence is not '': # SyntaxWarning: "is not" with a literal. Did you mean "!="?
                nouns.append(' '.join([noun for noun in self.twitter.nouns(str(sentence))
            if noun not in self.stopwords and len(noun) > 1]))
        return nouns



