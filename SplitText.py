class SplitText:
    def __init__(self):
        self.result = 0

    def splitTxt(self, text):
        ##읽어오는 과정에서 생긴 엔터 삭제
        text = text.replace("\r\n", "")
        text = text.replace("\n", "")

        ##읽어온 문자열 쉼표로 분리
        txt = text.split(",")
        ##쉼표로 분리한 문자열 스페이스바로 분리
        txt = txt.split(" ")
        ##스페이스바로 분리한 괄호로 분리
        txt = txt.split("(")
        txt = txt.split(")")

        ##text초기화
        text = list()

        for i in txt:
            ##비어있는 데이터 삭제
            if (len(i) == 0):
                continue

            ##의미없는 띄어쓰기 데이터, 숫자(퍼센트) 삭제
            first = i[0]
            if i == ' ' or first == '1' or first == '2' or first == '3' or first == '4' or first == '5' or first == '6' or first == '7' or first == '8' or first == '9' or first == '0':
                continue

            ##특수문자 삭제
            if i == ':' or i == '·' or i == '•' or i == '|' or i == "'":
                continue
            text.append(i)

        return text
