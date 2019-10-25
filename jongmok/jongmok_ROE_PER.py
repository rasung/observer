#-*- coding:utf-8 -*-
import pandas as pd

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
# 크롤링.
#for i in range(0, len(code_df)):
for i in range(0, 20):
    name = code_df['name'].get(i)
    code = code_df['code'].get(i)
    url = 'https://finance.naver.com/item/main.nhn?code={code}'.format(code = code)
    df = pd.read_html(url, header = 0, encoding='euc-kr')[3]    

    ROE = float(df.get(u'최근 분기 실적.4').get(7))
    PER = float(df.get(u'최근 분기 실적.4').get(12))

    data_list.append({'index' : i, 'name' : name, 'code': code, 'ROE' : ROE, 'PER' : PER})
    print('index : ', i, 'name : ', name, 'code : ', code, 'ROE : ', ROE, 'PER : ', PER)

    #print(a)






