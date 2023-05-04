import mysql.connector
import smartsheet
import pandas as pd
import json

#load configuration file 

config = json.load(open('C:/Users/Elcot/Desktop/SmartSheet I U D/config.json'))

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
    sheet_rows = sheet.rows
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
                    ss.Sheets.update_rows(sheet_id, [updated_row])
                    print(f"Row {index+1} updated successfully")
                    break
                    
###

# Skipping the operations
def skip():
    sheet_rows = sheet.rows
    if len(df) != len(sheet_rows):
        return False
    for index, row in df.iterrows():
        sheet_row = sheet_rows[index]
        for col in sheet.columns:
            if col.title in row.index and str(row[col.title]) != sheet_row.get_column(col.id).value:
                return False
    return True



###

if len(sheet_rows)==0:
    print("The sheet is empty so the program is about to insert the records to the sheet")
    insert()
    print("Inserted Successfully")
elif df.empty:
    print("your mysql doesnot have records so the program is about to delete the sheet record")
    delete()
    print("deleted successfully")
    for row in sheet_rows:
        ss.Sheets.delete_rows(sheet_id,[row.id])
else:
    if skip():
        print("could not insert datas")
        print("The MySQL table and sheet are already in sync. No updates needed.")
    else:
        print("Checking for any updates of cells")
        update()
        print("some rows are updated")
    
    




