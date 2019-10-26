#-*- coding:utf-8 -*-
import pandas as pd
from copy import deepcopy
from numpy import math
import openpyxl
import datetime



# 최근 분기 실적.4 data is our needed data. Data of the most recent date
RECENT_QUATER_DATA = u'최근 분기 실적.4'

# html에 있는 정보를 읽어온다.
# header = 0 으로 맨 윗줄의 데이터를 헤더로 사용하고 얻은 자료를 리스트 형태로 이용하기 위해 뒤에 [0] 을 붙여준다.
code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0, encoding='euc-kr')[0]

# 타입을 확인
print(type(code_df))  # <class 'pandas.core.frame.DataFrame'>


# code_df에 있는 '종목코드' 컬럼을 0을 채운 6자리 포멧으로 맞춰준다.
code_df[u'종목코드'] = code_df[u'종목코드'].map('{:06d}'.format)

# code_df를 회사명과 종목코드 컬럼만 뽑아낸다.
#    ***참고*** pandas에서 컬럼을 선택 할 때
#                   단일개 선택: df['컬럼명']   or   df.컬럼명
#                   여러개 선택: df[['컬럼명', ... ,'컬럼명']]
code_df = code_df[[u'회사명', u'종목코드']]

print(code_df)

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={u'회사명': 'name', u'종목코드': 'code'})


data_list = []
# 크롤링
#for i in range(0, 10):
for i in range(0, len(code_df)):
    name = code_df['name'].get(i)
    code = code_df['code'].get(i)
    #print(name)
    url = 'https://finance.naver.com/item/main.nhn?code={code}'.format(code = code)
    html_data = pd.read_html(url, header = 0, encoding='euc-kr')
    if html_data is None:
        print(name, ' pd.read_html() is None')
        continue

    # [3] index is company's financial data.
    df = html_data[3]
    if df is None:
        print(name, ' html_data[] is None')
        continue
    if df.get(RECENT_QUATER_DATA) is None:
        print(name, ' 최근 분기 실적 is None')
        continue

    # ROE is 7th index and PER is 12th index.
    if df.get(RECENT_QUATER_DATA).get(7) is None:
        print(name, ' ROE is None')
        continue 
    #else:
    #    print(df.get(RECENT_QUATER_DATA).get(7))
    if df.get(RECENT_QUATER_DATA).get(12) is None:
        print(name, ' PER is None')
        continue      
    #else:
    #    print(df.get(RECENT_QUATER_DATA).get(12))
    if math.isnan(float(df.get(RECENT_QUATER_DATA).get(7))):
        print(name, ' ROE is nan')
        continue
    #else:
    #    print(df.get(RECENT_QUATER_DATA).get(7))
    if math.isnan(float(df.get(RECENT_QUATER_DATA).get(12))):
        print(name, ' PER is nan')
        continue
    #else:
    #   print(df.get(RECENT_QUATER_DATA).get(7))

    ROE = float(df.get(RECENT_QUATER_DATA).get(7))
    PER = float(df.get(RECENT_QUATER_DATA).get(12))

    if ROE < 5:
        print(name, ' PER value is out of range')
        continue
    if PER < 0 or PER > 50:
        print(name, ' PER value is out of range')
        continue

    data_list.append([ 
        str(i)+'/'+str(len(code_df)-1), 
        name, 
        code, 
        ROE, 
        PER,
        0, # ROE rank
        0, # PER rank
        0  # Total score
    ])
    print(data_list[-1])
    #print(df)

# sort by ROE
data_list = sorted(data_list, key = lambda x: float(x[3]), reverse = True)

# set ROE rank
for i in range(0, len(data_list)):
    data_list[i][5] = i 

# sort by PER
data_list = sorted(data_list, key = lambda x: float(x[4]), reverse = False)

# set PER rank
for i in range(0, len(data_list)):
    data_list[i][6] = i 

# sum rank of ROE and PER
for i in range(0, len(data_list)):
    data_list[i][7] = data_list[i][5] + data_list[i][6]

# sort by Total score
data_list = sorted(data_list, key = lambda x: float(x[7]), reverse = False)
print(data_list)

# change data type for pandas DataFrame
date_for_dataframe = {
    'name' : [],
    'code' : [],
    'ROE' : [],
    'PER' : [],
    'ROE rank' : [],
    'PER rank' : [],
    'Total score' : []  
}

i=0
for key in date_for_dataframe:
    i+=1
    if i >= len(data_list[0]):
        print('i value is out of range')
    for j in range(0, len(data_list)):
        date_for_dataframe[key].append(data_list[j][i])

result = pd.DataFrame(date_for_dataframe)
print(result)

result.to_excel('REO_PER_rank_' + str(datetime.date.today()) + '.xlsx', sheet_name='REO_PER_rank')






