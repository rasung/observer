#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from requests import get
import re
import time
import datetime
import os

ROE = 58
PER = 108



class Parser:
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        year = str(datetime.date.today().year)
        month = str(datetime.date.today().month)
        day = str(datetime.date.today().day)
        file = path + "\jongmoks_" + year + "_" + month  + "_" + day + ".txt"
        self.f = open(file, 'w', -1, "utf-8")
        self.count = 0

    def __del__(self):
        self.f.write(str(self.count) + " counted")
        self.f.close()

    # 1. parse upjong list
    def __parseUpjongList__(self, url):
        html = get(url)
        data = BeautifulSoup(html.content.decode('euc-kr','replace')).find_all(style="padding-left:10px;")
        
        # "기타" upjong is useless.
        data = list(filter(lambda x : x.a.contents[0] != "기타", data))

        # save [upjongName, upjongURL] list
        upjongList = list(map(lambda x : [x.a.contents[0], "http://finance.naver.com" + x.a.get("href")], data))
        
        return upjongList

    # 2. parse jongmok list
    def __parseJongmokList__(self, upjongList):
        data = []
        for i in range(len(upjongList)):
            # save upjongName
            data.append([i, upjongList[i][0]])

            # time delay is to prevent server's connection close. Because of so fast connections
            time.sleep(0.2)

            jongmokListHtml = get(upjongList[i][1])
            jongmokList = BeautifulSoup(jongmokListHtml.content.decode('euc-kr','replace')).find_all("table")[3].find_all("tr")
            # Todo 2 -> 1 , 3
            jongmokList = jongmokList[2:len(jongmokList)-2]
            data += list(map(lambda x : "http://finance.naver.com" + x.a.get("href"), jongmokList))

            print("__parseJongmokList__" + str(i+1) + "/" + str(len(upjongList)))

        return data

    # 3. parse jongmok data
    def __parseJongmokData__(self, jongmokList):
        for i in range(len(jongmokList)):
            self.count += 1

            # write upjongName
            if len(jongmokList[i]) is 2:
                #print(jongmokList[i][1].encode('euc-kr', 'ignore').decode('utf-8', 'ignore'))
                self.f.write("-----" + jongmokList[i][1] + "-----\n")
                continue

            # time delay is to prevent server's connection close. Because of so fast connections
            #time.sleep(0.2)
            
            jongmokHtml = get(jongmokList[i])
            jongmokData = BeautifulSoup(jongmokHtml.content.decode('euc-kr','replace')).find("div", class_="section cop_analysis").tbody.find_all("td")
            jongmokName = BeautifulSoup(jongmokHtml.content.decode('euc-kr','replace')).find("div", class_="wrap_company").h2.a.contents[0]
            print(jongmokName)
            print(jongmokName.encode('utf-8'))


            try:
                # 3. verify jongmok data
                if self.__isVerified__(jongmokData) is True:
                    self.f.write(jongmokName + "\n")
            except:
                print(jongmokName + "error!!!!!!!!")
            
            print("__parseJongmokData__" + str(i) + "/" + str(len(jongmokList)))


    def __isVerified__(self, jongmokData):

        if len(jongmokData) == 1:
            return False

        roe = self.__stringToint__(jongmokData[ROE])
        roe_pred = self.__stringToint__(jongmokData[ROE+1])
        per = self.__stringToint__(jongmokData[PER])
        per_pred = self.__stringToint__(jongmokData[PER+1])

        if roe is None and per is None:
            return False

        if roe < 0 :
            return False

        if roe_pred is not None:
            roe = (roe_pred + roe) / 2

        if per_pred is not None:
            per = (per_pred + per) / 2

        print(int(roe))
        print(int(per))  
   
        return True

    # Plus and minus string value change to int 
    def __stringToint__(self, data):
        if data.em is None:
            temp = re.sub("[\s,]", "", data.contents[0]).replace(u"\xa0", u"")
            if temp == "-" or temp == "":
                return None
            else:
                return int(temp)
        else:
            return int(re.sub("[\s,]", "", data.em.contents[0]))

    def parse(self):
        upjongList = self.__parseUpjongList__("http://finance.naver.com/sise/sise_group.nhn?type=upjong")
        jongmokList = self.__parseJongmokList__(upjongList)
        self.__parseJongmokData__(jongmokList)




parser = Parser()
parser.parse()

