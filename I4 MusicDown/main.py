from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
import csv


url = 'https://www.i4.cn/ring_1_0_1.html'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

title_tmp = soup.find_all('div', attrs={'class': 'title'})[1:-1]
title_list = [i.get_text() for i in title_tmp]
# print(title_list)

downcount_tmp = soup.find_all('div', attrs={'class': 'downcount'})
downcount_list = [i.get_text() for i in downcount_tmp]
# print(downcount_list)

with open('MusicDown.csv', 'w', newline='') as f:
    f_csv = csv.writer(f)
    for index in range(len(title_list)):
        f_csv.writerow([title_list[index], downcount_list[index]])

x_data, y_data =  [], []
with open('MusicDown.csv', 'r') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        x_data.append(row[0])
        y_data.append(row[1])

y_data = [int(tmp.replace('万', '0000').replace('次', '')) for tmp in y_data]
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title('铃声下载数据分析')
plt.xlabel('歌曲名称')
plt.ylabel('下载次数')
plt.xticks(rotation=90)
plt.plot(x_data, y_data)
plt.show()