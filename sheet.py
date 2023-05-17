import mysql.connector
import smartsheet
import pandas as pd
import json as js

#load configuration file 

config = js.load(open('config.json'))

#configuring the mysql to make connection to the server
MysqlConfig=config['dev']['mysql']

# configuring for smartsheet
SheetConfig=config['dev']['smartsheet']

# configuration for accessing the mysql table
MysqlTableConfig =config['dev']['sync']['mysqlTable']

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
sheet_rows=sheet.rows


# Inserting #
def insert(initial_row_value):
    MysqlLists = [str(row[0]) for index, row in df.iterrows()]
    init_value=int(initial_row_value)
    if initial_row_value in MysqlLists:
        row_values = df[df['id'] == init_value].values.tolist()
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
        response = SheetClient.Sheets.add_rows(sheet_id, [new_row])
        if response.message == 'SUCCESS':
            print("Row added successfully.")
        else:
            print("Failed to add row.")
    
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

if df.any:
        df_rows = [str(row[0]) for index, row in df.iterrows()]
        SheetRows = [rows.cells[0].value for rows in sheet.rows]
        print(df_rows)
        print(SheetRows)
        print(len(df_rows))
        print(len(SheetRows))
        if len(df_rows) > len(SheetRows):
            for k in range(len(df_rows)):
                SheetRows.append('')
            for i in range(len(df_rows)):
                if df_rows[i] != SheetRows[i]:
                    print(f"Row {i+1} From MySql is not  Matching to the Sheet Row {i+1}")
                    insert(df_rows[i])
                    print("Inserted")
elif df.empty:
    print("your mysql doesnot have records so the program is about to delete the sheet record")
    delete()
    print("deleted successfully")
else:
    print("There Could be a Possibility of Updating the Sheet Cells")
    print("Comparing the Sheet with mysql records")
    update()
    print("processed")





