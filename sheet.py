import mysql.connector
import smartsheet
import pandas as pd
import json as js

#load configuration file 

config = js.load(open('config.json'))

#Comments: use dev varaible and from dev variable derive the MysqlConfi,SheetConfig and  MysqlTableConfig
dev=config['dev']

#configuring the mysql to make connection to the server
MysqlConfig=dev['mysql']

# configuring for smartsheet
SheetConfig=dev['smartsheet']

# configuration for accessing the mysql table
MysqlTableConfig =dev['sync']['mysqlTable']

#sql connection
connection = mysql.connector.connect(host=MysqlConfig['host'],
                             user=MysqlConfig['username'],
                             password=MysqlConfig['password'],
                             db=MysqlConfig['databaseName'])
    
    
AccessToken=SheetConfig['access_token']
SheetClient=smartsheet.Smartsheet(AccessToken)
sheet_id=SheetConfig['sheet_id']
sheet=SheetClient.Sheets.get_sheet(sheet_id)
query = f"SELECT * FROM {MysqlTableConfig}" # if your table records are more you can use the limit and offset keys in the query variable
df=pd.read_sql(query,connection)
df=df.replace(r'^\s*$',0,regex=True)
df=df.sort_values(by='id', ascending=True)
sheet_rows=sheet.rows
isInsert=False
isDelete=False
isUpdate=False

# Inserting #
def insert(initial_row_value):
    global isInsert
    MysqlLists = [str(row[0]) for index, row in df.iterrows()]
    if initial_row_value in MysqlLists:
        row_values = df[df['id'] == int(initial_row_value)].values.tolist()
        cells = []
        col_ids = [col.id for col in sheet.columns]
        for i in range(len(col_ids)):
            cell_value = row_values[0][i]
            cell = smartsheet.models.Cell()
            cell.column_id=col_ids[i]
            cell.value=str(cell_value)
            cells.append(cell)
        new_row = smartsheet.models.Row()
        new_row.to_bottom = True
        new_row.cells = cells
        SheetClient.Sheets.add_rows(sheet_id, [new_row])
        isInsert=True
    ###


# Deleting #
def delete(to_be_deleted_row_value):
    global isDelete
    rows=sheet.rows
    for row in rows:
        if (str(row.cells[0].value)) == to_be_deleted_row_value :
            SheetClient.Sheets.delete_rows(sheet_id,row.id)
            isDelete=True
    
# Updating #
def update(up):
    global isUpdate
    row_values = []
    row_id = ''
    col_ids = []
    df_row_values = df[df['id'] == int(up)].values.tolist()
    df_row_values2 = [str(i) for i in df_row_values[0]]
    for row in sheet_rows:
        if row.cells[0].value == up:
            res = SheetClient.Sheets.get_row(sheet_id, row.id)
            row_id = row.id
            for cell in res.cells:
                row_values.append(cell.value)
                col_ids.append(cell.column_id)
    if df_row_values2 != row_values:
        for i, j in zip(range(len(df_row_values2)), range(len(col_ids))):
            new_cell = smartsheet.models.Cell()
            new_row = smartsheet.models.Row()
            new_row.id = row_id
            new_cell.column_id = col_ids[j]
            new_cell.value = df_row_values2[i]
            new_row.cells.append(new_cell)
            SheetClient.Sheets.update_rows(sheet_id, [new_row])
            isUpdate = True
# Skipping the operations
###
df_rows = [str(row[0]) for index, row in df.iterrows()]
SheetRows = [str(rows.cells[0].value) for rows in sheet.rows]
for x in df_rows:
    if x not in SheetRows:
        insert(x)
    else:
        update(x)
for y in SheetRows:
    if y not in df_rows:
        delete(y)
        
if isInsert:
    print("Row(s) Only Inserted to the sheet")
elif isDelete:
    print("unnecessary row deleted from the sheet")
elif isUpdate:
    print("Sheet Updated")
else:
    print("No Need To Do,Both Mysql and SmartSheet Has Same Records")
    
