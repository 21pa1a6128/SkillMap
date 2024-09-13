# import streamlit as st
# import pandas as pd

# df1=pd.read_csv('D://krish-naik-genai//Langchain//data//finale2.csv')
# df2=pd.read_csv('D://krish-naik-genai//Langchain//data//naukri-combined-finale1.csv')

# df1.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1,inplace=True)
# df2.drop(['Unnamed: 0'],axis=1,inplace=True)

# df=pd.concat([df1,df2],axis=0)

# print(len(df))
# df = df.drop_duplicates()

# df = df.fillna('None')


# def modify_rating(rating):
#     try:
#         rating=float(rating)
#         if rating>10:
#             return 3.0
#         return rating
#     except:
#         return 3.0
# def modify_experience(exp):
#     try:
#         if(len(exp)==3):
#             return int(exp[2])
#         if(len(exp)==1):return int(exp)
#         return 0
#     except:return 0
# def modify_str(s):
#     try:
#         s.split()
#         return s.strip()
#     except:
#         return 'nan'
# for index, row in df.iterrows():
#     df.at[index, 'Ratings'] = modify_rating(row['Ratings'])
#     df.at[index,'Experience']= modify_experience(row['Experience'])
#     df.at[index,'Skills']=modify_str(row['Skills'])
    
# print(df.head())
# df.to_csv('job_data.csv',index=False)

# # import pandas as pd

# # df=pd.read_csv('job_data.csv')
# # print(df.head)

import pandas as pd
df=pd.read_csv('job_data.csv')
df = df.apply(lambda x: x.str.upper() if x.dtype == "object" else x)
print(df)
df.to_csv('job_data.csv',index=False)
