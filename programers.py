import ProDef
import datetime
import time
from selenium.webdriver.common.keys import Keys

def start():
    pd = ProDef.ProDef() #객체 생성

    pd.init()  # 초기 값 시작
    pd.page_start() # 드라이버에서 프로그래머스 홈페이지 열기
    pd.login()  # 드라이버에서 제이슨 정보 확인 후 로그인
    
    pd.search() # 드라이버에서 검색 옵션 클릭
    
    
    page_list = pd.driver.find_element_by_xpath("/html/body/div[3]/div/div[3]/div/section/div[2]/div/div/div[1]/div/nav/ul").find_elements_by_tag_name("li")
    title_list = []
    #
    format = '%Y-%m-%d'

    checkListFileR = open("checklist.txt", 'r', encoding="UTF-8")
    checkList = checkListFileR.readlines()
    count = len(checkList)

    dt_datetime = datetime.datetime.now()

    for page in range(1,len(page_list)-1):
        time.sleep(1)
        pd.soup_start()

        for i in pd.soup.find_all("h4"):
            s = ""
            for j in i.text.split()[2:]:
                s += j +" "
            s = s.strip()
            if s == "" or s == "문제":continue
            time.sleep(0.25)
            if s in checkList:continue
            checkListFileW = open("checklist.txt", 'a', encoding="UTF-8")
            checkListFileW.write(s + "\n")
            checkListFileW.close()
            print(s)
            pd.driver.find_element_by_partial_link_text(s).send_keys(Keys.ENTER)
            time.sleep(0.5)
            pd.soup_start()
            if pd.soup.find("svg","ic-blue-grey-200") != None:
                pd.driver.find_element_by_xpath("/html/body/div[11]/div[3]").find_element_by_tag_name("svg").find_element_by_tag_name("use").click()
            time.sleep(0.5)
            cl = pd.soup.find("button","dropdown-toggle").text.strip()
            str_datetime = datetime.datetime.strftime(dt_datetime, format)
            f = open('mdZip/'+str_datetime + "-" + pd.json_object["file_name"]+cl+str(count) +".md", 'a', encoding="UTF-8")
            f.write(ProDef.md_text_start(cl,s,pd.imgUrl))

            pd.soup_start()
            f.write(ProDef.get_explanation(pd.soup.find("div", "markdown solarized-dark").contents))
            f.write(ProDef.get_code(pd.soup.find_all(attrs={'class': 'CodeMirror-line'})))
            
            f.close()
            pd.driver.back()
            count += 1
            if page != 1:
                time.sleep(0.5)
                p = pd.driver.find_element_by_xpath("/html/body/div[3]/div/div[3]/div/section/div[2]/div/div/div[1]/div/nav/ul").find_elements_by_tag_name("li")[1:-1]
                p[page-1].click()

            title_list.append(s)
        time.sleep(0.5)
        pd.driver.find_element_by_class_name('next_page').click()
    print(title_list)