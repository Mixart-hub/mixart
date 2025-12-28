import sqlite3, pandas as pd
from sklearn.linear_model import LinearRegression

db=sqlite3.connect('data/mixart.db')
df=pd.read_sql("SELECT rowid, amount FROM orders",db)
if len(df)>1:
    m=LinearRegression().fit(df[['rowid']],df['amount'])
    print("Prognoz:",int(m.predict([[len(df)+1]])[0]))
