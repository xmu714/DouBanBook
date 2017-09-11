import requests
import re
import csv,codecs
from bs4 import BeautifulSoup
url = 'https://book.douban.com/top250'

class DoubanBook_top250():
    def __init__(self):
        self.head = ['图书名字','作者','引述','出版社','发行日期','价格','评分','评价人数','图书详细链接']
        self.rows = []
        self.page = 0
        
    def get_bookinfo(self, host):
        print('现开始抓取豆瓣图书Top250的数据：')
        while self.page <= 225:
            print('现抓取第%d页'% (self.page/25+1))
            page_url = host + '?start=' + str(self.page)
            self.handle_html(page_url)
            self.page += 25
        self.write_csv(self.rows)
        print('抓取完成！')
            
    def handle_html(self,url):
        headers = {'Host':'book.douban.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        html = requests.get(url, headers=headers)
        content = BeautifulSoup(html.text, 'lxml')
        
        for book in content.find_all('td', valign='top'):
            if book.find('div',{'class':re.compile(r'pl[2]{1}')})==None:
                continue
            bookUrl = book.a['href'].strip()
            title = '《' + book.a['title'].strip()+'》'
            detail = book.find('p', class_='pl').get_text().split('/')
            author = detail[0].strip()
            if len(detail) == 5:
                translator = detail[1].strip()
                press = detail[2].strip()
                date = detail[3].strip()
                price = detail[4].strip()
            else:
                translator = ''
                press = detail[1].strip()
                date = detail[2].strip()
                price = detail[3].strip()
            mark = book.find('span', class_='rating_nums').get_text().strip()
            people = book.find('span', class_='pl').get_text().strip('(').strip(')').strip()
            if book.find('span', class_='inq') == None:
                quote = ''
            else:
                quote = book.find('span', class_='inq').get_text().strip()
            values = [title,author,quote,press,date,price,mark,people,bookUrl]
            dic = dict(zip(self.head,values))
            self.rows.append(dic)
            
    def write_csv(self,rows):
        with codecs.open('DoubanBooks.csv','w','utf_8_sig') as f:
            writer=csv.DictWriter(f,self.head)
            writer.writeheader()
            writer.writerows(rows)

DoubanBook_top250().get_bookinfo(url)
