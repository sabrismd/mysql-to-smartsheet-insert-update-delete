import mysql.connector
import smartsheet
import pandas as pd
import json

#load configuration file 

config = json.load(open('C:/Users/Elcot/Desktop/config.json'))

#sql connection
connection = mysql.connector.connect(host=config['dev']['mysql']['host'],
                             user=config['dev']['mysql']['username'],
                             password=config['dev']['mysql']['password'],
                             db=config['dev']['mysql']['databaseName'])

for table in config['dev']['sync']:
    mysql_table = table['mysqlTable']
    
    
at=config['dev']['smartsheet']['access_token']
ss=smartsheet.Smartsheet(at)
sheet_id=config['dev']['smartsheet']['sheet_id']
sheet=ss.Sheets.get_sheet(sheet_id)
query = f"SELECT * FROM {mysql_table}"
df=pd.read_sql(query,connection)
column=sheet.columns[0]
row=sheet.rows[0]
#print(row.cells[0].value)

# Inserting #

def insert():
    rows=[]
    for index,row in df.iterrows():
        cells=[]
        for col in sheet.columns:
            cell=smartsheet.models.Cell({
            'column_id':col.id,
            'value':str(row[col.title])
            })
            cells.append(cell)
            new_row=smartsheet.models.Row({
            'to_top':True,
            'cells':cells
            })
        rows.append(new_row)
    ss.Sheets.add_rows(sheet_id,rows)
###

if(row.cells[0].value==None):
    insert()
    print("Inserted Successfully")
else:
    print("could not insert")
    
    





