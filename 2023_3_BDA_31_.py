#!/usr/bin/env python
# coding: utf-8

# In[1]:


#개발 환경: Windows 10
#라이브러리 버전: pandas -> 2.1.1 / numpy -> 1.26.0 /  matplotlib -> 3.8.0 / seaborn -> 0.13.0
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

font_path = "C:/Windows/Fonts/malgun.ttf"  
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
pd.set_option('mode.chained_assignment', None)

# #### 상권별 유동인구 데이터

# In[2]:


df_people = pd.read_csv('서울시 상권분석서비스(길단위인구-상권).csv', encoding='euc-kr')
df_people = df_people[df_people['기준_년분기_코드'] == 20224]
df_people = df_people[['기준_년분기_코드', '상권_코드', '상권_코드_명', '총_유동인구_수']]
df_people

# #### 상권별 매출 데이터

# In[3]:


df_sales = pd.read_csv('서울시_상권분석서비스(추정매출-상권)_2022년.csv', encoding='euc-kr')
df_sales = df_sales[df_sales['상권_구분_코드_명'] == '골목상권']
df_sales = df_sales[df_sales['기준_년분기_코드'] == 20224]
df_sales = df_sales[['기준_년분기_코드', '상권_코드', '상권_코드_명', '당월_매출_금액']]
df_sales

# #### 상권별 유동인구,  매출 데이터 정리

# In[4]:


df_ps = pd.merge(df_people, df_sales, on=['기준_년분기_코드', '상권_코드', '상권_코드_명'])
pd.options.display.float_format = '{:.0f}'.format
df_ps = df_ps.groupby(['기준_년분기_코드', '상권_코드', '상권_코드_명', '총_유동인구_수'])['당월_매출_금액'].sum()
df_ps = df_ps.reset_index()
df_ps

# #### 유동인구 수 상위 75% 이상, 매출 하위 25% 이하인 상권 정리

# In[5]:


cri_people = df_ps['총_유동인구_수'].quantile(0.75)
cri_sales = df_ps['당월_매출_금액'].quantile(0.25)
find_place = []
for idx in df_ps.index:
    if df_ps['총_유동인구_수'][idx] >= cri_people and df_ps['당월_매출_금액'][idx] <= cri_sales:
        find_place.append(idx)
df_place = df_ps.loc[find_place]
df_place

# #### 직장 인구수 데이터를 추가하고, 직장 인구수 기준으로 상권 정렬

# In[6]:


df_jobpeople = pd.read_csv('서울시 상권분석서비스(직장인구-상권).csv', encoding='euc-kr')
df_jobpeople = df_jobpeople[df_jobpeople['기준_년분기_코드'] == 20224]
df_jobpeople = df_jobpeople[df_jobpeople['상권_구분_코드_명'] == '골목상권']
df_jobpeople = df_jobpeople[['기준_년분기_코드', '상권_코드', '상권_코드_명', '총_직장_인구_수']]
df_psj = pd.merge(df_place, df_jobpeople, on=['기준_년분기_코드', '상권_코드', '상권_코드_명'])
df_psj.sort_values('총_직장_인구_수', ascending=False)

# #### 도림초등학교 상권 연령대 데이터 시각화

# In[7]:


df_dorim_age = pd.read_csv('서울시 상권분석서비스(길단위인구-상권).csv', encoding='euc-kr')
df_dorim_age = df_dorim_age[df_dorim_age['상권_코드_명'] == '도림초등학교']
df_dorim_age = df_dorim_age[df_dorim_age['기준_년분기_코드'] == 20224]
df_dorim_age = df_dorim_age[['연령대_10_유동인구_수', '연령대_20_유동인구_수', '연령대_30_유동인구_수', 
'연령대_40_유동인구_수', '연령대_50_유동인구_수', '연령대_60_이상_유동인구_수']]
bar_dorim_age = {
    'age' : ['10대', '20대', '30대', '40대', '50대', '60대 이상'],
    'num' : df_dorim_age.values[0]
}
df_dorim_age = pd.DataFrame(bar_dorim_age)
sns.barplot(x='age', y='num', data=df_dorim_age)
plt.ticklabel_format(axis='y',useOffset=False, style='plain')

# #### 도림초등학교 상권 추정소비 데이터 시각화

# In[8]:


