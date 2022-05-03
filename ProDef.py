from selenium import webdriver
from  bs4 import  BeautifulSoup
import time
import re
import json

class ProDef:
    def init (self):

        self.imgUrl = "'" + "https://ifh.cc/g/paXC3t.jpg" + "'"

        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized') # 드라이버 브라우저 창 최대 화

        self.driver = webdriver.Chrome(options=options) # 드라이버 옵션 추가
        self.driver.implicitly_wait(10)

        # json 파일에 정보가 없을 경우 입력 받아 저장
        with open('info.json') as js:
            jo = json.load(js)

        if jo["programers"]["user_id"] == "":
            jo["programers"]["user_id"] = input("아이디를 입력해주세요")

        if jo["programers"]["user_password"] == "":
            jo["programers"]["user_password"] = input("비밀번호를 입력해주세요")

        if jo["programers"]["file_name"] == "":
            jo["programers"]["file_name"] = input("등록할 파일이름을 입력해주세요")

        with open('info.json', 'w') as f:
            json.dump(jo, f,indent=2)

        self.json_object = jo["programers"]

    def page_start(self): # 드라이버에서 사이트 접근
        self.driver.get("https://programmers.co.kr/learn/challenges")
        

    def login(self): #json 파일에서 로그인 정보 파싱 후 로그인
        self.driver.find_element_by_partial_link_text('로그인').click()
        self.driver.find_element_by_id('user_email').send_keys(self.json_object["user_id"])
        self.driver.find_element_by_id('user_password').send_keys(self.json_object["user_password"])
        self.driver.find_element_by_id('btn-sign-in').click()
        time.sleep(1)
        

    def search(self): # 검색조건 클릭
        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[3]/div/section/div[1]/div[1]/div[1]/div[2]/button').click()
        
        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[3]/div/section/div[1]/div[1]/div[1]/div[2]/div/div[1]/label/input').click()
        time.sleep(1)
        
    def soup_start(self): # soup 드라이버 html 코드 새로고침
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")

def md_text_start(cl,title,imgUrl): # 마크다운 서식 추가
    s = "---\n"
    s += "title: " + title +"("+cl+")"+ "\n"
    s += "layout: post\n"
    s += "post-image: " + imgUrl + "\n"
    s += "description: 백준 알고리즘의 문제 " + "'" + title + "'" + " 문제풀이입니다.\n"
    s += "tags:\n"
    s += "- 알고리즘\n"
    s += "- 백준알고리즘\n"
    s += "- " + cl + "\n"
    s += "---\n\n"
    return s

def get_quote(s): # 마크다운 인용구 반환
    return "\n>**" + s + "**\n\n"

def get_code(tag_list): # 풀었던 문제코드 크롤링 후 반환
    s = get_quote("문제풀이")
    for code in tag_list:
        s += "\t" + str(code.text).replace(" ", "").replace("​", "") + "\n"
    return s

# 마크다운 크롤링 결과 반환
def get_explanation(tag_list):
    s = ""
    for markdown in tag_list:
        tag_name = markdown.name
        if tag_name == "hr": break
        if tag_name == None: continue
        if bool(re.match('h[0-9]', markdown.name)):
            s += get_quote(markdown.text.strip())
        elif tag_name == "p":
            if markdown.find("img") != None: #p태그안에 이미지 존재하면 html코드 저장
                s+= "\n" + str(markdown.find("img")) + "\n\n"
            else: #이미지가 존재하지않으면 p태그 text 저장
                s += markdown.text.strip() + "\n"
        elif tag_name == "ul": # 리스트 마크다운으로 저장
            s += markdown.text.strip()
        elif tag_name == "table": # 테이블 마크다운으로 저장
            table_count = 0
            Text = "|"
            for th in markdown.find("thead").find("tr").find_all("th"):
                Text += " " + th.text + " |"
                table_count += 1
            s += "\n" + Text + "\n"
            s +="|" + ("--|" * table_count) + "\n"
            Text = "|"
            for td in markdown.find("tbody").find("tr").find_all("td"):
                Text += " " + td.text + " |"
            s += Text + "\n\n"
    return s