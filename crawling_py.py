from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver


def crawling(keyword):
    baseUrl = 'https://www.google.com/search?q='
    url = baseUrl + quote_plus(keyword)

    # webdriver option 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--no-sandbox")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
    chrome_options.add_argument("--disable-gpu")  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
    chrome_options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # 읽어온 페이지의 html 코드 받아오기
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    result = {}  # 검색 결과의 리스트 저장, key=문서이름, value=문서링크
    lists = soup.select('#rso > .g')
    # 검색 결과의 리스트 저장
    for list in lists:
        name = list.select_one('.LC20lb.DKV0Md').text
        print(name)

        link = list.a.attrs['href']
        print(link)
        print()
        result[name] = link

    contents = {}  # 모든 문서의 내용 저장, key=문서이름, value=문서 body 내용
    # 각 문서에 대한 html body부분 저장
    for key, val in result.items():
        print(val)
        driver.get(val)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        content = soup.find('body').text
        content = content.replace("\n", " ")
        contents[key] = content
        print(content)
    driver.close()
    return contents

# main code
keywords = ['토마토', '코코아']
result={}
for i in keywords:
    result[i] = crawling(i)
print(result)