from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time
import datetime

def minus_check(data):

	if data.em is None:
		temp = re.sub("[\s,]", "", data.contents[0]).replace(u"\xa0", u"")

		if temp == "-" or temp == "":
			return None
		else:
			return int(temp)
	else:
		return int(re.sub("[\s,]", "", data.em.contents[0]))


count = 0
today = datetime.date.today()
save_address = r"C:\Users\라성\Desktop\jongmoks_"


upjong_list = urlopen("http://finance.naver.com/sise/sise_group.nhn?type=upjong").read()
upjong_url = BeautifulSoup(upjong_list, "html.parser").find_all(style="padding-left:10px;")

for i in range(0, len(upjong_url)):

	if upjong_url[i].a.contents[0] == "기타":
		time.sleep(0.3)
		continue

	jongmok_list = urlopen("http://finance.naver.com" + upjong_url[i].a.get("href")).read()
	jongmok_url = BeautifulSoup(jongmok_list, "html.parser").find_all("table")[3].find_all("tr")

	f = open(save_address + str(today.year) + "_" + str(today.month) + "_" + str(today.day) + ".txt", "a")
	f.write("-----" + upjong_url[i].a.contents[0] + "-----\n")
	f.close()

	time.sleep(0.3)

	for j in range(0, len(jongmok_url)-4):

		try:
			jongmok_page = urlopen("http://finance.naver.com" + jongmok_url[2+j].a.get("href")).read()
			jongmok_data = BeautifulSoup(jongmok_page, "html.parser").find("div", class_="section cop_analysis").tbody.find_all("td")

			if len(jongmok_data) == 1:
				continue

			a = minus_check(jongmok_data[0])
			b = minus_check(jongmok_data[1])
			c = minus_check(jongmok_data[2])
			d = minus_check(jongmok_data[10])
			e = minus_check(jongmok_data[11])
			f = minus_check(jongmok_data[12])
			g = minus_check(jongmok_data[20])
			h = minus_check(jongmok_data[21])
			i = minus_check(jongmok_data[22])

			if a != None and b != None and c != None and d != None and e != None and f != None and g != None and h != None and i != None:

				if a < b and b < c and d < e and e < f and g < h and h < i:
					f = open(save_address + str(today.year) + "_" + str(today.month) + "_" + str(today.day) + ".txt", "a")
					f.write(BeautifulSoup(jongmok_page, "html.parser").find("h2").a.contents[0] + "\n")
					f.close()

		except:
			print(BeautifulSoup(jongmok_page, "html.parser").find("h2").a.contents[0] + "error!!!!!!!!")

		time.sleep(0.3)
		count += 1

f = open(save_address + str(today.year) + "_" + str(today.month)  + "_" + str(today.day) + ".txt", "a")
f.write(str(count) + " counted")
f.close()
