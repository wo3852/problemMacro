from selenium.webdriver.common.keys import Keys
import time
import datetime
import BackDef

def start():
    format = '%Y-%m-%d'

    checkListFileR = open("checklist.txt", 'r', encoding="UTF-8")
    checkList = checkListFileR.readlines()
    for i in range(len(checkList)):
        checkList[i] = checkList[i].replace("\n","")
    count = len(checkList)
    dt_datetime = datetime.datetime.now()

    bd = BackDef.BackDef()
    bd.init()
    bd.page_start()
    # 로그인
    bd.login()
    # 옵션세팅
    bd.search()
    # 문제 선택
    paging = bd.driver.find_element_by_class_name("pagination").find_elements_by_tag_name("li")

    for page in range(1,len(paging)+1):
        name_list = []
        bd.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[6]/div[2]/div/ul/li["+str(page)+"] / a").click()
        item_list = bd.driver.find_element_by_id("problemset").find_element_by_tag_name("tbody").find_elements_by_tag_name(
            "tr")
        for il in item_list:
            a_tag = il.find_elements_by_tag_name("td")[1].find_element_by_tag_name("a")
            name_list.append(a_tag.text)

        for i in name_list:
            if i in checkList: continue
            checkListFileW = open("checklist.txt", 'a', encoding="UTF-8")
            checkListFileW.write(i + "\n")
            checkListFileW.close()
            print(i)
            bd.driver.find_element_by_link_text(i).send_keys(Keys.ENTER)
            time.sleep(0.5)
            bd.soup_start()
            stackStr = ""
            str_datetime = datetime.datetime.strftime(dt_datetime, format)
            if bd.soup.find("ul", "spoiler-list") != None:
                stack = bd.soup.find("ul", "spoiler-list").find_all("li")
                for st in stack:
                    stackStr += "(" + st.text.strip() + ")"
            f = open('mdZip/' + str_datetime + "-" + bd.json_object["file_name"] + str(count) + ".md", 'a', encoding="UTF-8")
            f.write(BackDef.md_text_start(bd.cl,i,bd.imgUrl,stackStr))

            f.write(BackDef.get_explanation(bd.soup.find("div", id="problem-body").find_all("div", "col-md-12")))

            bd.driver.find_element_by_partial_link_text("내 제출").click()
            bd.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[6]/div/table/tbody/tr[1]/td[7]/a[1]").click()
            
            bd.soup_start()
            f.write(BackDef.get_code(bd.soup.find("div", "CodeMirror-code").find_all("div"),bd.driver))
            f.close()
            count += 1