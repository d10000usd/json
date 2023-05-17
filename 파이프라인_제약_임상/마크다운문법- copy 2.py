import pandas as pd
import yaml
import markdown
from pykrx import stock
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import pprint as pp
import streamlit.components.v1 as components
#dataframe 전체를 보여주기 위한 설정
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', 90)
#pd.set_option('display.width', None)

G_stockInfo_DF = pd.read_csv("/Users/hg/WORKSPACE/Gitblog/stock/chart/data/csv/stockTicker.csv")

def readNewsJsonRawfile(fname):
    
    df = pd.read_json(f"/Users/hg/WORKSPACE/Gitblog/naver/src/data/json/{fname}/{fname}_news_원본.json")
    df.columns =[ 'title', 'newstext', 'summary', 'gentime', 'img', 'link', 'companytag', 'imagelist']
    df = df[['title', 'newstext', 'gentime', 'companytag','link']]
    df.transpose()
    df = df.sort_values(by=['gentime'], axis=0, ascending=False)
    df = df.reset_index(drop=True)
    df = df.drop_duplicates(['title'], keep='first')
    df = df.reset_index(drop=True)


  
    return df

def mk_관련회사테그(ct):
    관련회사테그= f'''   
[`note`](#type:note){{ #type:note }}
!!! note "관련회사테그 링크 네이버"
    {ct} 
    '''
    return 관련회사테그



def mk_기사본문_접어두기(title,newstext,mainsentence,회사를포함한문장):
    기사= f'''
[`mk_기사본문_접어두기`](#type:mk_기사본문_접어두기){{ #type:mk_기사본문_접어두기 }}
??? mk_기사본문_접어두기 "{title}"
    
    [Critic]  
    - ==검색어==  
    - ^^관련회사^^  
    - ~~쓸데없는정보~~  
    {mainsentence}

    {회사를포함한문장}

    {newstext}  
    
    [{title}]: https://github.com/jimporter/mike#why-use-mike

        '''
    return 기사
def mk_기사본문_주요문장(title,newstext,mainsentence,회사를포함한문장,fname):
    기사= f'''
[`mk_기사본문_주요문장`](#type:mk_기사본문_주요문장){{ #type:mk_기사본문_주요문장 }}
!!! mk_기사본문_주요문장 "{title}"
    
    [Critic]  
    - =={fname}==  
    - ^^관련회사^^  
    - ~~쓸데없는정보~~  
    {mainsentence}

    {회사를포함한문장}

    {newstext}  
    
    [{title}]: https://github.com/jimporter/mike#why-use-mike

        '''
    return 기사
def mk_기사본문_회사포함(title,newstext,mainsentence,회사를포함한문장,ct):
    기사= f'''
[`mk_기사본문_회사포함`](#type:mk_기사본문_회사포함){{ #type:mk_기사본문_회사포함 }}
!!! mk_기사본문_회사포함 "{title}"
    
    [Critic]  
    - =={ct}==  
    - ^^관련회사^^  
    - ~~쓸데없는정보~~  
    {mainsentence}

    {회사를포함한문장}

    {newstext}  
    
    [{title}]: https://github.com/jimporter/mike#why-use-mike

        '''
    return 기사
def mk_기사본문(title,newstext,mainsentence,회사를포함한문장):
    기사= f'''
[`mk_기사본문`](#type:mk_기사본문){{ #type:mk_기사본문 }}
!!! mk_기사본문 "{title}"
    
    [Critic]  
    - ==검색어==  
    - ^^관련회사^^  
    - ~~쓸데없는정보~~  
    {mainsentence}

    {회사를포함한문장}

    {newstext}  
    
    [{title}]: https://github.com/jimporter/mike#why-use-mike

        '''
    return 기사
def mk_아이콘(iconname):
    리드라인아이콘= f'''
[:octicons-heart-fill-24:{{ .mdx-heart }} {iconname} 리드라인 기사][Insiders]{{ .mdx-insiders }} ·
[:octicons-tag-24: insiders-4.12.0][Insiders] ·
:octicons-beaker-24: Experimental
[Insiders]: ../readme.md
[list]: #list-syntax
[block syntax]: #block-syntax
        '''
    return 리드라인아이콘
def mk_제목모음(titleStr,fname,linkStr):
    제목모음= f'''
[`abstract`](#type:abstract){{ #type:abstract }}
!!! abstract "Readable News"
    <h3 style="color:black; background-color: ; ">{titleStr} </h3>
    <h4 style="color:green; background-color: ; ">{linkStr} </h2>
        '''
    return 제목모음


def 회사링크만들기(comtag):
    listss = []
    if len(comtag) == 0:
        
        return []
    else:
        
        for cname in comtag:
            cname.strip()
            code=find_code(cname)
            url = f"https://finance.naver.com/item/main.nhn?code={code}"
            listss.append(f"[{cname}]({url})")
        listss=" ".join(listss)
        return listss
