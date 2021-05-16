from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
# todo: bs4, selenium install

def crawling(keyword, size):
    baseUrl = 'https://www.google.com/search?q='
    url = baseUrl + quote_plus(keyword)

    # todo: webdriver option 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
    chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
    chrome_options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # todo: 읽어온 페이지의 html 코드 받아오기
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    result = {}  # 검색 결과의 리스트 저장, key=문서이름, value=문서링크
    lists = soup.select('#rso > .g')

    # 가져올 사이트 개수 조정
    cur_doc_count = 0

    # todo: 검색 결과의 리스트 저장
    for list in lists:
        name = list.select_one('.LC20lb.DKV0Md').text
        link = list.a.attrs['href']
        result[name] = link
        cur_doc_count+=1
        # 가져올 사이트 개수 조정
        if cur_doc_count>size:
            break
    print(result)

    contents = {}  # 모든 문서의 내용 저장, key=문서이름, value=문서 body 내용
    # todo: 각 문서에 대한 html body부분 저장
    for key, val in result.items():
        driver.get(val)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # html의 태그 추출해서 삭제
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])] # header, footer
        content=soup.find('body').getText()

        content = content.replace("\n", " ")
        contents[key] = content
        print(content)
    driver.close()
    return contents

# main code
keywords = ['토마토'] # 검색어 리스트 toy
search_words = [' ',' 사전',' 효능',' 부작용'] # 검색어 option list
search_filtering = ' -유튜브, -아프리카티비, -지마켓, -옥션, -쇼핑몰'
size = 3
final_search_word = {}
result={}
for keyword in keywords:
    for search_word in search_words:
        print(keyword+search_word+search_filtering)
        result[keyword] = crawling(keyword+search_word+search_filtering, size)

# f = open('crawlingResult.txt', 'w')
# f.write(str(result))
# f.close()
print(result)
