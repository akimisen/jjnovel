import pandas as pd
import ast

def extract_novels():
  _data = pd.read_csv('data/authors.csv',index_col='id', encoding='utf-8')
  data=_data.reindex(columns=['name','novels','flw_count','score'])
  novels=[]
  for index,row in data.iterrows():
    for n in ast.literal_eval(row['novels']):
      novels.append((index,row['name'],int(n)))
  df2=pd.DataFrame(novels,columns=['aid','author','nid'])
  df2.to_csv('data/novels_of_author.csv',index=False,encoding='utf-8')

# def query_novels(raw_csv_path):
raw_csv_path='data/newdaylist_author_novels-[raw][20230116-20230216].csv'
_data=pd.read_csv(raw_csv_path,index_col='nid', encoding='utf-8', thousands=',')
data=_data.reindex(columns=['title','author','like_count','avg_click','word_count','chapter_count','is_signed','created','updated','yc','xx','era','style','score','copystatus'])
grouped=data.groupby('author')
novel_count=grouped['title'].count()
avg_word_count=grouped['word_count'].mean()
# copyrights=(grouped['copystatus']=='1').sum()
print(novel_count)
print(avg_word_count)
# print(copyrights)
