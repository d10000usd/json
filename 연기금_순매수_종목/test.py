import pandas as pd
import re
ct = ["스타크래프트asdfasdf          대회     블리자드",1]

ct1 = re.sub(r"\s+", " ", ct[0])
ct[0]=ct1
print(ct)
# ct1 = ct.replace(" ","_")

# ct = ct.split(" ")

# print(ct1)
# artistrings = pd.read_json(  f'/Users/hg/WORKSPACE/Gitblog/naver/src/data/json/{ct1}/{ct1}.json'  )
# # artistrings 에서 ct 리스트에 있는 단어가 포함된 갯수를 세어서 출력
# artistrings[ct[0]] = artistrings['newstext'].str.count(ct[0])
# artistrings[ct[1]] = artistrings['newstext'].str.count(ct[1])
# artistrings[ct[2]] = artistrings['newstext'].str.count(ct[2])
# artistrings[ct1] = artistrings.sum(axis=1)

# print(artistrings[[ct[0],ct[1],ct[2],ct1]])

# # artistrings 정렬 오름차순
# artistrings = artistrings.sort_values(by=[ct1], axis=0, ascending=False)
# print(artistrings[[ct[0],ct[1],ct[2],ct1]])

# # artistrings[ct1] 값이 0인 행을 제거
# artistrings = artistrings[artistrings[ct1] != 0]

# artistrings.to_json(  f'/Users/hg/WORKSPACE/Gitblog/naver/src/data/json/{ct1}/{ct1}.json'  , orient='records', force_ascii=False, indent=4 )