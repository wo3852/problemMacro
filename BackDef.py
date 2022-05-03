from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import json


class BackDef:
    def init(self):

        self.cl = "Python"
        self.imgUrl = "'" + "https://ifh.cc/g/zjvJzN.jpg" + "'"

        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')  # 드라이버 브라우저 창 최대 화

        self.driver = webdriver.Chrome(options=options)  # 드라이버 옵션 추가
        self.driver.implicitly_wait(10)

        # json 파일에 정보가 없을 경우 입력 받아 저장
        with open('info.json') as js:
            jo = json.load(js)

        if jo["backjoon"]["user_id"] == "":
            jo["backjoon"]["user_id"] = input("아이디를 입력해주세요")

        if jo["backjoon"]["user_password"] == "":
            jo["backjoon"]["user_password"] = input("비밀번호를 입력해주세요")

        if jo["backjoon"]["file_name"] == "":
            jo["backjoon"]["file_name"] = input("등록할 파일이름을 입력해주세요")

        with open('info.json', 'w') as f:
            json.dump(jo, f, indent=2)

        self.json_object = jo["backjoon"]

    def page_start(self):  # 드라이버에서 사이트 접근
        self.driver.get("https://www.acmicpc.net/")
        

    def login(self):  # json 파일에서 로그인 정보 파싱 후 로그인
        self.driver.find_element_by_partial_link_text("로그인").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/form/div[2]/input").send_keys("wo3852@naver.com")
        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/form/div[3]/input").send_keys("jw9868")
        
        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/form/div[4]/div[2]/button").click()
        input("넘어가려면 엔터를 누르세요")
        time.sleep(1)

    def search(self):  # 검색조건 클릭
        time.sleep(0.2)
        self.driver.get("https://www.acmicpc.net/problemset")
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[1]/ul/li[7]/a").click()
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[5]/div/form/fieldset[1]/div/section/div/label[5]/i").click()
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[5]/div/form/fieldset[1]/div/fieldset/section[1]/div/label[1]/i").click()
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[5]/div/form/fieldset[2]/div/fieldset[1]/section[2]/div/label[1]/i").click()
        
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[5]/div/form/footer/button[1]").click()
        time.sleep(0.5)

    def soup_start(self):  # soup 드라이버 html 코드 새로고침
        time.sleep(1)
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")


def md_text_start(cl, title, imgUrl,stackStr):  # 마크다운 서식 추가
    s = "---\n"
    s += "title: " + title + "(" + cl + ")" + stackStr + "\n"
    s += "layout: post\n"
    s += "post-image: " + imgUrl + "\n"
    s += "description: 백준 알고리즘의 문제 " + "'" + title + "'" + " 문제풀이입니다.\n"
    s += "tags:\n"
    s += "- 알고리즘\n"
    s += "- 백준알고리즘\n"
    s += "- " + cl + "\n"
    s += "---\n\n"
    return s


def get_quote(s):  # 마크다운 인용구 반환
    return "\n>**" + s + "**\n\n"


def get_code(tag_list,driver):  # 풀었던 문제코드 크롤링 후 반환
    s = get_quote("문제풀이")
    for code in tag_list:
        if code.find("pre", "CodeMirror-line") == None: continue
        s += "\t" + code.find("pre", "CodeMirror-line").text.replace("​", "").replace(" ", "") + "\n"
    driver.back()
    driver.back()
    driver.back()
    return s


# 마크다운 크롤링 결과 반환
def get_explanation(tag_list):
    s = ""
    for j in tag_list:
        section_id = j.find("section").attrs["id"]
        if section_id == "hint" or section_id == "limit": continue

        if "sampleinput" in section_id:
            if j.find("div", "row") == None: continue
            temp = j.find("div", "row").find_all("div", "col-md-6")
            for t in temp:
                s += "\n>** " + (t.find("section").find("div", "headline").text.replace("복사", "").strip()).replace(" ","") + " **\n\n"
                for ti in t.find("section").find("pre").text.split("\n")[:-1]:
                    s += "\t" + ti.replace(" ", "") + "\n"
            continue
        if j.find("div", "headline") == None: continue
        s += "\n>** " + (j.find("div", "headline").text.replace("\n", "").replace(" ", "")) + " **\n\n"
        if j.find("div", "problem-text") == None: continue
        for h in j.find("div", "problem-text").find_all("p"):
            if h == "\n":
                continue
            elif h.find("img") == None:
                s += h.text.replace(" ", "") + "\n"
            else:
                s += "\n" + str(h.find("img")) + "\n\n"
    return s