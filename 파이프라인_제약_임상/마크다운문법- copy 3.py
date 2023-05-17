import pandas as pd
import yaml
import markdown
from pykrx import stock
import plotly.graph_objects as go
import re,os,sys

import matplotlib.pyplot as plt
import pprint as pp
import streamlit.components.v1 as components
#dataframe 전체를 보여주기 위한 설정
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', 90)
#pd.set_option('display.width', None)

G_stockInfo_DF = pd.read_csv("/Users/hg/WORKSPACE/Gitblog/stock/chart/data/csv/stockTicker.csv")
class mk_box():
    def __init__(self):
        self.pathdf = "path"
        self.fnameaf = ""
    def readNewsJsonRawfile(self,fname):
        df = pd.read_json(f"/Users/hg/WORKSPACE/Gitblog/naver/src/data/json/{fname}/{fname}.json")
        # df.columns =[ 'title', 'newstext', 'summary', 'gentime', 'img', 'link', 'companytag', 'imagelist']
        df = df[['title', 'newstext', 'gentime', 'companytag','link']]
        df.transpose()
        df = df.sort_values(by=['gentime'], axis=0, ascending=False)
        df = df.reset_index(drop=True)
        df = df.drop_duplicates(['title'], keep='first')
        df = df.reset_index(drop=True)
        return df

    def mk_제목모음(self,titleStr,fname,linkStr):
        lists = []
        for idx,var in enumerate(titleStr):
            #fa = f":fontawesome-regular-face-laugh-wink: [{var}]({linkStr[idx]}) <br>"
            fa = f"[{var}]({linkStr[idx]}) <br>"
            lists.append(fa)
        linkStr = "".join(lists)# <br>로 마크다운 줄바꿈
    # [`abstract`](#type:abstract){{ #type:abstract }}

        제목모음= f'''
!!! abstract "Readable News"
    <h3 style="color:black; background-color: ; ">{linkStr} </h3>
            '''
        return 제목모음
    

    def mk_기사본문_접어두기(self,title,newstext,mainsentence,회사를포함한문장):
    # [`mk_기사본문_접어두기`](#type:mk_기사본문_접어두기){{ #type:mk_기사본문_접어두기 }}
        기사= f'''
## {title}
??? mk_기사본문_접어두기 "{title}"
    
    - ==검색어==  
    - ^^관련회사^^  
    - ~~쓸데없는정보~~  
    {mainsentence}
    {회사를포함한문장}
    {newstext}  
    [{title}]: https://github.com/jimporter/mike#why-use-mike
            '''
        return 기사
    def mk_기사본문_주요문장(self,title,newstext,mainsentence,회사를포함한문장,fname):
    # [`mk_기사본문_주요문장`](#type:mk_기사본문_주요문장){{ #type:mk_기사본문_주요문장 }}
        기사= f'''
### Search-sentence
!!! mk_기사본문_주요문장 "{title}"
    

    <h2 style="color:black; background-color: ;"> {fname}  </h2>
    {mainsentence}
    {회사를포함한문장}
    {newstext}  
    [{title}]: https://github.com/jimporter/mike#why-use-mike
            '''
        return 기사
    def mk_기사본문_회사포함(self,title,newstext,mainsentence,회사를포함한문장,ct):
    # [`mk_기사본문_회사포함`](#type:mk_기사본문_회사포함){{ #type:mk_기사본문_회사포함 }}
        기사= f'''
### Company-sentence
!!! mk_기사본문_회사포함 "{title}"
    
    
    { ct }  
    {mainsentence}
    {회사를포함한문장}
    {newstext}  
    [{title}]: https://github.com/jimporter/mike#why-use-mike

            '''
        return 기사
    def mk_관련회사테그(self,ct):
        #ct리스트에서 특수문자 제거
    
        
    # [`note`](#type:note){{ #type:note }}
        관련회사테그= f'''   
### Company-tag
!!! note "관련회사테그 링크 네이버"
    {ct}  
        '''
        return 관련회사테그


    def mk_아이콘(self,iconname):
        리드라인아이콘= f'''
[:octicons-heart-fill-24:{{ .mdx-heart }} {iconname} 리드라인 기사][Insiders]{{ .mdx-insiders }} ·
[:octicons-tag-24: insiders-4.12.0][Insiders] ·
:octicons-beaker-24: Experimental
[Insiders]: ../readme.md
[list]: #list-syntax
[block syntax]: #block-syntax
            '''
        return 리드라인아이콘



    def 링크_회사태그(self,comtag):
        listss = []
        if len(comtag) == 0:
            #html 관련회사 없음

            taf = "관련회사가 없습니다."
            taf = f"<font color='red'>{taf}</font>"

            return taf
        else:
            
            for cname in comtag:
                cname.strip()
                code=self.find_code(cname)
                url = f"https://finance.naver.com/item/main.nhn?code={code}"
                listss.append(f" [{cname}]({url})  ")
            listss=" ".join(listss)
            return listss
    def 링크_회사문장(self,comtag):
        listss = []
        if len(comtag) == 0:
            
            return []
        else:
            
            for cname in comtag:
                cname.strip()
                code=self.find_code(cname)
                url = f"https://finance.naver.com/item/main.nhn?code={code}"
                listss.append(f" [{cname}]({url}) ")
            listss=" ".join(listss)
            return listss
    def 마크다운exm(self,path,fname):
        기사 =""
        기사 = ""
        관련회사테그 = ""
        리드라인아이콘 = ""
        ## 처음에

        df=self.readNewsJsonRawfile(fname)
        
        # 제목리스트
        # title , 생성시간합쳐서 출력
        # "2023-03-19T02:55:36.000Z" 컬럼에서 문자기준 스플릿
        df['grp'] = df.gentime.str.split('T').str[0]
        df['ti+gen'] = df['title'] +" <b>"+df['grp']
        # titleStr = "<br>".join(df['ti+gen'].to_list())# <br>로 마크다운 줄바꿈
        # linkStr = "<br>".join(df['link'].to_list())# <br>로 마크다운 줄바꿈
        titlelist = df['ti+gen'].to_list()# <br>로 마크다운 줄바꿈
        linklist = df['link'].to_list()# <br>로 마크다운 줄바꿈


        제목모음=self.mk_제목모음(titlelist,fname,linklist)

        with open(f"/Users/hg/WORKSPACE/Gitblog/mkdocs-material/docs/md/posts/{fname}.md", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(제목모음)
        for idx, (title, newstext, gentime, companytag) in enumerate(df[['title', 'newstext', 'gentime', 'companytag']].values):
            # 기사내용
            ctList = list(companytag.keys())
            ct = ",".join(ctList).replace("#","")
            comtag =  ct.split(",")
            newstext,주요문장,회사를포함한문장=self.mk_문장분석(newstext,comtag,fname)
            
            리드라인아이콘=self.mk_아이콘(f"{idx}-번째")
            기사=self.mk_기사본문_접어두기(title,newstext,"","")
            기사중심문장=self.mk_기사본문_주요문장("주요문장","",주요문장,"",fname)
            # 다이아그램=flowcharts_diagram(newstext)
            회사를포함한문장=self.mk_기사본문_회사포함("회사를포함한문장","","",회사를포함한문장,self.링크_회사문장(comtag))
            #관련회사테그=mk_관련회사테그(링크_회사태그(comtag))

            구분선="---"
            with open(f'/Users/hg/WORKSPACE/Gitblog/mkdocs-material/docs/md/posts/{fname}.md', "a", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
                output_file.write(리드라인아이콘+기사+기사중심문장+회사를포함한문장+'\n\n'+ 구분선)

    def flowcharts_diagram(self,df):
        
        dia = f'''

        '''
        return dia


    def mf_tag(self,i):
        # t = f''':octicons-heart-fill-24:{{ .mdx-heart }}'''
        t = f''' =={i}== '''
        return t
    # G_stockInfo_DF 종목이름으로 종목코드 찾기
    def find_code(self,name):
        if name != "" or name != None or name != "n":
            code = ""
            try :
                code = G_stockInfo_DF[G_stockInfo_DF['종목명'] == name]['종목코드'].values[0]
            except:
                pass

            return code
        else:
            return ""
    def mk_문장분석(self,text_p,comtag,serchword):
        # - ==검색어==  
        # - ^^관련회사^^  
        # - ~~쓸데없는정보~~  
        # [`mark`][mark], [`ins`][ins] and [`del`][del] HTML tags: 
        # yellow = f"=={text}=="
        # underlin = f"^^{text}^^"
        # delete = f"~~{text}~~"
        # angker = f"`{text}`"
        ser = serchword.split("_")
        # text를 .으로 구분하여 리스트로 만들고 datafrmae으로 만들어서 serchword가 포함된 행을 찾아서 yellow로 치환
        text=text_p.replace('다.','다. \n ')#마침표로 끝나야 문장, 1.3% 같은게 있음
        text = text.split("\n")
        df = pd.DataFrame(text)
        df.columns = ["text"]
        # df 에서 serchword가 포함된 단어를 찾아서 yellow로 치환
        searlists= []
        comlists =[]

            # sedf 에 serchword가 포함된 단어를 찾아서 yellow로 치환
        st = pd.DataFrame()
        dfstr = ""
        if ser != ['']:
            serchwordcom ="|".join(ser)
            sedf = df[df['text'].str.contains(serchwordcom)]
            st = pd.DataFrame()
            for i in ser:
                # (.*)li(.*)', r'\1LI\2
                # 경고(SettingWithCopyWarning 발생, 기본 값입니다) 
                pd.set_option('mode.chained_assignment',None) # 
                st['text'] = sedf['text'].str.replace(i, f" =={i}== ")
                sedf = st
            st = sedf
            # searlists = st['text'].to_list()

            

        tc = pd.DataFrame()
        dfstr = ""
        if len(comtag)>=1 and comtag[0] != "":
            # print(comtag)
            tagCom ="|".join(comtag)
            tcdf = df[df['text'].str.contains(tagCom)]
            for i in comtag:
                pd.set_option('mode.chained_assignment',None) # 
                tc['text'] = tcdf['text'].str.replace(i, f"' =={i}== '")
                tcdf = tc
        
            tc = tcdf
        
        print(tc)

        검색어를포함한문장 = "<p> ".join(st["text"].to_list())# <br>로 마크다운 줄바꿈
        검색어를포함한문장.replace("이미지","")
        if len(tc)>0:
            
            회사를포함한문장 = "<p> ".join(tc["text"].to_list())# <br>로 마크다운 줄바꿈
        else:
            회사를포함한문장 = "관련회사가 없습니다."
            회사를포함한문장 = f"<font color='red'>{회사를포함한문장}</font>"

        text_p=text_p.replace("다.","다. <p>")
        return text_p, 검색어를포함한문장,회사를포함한문장
mk_box().마크다운exm("path",fname="영업이익_sk이노베이션_실적")
    
# find_code("삼성전자")



