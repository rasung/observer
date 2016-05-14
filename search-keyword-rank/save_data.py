from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymysql
import sys
import time
import re

init_url = "/main/ranking/searchWeek.nhn?rankingType=search_week&date=20050615"
next_url = init_url

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='xotjr', db='keyword_rank', charset ='utf8')
cur = conn.cursor()

while next_url != None:
    page = urlopen("http://news.naver.com" + next_url).read()
    soup = BeautifulSoup(page, "html.parser")

    keywords = soup.find("div", class_="ranking_keyword").find_all("div")

    date = re.compile("........$").search(next_url).group()
    print(date)

    cur.execute("INSERT INTO naver(date) VALUES(" + "'" + str(date) + "'" + ");")
    conn.commit()

    for i in range(len(keywords)):
        cur.execute("UPDATE naver SET _" + str(i+1) + "= '" + re.sub("[\'\"]", "", keywords[i].a.contents[0]) + "'" + "WHERE date = '" + str(date) + "';")
        conn.commit()

    next_url = soup.find("div", class_="calendar_date").find_all("a")[1].get("href")
