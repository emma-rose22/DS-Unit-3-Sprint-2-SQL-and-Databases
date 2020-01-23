import psycopg2
import sqlite3
import pandas as pd

# READ ME
# if you want it to run top to bottom, uncomment everything
# it is commented out to avoid the table already exists error
# and the errors that come from trying to replace something
# that has already been replaced

titanic = pd.read_csv('titanic.csv')

titanic = titanic.replace(' ', '_')
titanic = titanic.replace('/', '_')
titanic = titanic.replace({"\"": "'"}, regex=True)
titanic = titanic.replace("'", '')
titanic.Name = titanic.Name.replace("'", "_")


titanic.rename(columns={'Siblings/Spouses Aboard': 'Siblings_Spouses_Aboard',
                        'Parents/Children Aboard': 'Parents_Children_Aboard', },
               inplace=True)


titanic['Name'] = titanic['Name'].str.replace(r"[\"\',]", '')


print(titanic.head())
print(titanic.shape)
print(titanic.dtypes)

dbname = 'nussvsao'
user = 'nussvsao'
password = 'you cant have my password'
host = 'rajje.db.elephantsql.com'

pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)


pg_curs = pg_conn.cursor()

create_titanic_table = '''
CREATE TABLE titanic_table(
    Survived INT,
    Pclass INT,
    Name TEXT,
    Sex varchar(10),
    Age FLOAT,
    SiblingsSpousesAboard INT,
    ParentsChildrenAboard INT,
    Fare FLOAT

);
'''

pg_curs.execute(create_titanic_table)
pg_conn.commit()

query = 'SELECT * FROM titanic_table'
pg_curs.execute(query)
print(pg_curs.fetchall())

for index, row in titanic.iterrows():
    titanic_insert = f'''
  INSERT INTO titanic_table
  VALUES {row.Survived, row.Pclass, 
  row.Name, row.Sex, row.Age, row.Siblings_Spouses_Aboard, row.Parents_Children_Aboard, row.Fare};'''
    pg_curs.execute(titanic_insert)

pg_conn.commit()

query = 'SELECT * FROM titanic_table;'
pg_curs.execute(query)
print(pg_curs.fetchall())
