# coding:utf-8
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 前期:1 後期:2
url = "http://www.z.k.kyoto-u.ac.jp/zenkyo/syllabus?utf8=%E2%9C%93&condition%5Bcondition.semester%5D=" + \
"2" + \
"&condition%5Bcondition.targetStudent%5D=&condition%5Bcondition.courseTitle%5D=&condition%5Bcondition.teacherName=&condition%5Bcondition.oldFamilies%5D%5B1%5D=true&condition%5Bcondition.oldFamilies%5D%5B2%5D=true&condition%5Bcondition.oldFamilies%5D%5B3%5D=true&x=38&y=17"
response1 = requests.get(url)
print(response1.status_code == 200)
bs1 = BeautifulSoup(response1.content,"lxml")
totalCount = bs1.select('.total-count')
table = []
for i in range(1,int(int(totalCount[0].text)/10)+2):
    url = "http://www.z.k.kyoto-u.ac.jp/zenkyo/syllabus/syllabus-detail?condition%5Bcondition.courseTitle%5D=&condition%5Bcondition.oldFamilies%5D%5B1%5D=true&condition%5Bcondition.oldFamilies%5D%5B2%5D=true&condition%5Bcondition.oldFamilies%5D%5B3%5D=true&condition%5Bcondition.semester%5D=" + \
    "2" + \
    "&condition%5Bcondition.targetStudent%5D=&condition%5Bcondition.teacherName%5D=&condition%5Bpage%5D=1&page=" + \
    str(i)
    response = requests.get(url)
    bs = BeautifulSoup(response.content,"lxml")
    dayPeriod = bs.select('.day-period')[1::2]
    classroom = bs.select('.classroom')[1::2]
    grade = bs.select('.grade-allotted')[1::2]
    for k in range(0,len(classroom)):
        table.append([dayPeriod[k].text, classroom[k].text.strip(), grade[k].text])
        print(table[(i-1)*10+k])
df = pd.DataFrame(table,columns=['時限', '教室', '回生'])
df.to_csv("classroom.sjis.csv", encoding="shift_jis")
