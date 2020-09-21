import requests
import os, time, re
from base64 import b64encode
from lxml import etree

login_url = 'http://jiaowu.jvtc.jx.cn/jsxsd/xk/LoginToXk'
lesson_url = "http://jiaowu.jvtc.jx.cn/jsxsd/framework/main_index_loadkb.jsp"

username = os.getenv("MYNAME")
password = os.getenv("MYWORD")
encoded = b64encode(username.encode()) + b'%%%' + b64encode(password.encode())

data = {
    "userAccount": username,
    "userPassword": password,
    "encoded": encoded.decode()
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
}

session = requests.Session()

res = session.post(login_url, headers=headers, data=data)
print(res.status_code)

now = time.strftime("%Y-%m-%d", time.localtime())

data = {
    'rq': now,
    'sjmsValue': '956C06E11ABA1DDFE0530100007FC305'
}
# 956C06E11ABA1DDFE0530100007FC305


res = session.post(lesson_url, headers=headers, data=data)
print(res.status_code)

html = etree.HTML(res.text)
# print(etree.tostring(html).decode())
lesson_list = html.xpath('//tbody//tr')
print(len(lesson_list))

reName = re.compile(r"课程名称：(.*?)<br/>")
reLocal = re.compile(r"上课地点：(.*?)<br/>")
lesson = []
for tr in lesson_list:
    row_list = tr.xpath(".//td")
    row = []
    for k in range(1, len(row_list)):
        content = row_list[k].xpath('./p/@title')
        if len(content) == 0:
            row.append([])
            continue
        content = content[0] + '<br/>'
        # print(content)
        lessonName = re.search(reName, content).group(1)
        lessonLocal = re.search(reLocal, content).group(1)
        # print(lessonName, lessonLocal)
        row.append(lessonName + '&' + lessonLocal)
    lesson.append(row)

for x in lesson:
    print(x)
