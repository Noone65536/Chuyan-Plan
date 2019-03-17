
import requests
from bs4 import BeautifulSoup
import time
import MySQLdb
import json
import tkinter as tk
import tkinter.messagebox

# 由于京东商品评论的网页经常更换，所以展示依然只能人工借助浏览器的NETWORK查看网络请求信息得到URL
# 并且用“{}”将页码替换（将“1&pageSize”替换成“{}&pageSize”）
# 缩进位数指的是京东商品标号数字个数，比如"...fetchJSON_comment98vv125108..."中的商品编号为125108，那么缩进位数就是6位

root = tk.Tk()  # Create root widget (windoe)

root.title('网店评论爬虫')
root.geometry('300x200')

label1 = tk.Label(root, text='输入网页：').grid(row=0)
label2 = tk.Label(root, text='输入起始页码：').grid(row=1)
label3 = tk.Label(root, text='输入结束页码：').grid(row=2)
label4 = tk.Label(root, text='缩进位数：').grid(row=3)
# 测试用网址https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv125108&productId=5054737&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1
varAdd = tkinter.StringVar()
varSta = tkinter.IntVar()
varEnd = tkinter.IntVar()
varSou = tkinter.IntVar()

address = tk.Entry(root,textvariable=varAdd).grid(row=0, column=1)
start = tk.Entry(root,textvariable=varSta).grid(row=1, column=1)
end = tk.Entry(root,textvariable=varEnd).grid(row=2, column=1)
suo = tk.Entry(root,textvariable=varSou).grid(row=3, column=1)

button = tk.Button(root, text='提交', command=root.quit).grid(row=4, column=1)

root.mainloop()  # Make the script remain in the event loop

print('爬取的网址是: %s' % varAdd.get())
print('开始的页数是: %d' % varSta.get())
print('结束的页数是: %d' % varEnd.get())

a = varSta.get()
b = varEnd.get()
suojin = varSou.get()

conn= MySQLdb.connect(host='localhost', user='root', passwd='223451ZHU2', db='scraping', charset='utf8')
cur=conn.cursor()
# python连接数据库


headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0'
}
# 设置浏览器请求头

urls = [varAdd.get().format
       (str(i)) for i in range(a, b)]   # 这里是需要爬取的页数

cookie={'TrackID':'1_VWwvLYiy1FUr7wSr6HHmHhadG8d1-Qv-TVaw8JwcFG4EksqyLyx1SO7O06_Y_XUCyQMksp3RVb2ezA',
'__jda':'122270672.1507607632.1423495705.1479785414.1479794553.92',
'__jdb':'122270672.1.1507607632|92.1479794553',
'__jdc':'122270672',
'__jdu':'1507607632',
'__jdv':'122270672|direct|-|none|-|1478747025001',
'areaId':'1',
'cn':'0',
'ipLoc-djd':'1-72-2799-0',
'ipLocation':'%u5317%u4EAC',
'mx':'0_X',
'rkv':'V0800',
'user-key':'216123d5-4ed3-47b0-9289-12345',
'xtest':'4657.553.d9798cdf31c02d86b8b81cc119d94836.b7a782741f667201b54880c925faec4b'}


def get_info(url):
    r = requests.get(url, headers=headers, cookies=cookie)
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.prettify()
    # print(content)
    jsondata = content[22 +suojin:-3]
    print(jsondata)
    data = json.loads(jsondata)
    # 将爬取的页面内容整理为完整且正确的json格式

    for i in data['comments']:
        id = i['id']
        productName = i['referenceName']
        commentTime = i['creationTime']
        content = i['content']

        print("商品全名:{}".format(productName))
        print("用户评论时间:{}".format(commentTime))
        print("用户评论内容:{}".format(content))

        sql = "insert into `urls` (`productName`,`commentTime`,`content`) values (%s,%s,%s)"
        cur.execute(sql, (productName, commentTime, content))

for url in urls:
    get_info(url)

time.sleep(1)

cur.close()
conn.commit()
conn.close()