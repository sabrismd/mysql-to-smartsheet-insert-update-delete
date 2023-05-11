import mysql.connector
import smartsheet
import pandas as pd
import json as js

#load configuration file 

config = js.load(open('config.json'))

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
df=df.replace(r'^\s*$',0,regex=True)
sheet_rows=sheet.rows


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
    print("Recordss successfully inserted")
    
###

# Deleting #
def delete():
    rows = sheet.rows
    row_ids = [row.id for row in rows]
    ss.Sheets.delete_rows(sheet_id, row_ids)
    print("All rows deleted successfully.")


###
# Updating #
def update():
    rows_to_update = []
    for index, row in df.iterrows():
        for sheet_row in sheet_rows:
            if sheet_row.row_number == index+1:
                cells_to_update = []
                for col in sheet.columns:
                    if col.title in row.index and str(row[col.title]) != sheet_row.get_column(col.id).value:
                        cell = smartsheet.models.Cell({
                            'column_id': col.id,
                            'value': str(row[col.title])
                        })
                        cells_to_update.append(cell)
                if cells_to_update:
                    updated_row = smartsheet.models.Row({
                        'id': sheet_row.id,
                        'cells': cells_to_update
                    })
                    rows_to_update.append(updated_row)
                    break
    if rows_to_update:
        ss.Sheets.update_rows(sheet_id, rows_to_update)
        print("Updated successfully")
    else:
        print("No rows to update! So, Skipping the Update Operation")
                    
###

# Skipping the operations
###

if(not sheet_rows)and(not df.empty):
    print("The sheet is empty so the program is about to insert the records to the sheet")
    insert()
    print("Inserted Successfully")
elif df.empty:
    print("your mysql doesnot have records so the program is about to delete the sheet record")
    delete()
    print("deleted successfully")
else:
    print("There Could be a Possibility of Updating the Sheet Cells")
    print("Comparing the Sheet with mysql records")
    update()
    print("processed")





