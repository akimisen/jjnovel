import pandas as pd
import ast

def extract_novels():
  _data = pd.read_csv('data/authors.csv',index_col='id', encoding='gbk')
  data=_data.reindex(columns=['name','novels','flw_count','score'])
  novels=[]
  for index,row in data.iterrows():
    for n in ast.literal_eval(row['novels']):
      novels.append((index,row['name'],int(n)))
  df2=pd.DataFrame(novels,columns=['aid','author','nid'])
  df2.to_csv('data/novels_of_author.csv',index=False,encoding='gbk')

extract_novels()