df_dorim_consume = pd.read_csv('서울시 상권분석서비스(소득소비-상권배후지).csv', encoding='euc-kr')
df_dorim_consume = df_dorim_consume[df_dorim_consume['기준_년분기_코드'] == 20224]
df_dorim_consume = df_dorim_consume[df_dorim_consume['상권_코드_명'] == '도림초등학교']
df_dorim_consume = df_dorim_consume[['식료품_지출_총금액', '의류_신발_지출_총금액', '생활용품_지출_총금액', '의료비_지출_총금액', '교통_지출_총금액', '여가_지출_총금액', '문화_지출_총금액', '교육_지출_총금액', '유흥_지출_총금액']]
bar_dorim_consume = {
    'category': ['식료품', '의류', '생활용품', '의료비', '교통', '여가', '문화', '교육', '유흥'],
    'won' : df_dorim_consume.values[0]
}
df_dorim_consume = pd.DataFrame(bar_dorim_consume)
sns.barplot(x='category', y='won', data=df_dorim_consume)
plt.ticklabel_format(axis='y',useOffset=False, style='plain')

# #### 서울시 전체 유동인구 데이터

# In[9]:


df_seoulpeople = pd.read_csv("서울시 상권분석서비스(길단위인구-자치구).csv", encoding='euc-kr')

# #### 상권 코드 데이터

# In[10]:


df_code = pd.read_csv("서울시 상권분석서비스(상권영역).csv", encoding="euc-kr")
df_code = df_code.rename(columns={'시군구_코드': '자치구_코드'})

# #### 유동인구 & 상권 코드 데이터 결합

# In[11]:


df_join1 = pd.merge(df_seoulpeople, df_code, on="자치구_코드")

# #### 자치구 코드 데이터

# In[12]:


df_district = pd.read_csv("서울시 건축물대장 법정동 코드정보.csv", encoding='euc-kr')
df_district = df_district.rename(columns={'시군구코드': '자치구코드', '시군구명': '자치구명'})
df_district = df_district[["자치구코드", "자치구명"]].drop_duplicates('자치구코드', keep='first')

# In[13]:


df_join2 = pd.merge(df_join1, df_district, left_on="자치구_코드", right_on="자치구코드")
df_join2["구"] = [gu[:2] if len(gu)<=3 else gu[:3] for gu in df_join2['자치구명']]

# In[14]:


subset = df_join2[df_join2['기준_년분기_코드'] == 20224]
subset

# #### 요일별 유동인구 데이터 시각화

# In[15]:


df_daypeople = df_join2[['구', '월요일_유동인구_수','화요일_유동인구_수','수요일_유동인구_수','목요일_유동인구_수','금요일_유동인구_수','토요일_유동인구_수','일요일_유동인구_수']]
df_daypeople = df_daypeople.groupby('구').mean().round()
df_daypeople.columns = ['월','화','수','목','금','토','일']
fig, ax = plt.subplots(figsize=(15, 9))
sns.lineplot(data=df_daypeople.T, palette="tab10", linewidth=2.5, dashes=False, sort=False).set_title("요일별 상권 유동인구 수")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax.set(xlabel="요일", ylabel = "평균 유동인구 수")
plt.show()
fig.savefig("구&요일별 유동인구.png", dpi=200)

# #### 매출액 데이터

# In[16]:


df_districtsale = pd.read_csv("서울시 상권분석서비스(추정매출-자치구).csv", encoding='euc-kr')
df_districtsale = df_districtsale[['기준_년분기_코드', '자치구_코드', '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액']]
df_districtsale = df_districtsale[(df_districtsale['기준_년분기_코드'] == 20224) & ((df_districtsale['자치구_코드'] == 11680) | (df_districtsale['자치구_코드'] == 11560))]

# #### 요일별 매출 금액 비교 데이터 시각화

# In[17]:


# 데이터 분리
gangnam = df_districtsale[df_districtsale['자치구_코드'] == 11680]
yeongdeungpo = df_districtsale[df_districtsale['자치구_코드'] == 11560]

# 요일별 매출액의 합계
gangnam_sales = [gangnam['월요일_매출_금액'].sum(),
                 gangnam['화요일_매출_금액'].sum(),
                 gangnam['수요일_매출_금액'].sum(),
                 gangnam['목요일_매출_금액'].sum(),
                 gangnam['금요일_매출_금액'].sum(),
                 gangnam['토요일_매출_금액'].sum(),
                 gangnam['일요일_매출_금액'].sum()]

yeongdeungpo_sales = [yeongdeungpo['월요일_매출_금액'].sum(),
                      yeongdeungpo['화요일_매출_금액'].sum(),
                      yeongdeungpo['수요일_매출_금액'].sum(),
                      yeongdeungpo['목요일_매출_금액'].sum(),
                      yeongdeungpo['금요일_매출_금액'].sum(),
                      yeongdeungpo['토요일_매출_금액'].sum(),
                      yeongdeungpo['일요일_매출_금액'].sum()]

days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']


plt.figure(figsize=(10, 6))
plt.plot(days, gangnam_sales, marker='o', label='강남구')
plt.plot(days, yeongdeungpo_sales, marker='o', label='영등포구')
plt.title('요일별 매출금액 비교')
plt.xlabel('요일')
plt.ylabel('매출액')
plt.legend()
plt.show()

# In[ ]:



