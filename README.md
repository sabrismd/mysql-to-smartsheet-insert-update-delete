# mysql-to-smartsheet-insert-update-delete
This Project is Based on Automating the insertion/deletion/updation of sheets with the mysql reterieval

# first of all install the required packages by typing the following command
**pip install -r Requirements.txt**



#then loading the configuration file 
config = json.load(open('C:/Users/Elcot/Desktop/SmartSheet I U D/config.json'))

# making connection to the sql server 
connection = mysql.connector.connect(host=config['dev']['mysql']['host'],
                             user=config['dev']['mysql']['username'],
                             password=config['dev']['mysql']['password'],
                             db=config['dev']['mysql']['databaseName'])

for table in config['dev']['sync']:
    mysql_table = table['mysqlTable']
    
#accessing the sheet
at=config['dev']['smartsheet']['access_token']
ss=smartsheet.Smartsheet(at)
sheet_id=config['dev']['smartsheet']['sheet_id']
sheet=ss.Sheets.get_sheet(sheet_id)
query = f"SELECT * FROM {mysql_table}"

#here i am using pandas library for data visualizing and analysing 
pandas have a method that is read_sql() inside i must provide the query , and my connection Eg: "pd.read_sql(query,connection)"

#by using the pandas i can access the datas 

query = f"SELECT * FROM {mysql_table}"
df=pd.read_sql(query,connection)
df=df.replace(r'^\s*$',0,regex=True)
sheet_rows=sheet.rows

#i am applying the regular expression concept because some tables has blank spaces not none values , so i am using the "\s" for blankspace and i am replacing it with the 0 , 
#why i am using this regular expression is because i could not complete the update function() properly . so  i am using it


#then the program moves into take decisions according to the respective condition

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
    
#######

#the first if has two condition one is sheet_rows must be zero and pandas dataframes of the mysql table should not be empty

#this sheet has empty values column names only exists
![image](https://user-images.githubusercontent.com/90912183/237012904-971f86cc-fa8d-4ac1-8a54-5016c2ed6802.png)

#the code will check the length of the sheet has zero value , then only the first condition of if will be satisfied

#second condition is dataframes from the mysql table should not be empty ...it must have some records then only two condition satisfied using "df.empty" to check whether the gained table has some records or not
#my second condition of if is satisfied because it has some records

![image](https://user-images.githubusercontent.com/90912183/237012582-8be89604-3fc2-4320-b115-d660c7aed0fa.png)

#now  both the conditions of if are now satisifed the program is about to perform the insert( ) operation

#this is my insert function
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
#inside the insert() first empty "rows" will be created , then iterating into the dataframes by the index and row , inside create the "cells" list
#and iterating to the sheet columns and creating a cells , those cell values are got from the dataframes table,it will continue to loop until all the columns will got some values 
#using cell.append() method appending cells to the new rows, if all the values from the dataframes table inserted into the cells , now it is ready to add into the sheets
# using the row.append(new_row)
#after all the insertion of data the program in the end will say "records succesfully insereted"

#insert() successfully implemented 

#now i am changing the  table of mysql database which has null records, let's see what happens.
#i am running the program again, now if is not satisfied because sheet_rows has some records the first condition of if is failed.
#so the program is about to delete the sheet records because mysql has no records 
#so it moves into the elif condition it has a condition of dataframes is empty.
#the elif condition will check whether the dataframes has records or not.
#according to my condition the second condition will be successfully executed because dataframes from mysql is empty...
#so the program is about to move into the delete () 

# this is the delete function 
# Deleting #
def delete():
    rows = sheet.rows
    row_ids = [row.id for row in rows]
    ss.Sheets.delete_rows(sheet_id, row_ids)
    print("All rows deleted successfully.")


# inside this delete ()
#sheet rows will be deleted with the help of the row ids 
#and finally all the rows of a sheet were successfully deleted 
#now insert() and delete() done

# if i want to update the cells of sheet because of the changes of mysql records .
#i will move into the update() 
#when i will move into the update() is if and only if the cells of the sheet need to be  changed according to the mysql records
#let's take a scenario the sheets data were changed by another user but it is not updated to the mysql records for this the program will #check and perform the any updation of sheets.

else:
    print("There Could be a Possibility of Updating the Sheet Cells")
    print("Comparing the Sheet with mysql records")
    update()
    print("processed")
    
    
# this is the update function 
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
        
        
#this update function will compare the dataframes from mysql and sheets row by row and checks the cell value of each as it same to the #mysql dataframes if it not same it will proceed further and finally the program will show updated succesfully if there is updation
#otherwise it show no rows to update because of the same records those are not mismatching
![image](https://user-images.githubusercontent.com/90912183/237022788-124848d7-a2a9-46ef-883b-20d2d31a61ad.png)
#above image row 6 of employee were changed , when i perform the update() it will  change the value according to the mysql
#after changed
![image](https://user-images.githubusercontent.com/90912183/237023474-223bba25-fbee-4043-bfdc-c9dc6a95cd9f.png)


