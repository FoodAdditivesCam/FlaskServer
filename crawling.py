# Crawling 결과 반환
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import json
from flask import make_response
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver

# 이 페이지의 이름이 Crawling이라고 정의해주는 것.
Crawling = Namespace('Crawling')

# 3.35.255.25/crawling/<keyword>/<size> 주소가 들어왔을 때 실행
@Crawling.route('/<string:keyword>/<int:size>')
class Search(Resource):
    def get(self, keyword, size):
        keywords=[]  # 검색어 리스트 toy
        keywords.append(keyword)
        search_filtering = ' -유튜브, -아프리카티비, -지마켓, -옥션, -쇼핑몰, -TV'
        search_words = ['', ' 사전', ' 효능', ' 부작용']  # 검색어 option list
        result = {}
        for keyword in keywords:
            for search_word in search_words:
                final_search_word = keyword + search_word+search_filtering
                result[final_search_word] = self.crawling(final_search_word, size)
                # resp = self.crawling(keyword + search_word, size)

        # 결과 json으로 출력
        message = {
            'status': 200,
            'message': 'OK',
            'content': result
        }
        resp = jsonify(message)
        resp.status_code = 200
        # print(resp)
        return resp

    def crawling(self, keyword, size):
        baseUrl = 'https://www.google.com/search?q='
        url = baseUrl + quote_plus(keyword)


        # todo: webdriver option 설정
        path = '/home/ubuntu/FlaskServer/chromedriver' # chromedriver.exe
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
        lists = soup.select('#rso > .g')

        # 가져올 사이트 개수 조정
        cur_doc_count = 0

        # todo: 검색 결과의 리스트 저장
        for list in lists:
            name = list.select_one('.LC20lb.DKV0Md').text
            link = list.a.attrs['href']
            link_result[name] = link
            cur_doc_count += 1
            # 가져올 사이트 개수 조정
            if cur_doc_count >= size:
                break
        print(link_result)

        contents = {}  # 모든 문서의 내용 저장, key=문서이름, value=문서 body 내용
        # todo: 각 문서에 대한 html body부분 저장
        for key, val in link_result.items():
            driver.get(val)

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")

            # html의 태그 추출해서 삭제
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]  # header, footer
            content = soup.find('body').getText()

            content = content.replace("\n", " ")
            contents[key] = content
            print(key)
        driver.close()

        # # 결과 json으로 출력
        # message = {
        #     'status': 200,
        #     'message': 'OK',
        #     'scores': link_result,
        #     'content': contents
        # }
        # resp = jsonify(message)
        # resp.status_code = 200
        # print(resp)

        # json 형식으로 반환
        return contents


# if __name__ == "__main__":
#     print(get_search_count("코코아"))




# 셀레니움 없이
    # url = "https://www.google.com/search?q={}".format(quote_plus(keyword))
    # print(url)
    # headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    # res = requests.get(url,headers)
    # soup = BeautifulSoup(res.text, 'html.parser')  # lxml
    # print(soup)
    # find = soup.find_all('.kCrYT')
    # r=soup.select('.r')
    # for i in r:
    #     print(i.a.attrs['href'])
    # find = soup.find('span', class_='BNeawe')

    # number = soup.select('.kCrYT')
    # names = []
    # links = []
    # for i in number:
    #     try:
    #         name = i.select_one('.BNeawe.vvjwJb.AP7Wnd').text
    #         names.append(name)
    #         link = i.a.attrs['href']
    #         print(link)
    #         link = link.lstrip('/url?q=')
    #         link = link.split('&')
    #         links.append(link[0])
    #     except:
    #         pass
    # print("------")
    # print(names)
    # print(links)
    # exit()
    # # print(find)
    # print(number)
    # exit()
    # number = number[number.find('약', ) + 2:number.rfind('개')]
    # number = int(number.replace(',', ''))
    # return {'keyword': keyword, 'number': number}

    # tF2Cxc, yuRUbf, & 전 uri
    # href="/url?q= , kCrYT or BNeawe



# # 셀레니움 있음
#     def get(self, keyword):
#         baseUrl = 'https://www.google.com/search?q='
#         url = baseUrl + quote_plus(keyword)
#
#         # webdriver option 설정
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('headless')
#         chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
#         chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
#         chrome_options.add_argument('lang=ko_KR')
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.get(url)
#
#         # 읽어온 페이지의 html 코드 받아오기
#         html = driver.page_source
#         soup = BeautifulSoup(html, "lxml")
#
#         result = {} # 검색 결과의 리스트 저장, key=문서이름, value=문서링크
#         lists = soup.select('#rso > .g')
#         # 검색 결과의 리스트 저장
#         for list in lists:
#             name = list.select_one('.LC20lb.DKV0Md').text
#             print(name)
#
#             link = list.a.attrs['href']
#             print(link)
#             print()
#             result[name] = link
#
#         contents= {} # 모든 문서의 내용 저장, key=문서이름, value=문서 body 내용
#         # 각 문서에 대한 html body부분 저장
#         for key, val in result.items():
#             print(val)
#             driver.get(val)
#             html = driver.page_source
#             soup = BeautifulSoup(html, "lxml")
#             content = soup.find('body').text
#             content = content.replace("\n", " ")
#             contents[key]=content
#             print(content)
#         driver.close()
#
#         # 결과 json으로 출력
#         message = {
#             'status': 200,
#             'message': 'OK',
#             'scores': result,
#             'content': contents
#         }
#         resp = jsonify(message)
#         resp.status_code = 200
#         print(resp)
#
#         # json 형식으로 반환
#         return resp