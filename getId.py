# This is a sample Python script.
import traceback
import requests
import re
from bs4 import BeautifulSoup
import pypinyin
from soupsieve.util import lower


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def getAPI(get_id):
    try:
        req = requests.get("https://ordering.kcisec.com/chaxun.asp?kahao=" + get_id)
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        #                   "Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        # }
        reqt = req.text.encode('iso-8859-1').decode('gbk')
        soup = BeautifulSoup(reqt, 'html.parser')
        body = soup.body
        table = body.find('table', width='800')
        td = table.find('td', align='center', valign='top')
        span = td.find('span')
        span_text = span.text
        if span is None or span_text == "无此帐户，或帐户已被锁定！":
            return
        name = re.sub(r"\[.*?\](.+?) \d{4}/\d{1,2}/\d{1,2}.{4}", r"\1", span_text)
        print("Get " + get_id + " = " + name)
        return name
    except Exception as ex:
        traceback.print_exc()
        print("Error occurred when get API!")
        return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("华东开户学武系统 ver1.0 by Idad Wind in Python")
    print("For learning reference only, not abusing, or you will take the risk!")
    print()

    query_mode = input("Query mode ([o]nce, [a]ll, [c]ount)? ")
    if query_mode == "":
        query_mode = "once"
    mode = input("Query by ([N]ormal, [p]inyin, [r]egular expression, [i]d)? ")
    if mode == "":
        mode = "normal"
    mode = lower(mode)

    query = input("Enter id: ")

    if mode == "i" or mode == "id":
        staff_name = getAPI(query)
        if staff_name is None:
            print(query + " does not exist")
        else:
            staff_name = pypinyin.slug(staff_name, style=pypinyin.Style.NORMAL, separator=' ')
            print("As in pinyin - " + staff_name)
    else:
        staff_name = ""
        i = int(input("min: "))
        j = int(input("max: "))
        result = []
        condition = False
        while not (condition and (query_mode == "o" or query_mode == "once")) and i <= j:
            condition = False
            i += 1
            staff_name = getAPI(str(i))
            if staff_name is None:
                continue
            if mode == "pinyin" or mode == "p":
                staff_name = pypinyin.slug(staff_name, style=pypinyin.Style.NORMAL, separator=' ')
                print("Formed into pinyin - " + staff_name)
            condition = ((mode == "regular expression" or mode == "r") and re.match(query, staff_name)) \
                        or query == staff_name
            if condition:
                print(staff_name + " matched")
                result.append(str(i))

        print()
        if len(result) == 0:
            print(query + " did not exists in the given range!")
        else:
            if query_mode == "a" or query_mode == "all":
                print("Matched objects: ")
                print(result)
                print("count: " + str(len(result)))
            elif query_mode == "o" or query_mode == "once":
                print("Matched object: ")
                print(str(i))
            elif query_mode == "c" or query_mode == "count":
                print("Matched object count: " + str(len(result)))

    # header = {"cookie": "DSAI=" + query}
    # def getAPIs(urls: list) -> list:
    #     for i in urls:
    #         print("Getting " + i)
    #         req = requests.get(i, headers=header)
    #         print(req.text)
    #         print(json.loads(req.text))
    # print("Options: ")
    # print("1\tRegular query\t\t\t\tpowered by 学武系统")
    # print("2\tDeep query\t\t\t\t\tpowered by 学武系统")
    # print("3\tFill application form\t\tpowered by 学武系统")
    # print("4\tGet personal information\tpowered by 康桥开户")
    # print("5\tGet today's meals\t\t\tpowered by 订餐系统")
    # print("6\tExit")
    #
    # while True:
    #     mode = input("Select an option to process: ")
    #     match mode:
    #         case "1":
    #             print("Regular query API powered by 学武系统 python edition")
    #             urls = [
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     # "http://campus.kcisec.com/Form_List?strKeyWord1=1&strKeyWord2=&strOP1=or",
    #                     "http://campus.kcisec.com/DSAI/Query/Form_ListWarningMail?strKeyWord1=&strKeyWord2=&strOP1=or",
    #                     "http://campus.kcisec.com/DSAI/Query/Form_ListRewards?strKeyWord1=&strKeyWord2=&strOP1=or",
    #                     "http://campus.kcisec.com/DSAI/Query/Form_ListDetention?strKeyWord1=&strKeyWord2=&strOP1=or",
    #                     "http://campus.kcisec.com/DSAI/Query/Form_ListRewardsAll?strKeyWord1=&strKeyWord2=&strOP1=or"
    #                     ]
    #             getAPIs(urls)
    #         case "2":
    #             pass
    #         case "3":
    #             pass
    #         case "4":
    #             pass
    #         case "5":
    #             pass
    #         case "6":
    #             break
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
