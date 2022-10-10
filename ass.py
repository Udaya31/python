import pandas as pd
import numpy as np
import csv
import sqlite3

def create_f(how):
    a='lake'
    for i in range(1,how+1):
        b=str(i)
        a+=b
        file=open(f"{a}.txt", "w")
        file.write("Application,date,amount,load")
        print(f'File {i} created')
        a=a.strip(b)


def read_f(re):
    for i in range(1,re+1):
        s=input(f'Enter your {i} file name:')
        file_read=pd.read_csv(s)
        st_date=input('Enter Starting date:')
        file_read['date']= pd.Series(pd.date_range(start=st_date, end='2020-10-01 ', freq ='H'))
        file_read['load']='2020-10-01'
        file_read['Application']='Lake'
        file_read['amount']=np.random.randint(5,10,size=(len(file_read['date']))).astype(float)
        
        file_read.to_csv(s,index=False)
        print(f'File {i} updated!')

def comp(re):
    f1=input('Enter your First file to compare:')
    for i in range(2,re+1):
        file1=pd.read_csv(f1)
        f2=input(f"Enter your {i} file to compare:")
        file2=pd.read_csv(f2)
        file1=pd.concat([file1,file2[~file2.date.isin(file1.date)]])
        file1.sort_values(["date"], axis=0, ascending=[True], inplace=True)
        file1.to_csv(f1,index=False)
        print(f'File {i} updated!')


#Creating file
how=int(input('How many Files u want to create:'))
create_f(how)
#Reading file
re=int(input('How many files you want to read:'))
read_f(re)
#Comparing file
comp(re)
#Connecting Sqlite
conn=sqlite3.connect('lakes.db')
c=conn.cursor()
c.execute("""create table datec(application text,date integer,amount real,load text)""")
conn.commit()
lite=input('Enter the file name you want to import in SQLite:')
sq=pd.read_csv(lite)
sq.to_sql('datec',conn,index=False,if_exists='append')
data=conn.execute('''select * from datec''')
# for row in data:
#     print(row)

conn.commit()
conn.close()