def 마크다운exm(path,fname):
    기사 =""
    기사 = ""
    관련회사테그 = ""
    리드라인아이콘 = ""
    ## 처음에

    df=readNewsJsonRawfile(fname)
    df.to_json("/Users/hg/WORKSPACE/Gitblog/naver/src/data/json/바이오_제약_임상/바이오_제약_임상_news_원본_tranpose.json",orient='records',force_ascii=False,indent=4)
    mk_아이콘("첫번째")
    # 제목리스트
    # title , 생성시간합쳐서 출력
    df['ti+gen'] = df['title'] +" <b>"+df['gentime']
    titleStr = "<br>".join(df['ti+gen'].to_list())# <br>로 마크다운 줄바꿈
    linkStr = "<br>".join(df['link'].to_list())# <br>로 마크다운 줄바꿈

    
    


    제목모음=mk_제목모음(titleStr,fname,linkStr)


    with open(f"/Users/hg/WORKSPACE/Gitblog/mkdocs-material/docs/md/posts/{fname}.md", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(제목모음)
    for idx, (title, newstext, gentime, companytag) in enumerate(df[['title', 'newstext', 'gentime', 'companytag']].values):
        # 기사내용
        ctList = list(companytag.keys())
        ct = ",".join(ctList).replace("#","")

        comtag =  ct.split(",")
        
        newstext = newstext.replace('다. ','다. <p>')#마침표로 끝나야 문장, 1.3% 같은게 있음
        
        newstext,주요문장,회사를포함한문장=mk_문장분석(newstext,comtag,fname)
        
        리드라인아이콘=mk_아이콘(f"{idx}-번째")
        기사중심문장=mk_기사본문_주요문장("주요문장","",주요문장,"",fname)
        회사를포함한문장=mk_기사본문_회사포함("회사를포함한문장","","",회사를포함한문장,회사링크만들기(comtag))
        기사=mk_기사본문_접어두기(title,newstext,"","")
        
       
        관련회사테그=mk_관련회사테그(회사링크만들기(comtag))
        
        # 관련회사테그=mk_관련회사테그(ct)


    
 

        구분선="---"
        with open(f'/Users/hg/WORKSPACE/Gitblog/mkdocs-material/docs/md/posts/{fname}.md', "a", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(리드라인아이콘+기사+기사중심문장+회사를포함한문장+관련회사테그+'\n\n'+구분선)

def mf_tag(i):
    # t = f''':octicons-heart-fill-24:{{ .mdx-heart }}'''
    t = f''' =={i}== '''
    return t
# G_stockInfo_DF 종목이름으로 종목코드 찾기
def find_code(name):
    if name != "" or name != None or name != "n":
        code = ""
        try :
            code = G_stockInfo_DF[G_stockInfo_DF['종목명'] == name]['종목코드'].values[0]
        except:
            pass

        return code
    else:
        return ""
def mk_문장분석(text,comtag,serchword):
    # - ==검색어==  
    # - ^^관련회사^^  
    # - ~~쓸데없는정보~~  
    # [`mark`][mark], [`ins`][ins] and [`del`][del] HTML tags: 
    # yellow = f"=={text}=="
    # underlin = f"^^{text}^^"
    # delete = f"~~{text}~~"
    # angker = f"`{text}`"
    serchword = serchword.split("_")
    # text를 .으로 구분하여 리스트로 만들고 datafrmae으로 만들어서 serchword가 포함된 행을 찾아서 yellow로 치환
    text1=text.replace('다.','다. ')#마침표로 끝나야 문장, 1.3% 같은게 있음
    text = text1.split("\n")
    df = pd.DataFrame(text)
    df.columns = ["text"]
    mdf = df.copy()
    cdf = df.copy()
    # df 에서 serchword가 포함된 단어를 찾아서 yellow로 치환
    searlists= []
    
    for i in serchword:
        i=i.strip()
        # df['text']에 문자를 포함하는지 확인
        # df 에 문자가 포함된 행만 추출
        mdf["text"] = mdf["text"].str.replace(i, mf_tag(i))+"<p>"
        if len(mdf[mdf['text'].str.contains(i)].text.values) >1 and i != "":
            #dataframe에서 여러개 한거번에 찾기
            test = '|'.join(serchword)
            searlists.append(mdf[mdf['text'].str.contains(test)].text.values[0]+"<p>")
            # mdf 에서 i 를 포함한 행 삭제
            mdf = mdf[~mdf['text'].str.contains(i)]
    mdf=0
    # df 에서 comtag가 포함된 단어를 찾아서 underlin로 치환
    comlists = []
    # cdf.to_csv('/Users/hg/WORKSPACE/Gitblog/naver/src/data/json/크레딧_은행_인수/크레딧_은행_인수_news_원본.csv',encoding='utf-8-sig',index=False,header=True)
    
    if len(comtag) > 0:
        for i in comtag:
            cdf["text"] = cdf["text"].str.replace(i, mf_tag(i))+"<p>"
            if len(cdf[cdf['text'].str.contains(i)].text.values) > 0 and i != "":
                i=i.strip()
                #dataframe에서 여러개 한거번에 찾기
                test = '|'.join(comtag)
                comlists.append(cdf[cdf['text'].str.contains(test)].text.values[0]+"<p>")
                # cdf = cdf[~cdf['text'].str.contains(i)]
    cdf=0

    # text 리스트에서 문자 일괄 변경
    
    # <br>로 마크다운 줄바꿈


    검색어를포함한문장 = "<p>".join(searlists)# <br>로 마크다운 줄바꿈
    검색어를포함한문장.replace("이미지","")
    if len(comlists) >0:
        회사를포함한문장 = "<p>".join(comlists)# <br>로 마크다운 줄바꿈
    else:
        회사를포함한문장 = "관련회사가 없습니다."
        회사를포함한문장 = f"<font color='red'>{회사를포함한문장}</font>"

    return text1, 검색어를포함한문장,회사를포함한문장



 # df['text']에 이미지를 포함하는 행삭제
   
    

fname="제약_임상_3상"
마크다운exm("path",fname)

 
    
# find_code("삼성전자")



