import pandas as pd
import re


a = ['a','b','c']
b = ['d','e','f']
lists =[]


# lists에  a,b를 각각 1개식 fa 포맷으로  넣어준다.
for i in range(len(a)):
    
    fa = f"- [x] [{a[i]}]({b[i]}) "
    lists.append(fa)
print(lists)



