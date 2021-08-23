from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver

def getURL(keywords, size):
    # crawling
    search_filtering = ' -유튜브, -아프리카티비, -지마켓, -옥션, -쇼핑몰, -TV'
    search_words = ['', ' 사전', ' 효능', ' 부작용']  # 검색어 option list
    result = []
    for keyword in keywords:
        for search_word in search_words:
            final_search_word = keyword + search_word + search_filtering
            result += crawling(final_search_word, size)

    # tokenize
    url = result  # url list
    return url

def crawling(keyword, size):
    baseUrl = 'https://www.google.com/search?q='
    url = baseUrl + quote_plus(keyword)

    # todo: webdriver option 설정
    #path = '/Users/beans_bin/Downloads/chromedriver'
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