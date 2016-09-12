from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time
import datetime


####################################              class and function           #####################################


class Finance:
	jongmok_count = 0
	
	def find_upjonglist(self):
		time.sleep(0.3)
		upjong_listhtml = urlopen("http://finance.naver.com/sise/sise_group.nhn?type=upjong").read()
		upjong_list = BeautifulSoup(upjong_listhtml, "html.parser").find_all(style="padding-left:10px;")
		return upjong_list
	
	def find_jongmoklist(self, upjong_url):
		time.sleep(0.3)
		jongmok_listhtml = urlopen("http://finance.naver.com" + upjong_url).read()
		jongmok_list = BeautifulSoup(jongmok_listhtml, "html.parser").find_all("table")[3].find_all("tr")
		return jongmok_list
		
	def save_upjongName(self, filename, upjong_name):
		f = open(filename, "a")
		f.write("-----" + upjong_name + "-----\n")
		f.close()
	
	def save_jongmokName(self, filename, jongmok):
		f = open(filename, "a")
		f.write(jongmok + "\n")
		f.close()
		
	def save_count(self, filename):
		f = open(filename, "a")
		f.write(str(self.count) + " counted")
		f.close()
	
	def check_minus(self, data):
		if data.em is None:
			temp = re.sub("[\s,]", "", data.contents[0]).replace(u"\xa0", u"")

			if temp == "-" or temp == "":
				return None
			else:
				return int(temp)
		else:
			return int(re.sub("[\s,]", "", data.em.contents[0]))
			
	def add_jongmok_count(self):
		self.jongmok_count += 1


	
#########################################           end class and functions           ##########################################
	
today = datetime.date.today()
save_path = r"C:\Users\rlxotjr\Desktop\jongmoks_"
save_filename = save_path + str(today.year) + "_" + str(today.month)  + "_" + str(today.day) + ".txt"

finance = Finance()
upjong_list = finance.find_upjonglist()

for i in range(0, len(upjong_list)):
	# "기타" jongmoklist is useless. "기타" Jongmok skip.
	if upjong_list[i].a.contents[0] == "기타":
		continue
			
	finance.save_upjongName(save_filename, upjong_list[i].a.contents[0])
	jongmok_list = finance.find_jongmoklist(upjong_list[i].a.get("href"))

	for j in range(0, len(jongmok_list)-4):

		try:
			# time delay is to prevent server's connection close. Because of so fast connections
			time.sleep(0.3)
			jongmok_page = urlopen("http://finance.naver.com" + jongmok_list[2+j].a.get("href")).read()
			jongmok_data = BeautifulSoup(jongmok_page, "html.parser").find("div", class_="section cop_analysis").tbody.find_all("td")
			
			if len(jongmok_data) == 1:
				continue
				
			data1 = finance.check_minus(jongmok_data[0])
			if data1 == None: 
				continue
			data2 = finance.check_minus(jongmok_data[1])
			if data2 == None: 
				continue
			data3 = finance.check_minus(jongmok_data[2])
			if data3 == None: 
				continue
			data4 = finance.check_minus(jongmok_data[10])
			if data4 == None: 
				continue
			data5 = finance.check_minus(jongmok_data[11])
			if data5 == None: 
				continue
			data6 = finance.check_minus(jongmok_data[12])
			if data6 == None: 
				continue
			data7 = finance.check_minus(jongmok_data[20])
			if data7 == None: 
				continue
			data8 = finance.check_minus(jongmok_data[21])
			if data8 == None: 
				continue
			data9 = finance.check_minus(jongmok_data[22])
			if data9 == None: 
				continue
			
			if data1 < data2 and data2 < data3 and data4 < data5 and data5 < data6 and data7 < data8 and data8 < data9:
				finance.save_jongmokName(save_filename, BeautifulSoup(jongmok_page, "html.parser").find("h2").a.contents[0])
				
		except:
			print(BeautifulSoup(jongmok_page, "html.parser").find("h2").a.contents[0] + "error!!!!!!!!")
			
		finance.add_jongmok_count()
		
finance.save_count(save_filename)	



	

	
	
	
	
	
	
	
