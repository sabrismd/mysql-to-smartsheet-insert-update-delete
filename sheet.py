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

#sql connection
connection = mysql.connector.connect(host=MysqlConfig['host'],
                             user=MysqlConfig['username'],
                             password=MysqlConfig['password'],
                             db=MysqlConfig['databaseName'])

# configuring for smartsheet
SheetConfig=dev['smartsheet']
AccessToken=SheetConfig['access_token']
SheetClient=smartsheet.Smartsheet(AccessToken)

# configuration for accessing the mysql table
Mysql_Sheet_Sync =dev['sync']
for i in range(len(Mysql_Sheet_Sync)):
    sync=Mysql_Sheet_Sync[i]
    sheet_id=sync['sheet_id']
    sheet=SheetClient.Sheets.get_sheet(sheet_id)
    query = f"SELECT * FROM {sync['mysqlTable']}" # if your table records are more you can use the limit and offset keys in the query variable
    df=pd.read_sql(query,connection)
    df.replace(r'^\s*$',0,regex=True)
    df.sort_values(by='id',ascending=True)
    sheet_rows=sheet.rows
    sheet_columns=sheet.columns
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
            col_ids = [col.id for col in sheet_columns]
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
        for row in sheet_rows:
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
            for i,j in zip(range(len(df_row_values2)), range(len(col_ids))):
                new_cell = smartsheet.models.Cell()
                new_row = smartsheet.models.Row()
                new_row.id = row_id
                new_cell.column_id = col_ids[j]
                new_cell.value = df_row_values2[i]
                new_row.cells.append(new_cell)
                SheetClient.Sheets.update_rows(sheet_id, [new_row])
                isUpdate = True
    
    #DECIDING THE ROW TO BE INSERTED OR DELETED OR UPDATED
    df_rows = [str(row[0]) for index, row in df.iterrows()]
    SheetRows = [str(rows.cells[0].value) for rows in sheet_rows]
    for x in df_rows:
        if x not in SheetRows:
            insert(x)
        else:
            update(x)
    for y in SheetRows:
        if y not in df_rows:
            delete(y)
    
    print(f"Sheet {sheet.name} is Finished its Process")
        
    if isInsert:
        print(f"Row(s) Only Inserted to the {sheet.name} Sheet")
    elif isDelete:
        print(f"Unnecessary Row Deleted From The {sheet.name} Sheet")
    elif isUpdate:
        print(f"Sheet {sheet.name} Updated")
    else:
        print(f"Nothing to Do,Both {sync['mysqlTable']} and {sheet.name} Has Same Records")
