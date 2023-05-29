# mysql-to-smartsheet-insert-update-delete
This Project is Based on Automating the insertion/deletion/updation of sheets with the mysql reterieval

# first of all install the required packages by typing the following command
**pip install -r Requirements.txt**



#then load the configuration file 
config = json.load(open('config.json'))

#why i am using the config file here for,whenever if we want to change our mysql server or database we dont move into code ,instead of we change the path or anything in the config file itself.
#assigning new variable for "config['dev']"
dev=config['dev']

#configuring the mysql to make connection to the server
MysqlConfig=dev['mysql']

#configuring for smartsheet
SheetConfig=dev['smartsheet']

#configuration for accessing the mysql table
MysqlTableConfig =dev['sync']['mysqlTable']

#sql connection
connection = mysql.connector.connect(host=MysqlConfig['host'],
                             user=MysqlConfig['username'],
                             password=MysqlConfig['password'],
                             db=MysqlConfig['databaseName'])
    
#accessing the sheet
AccessToken=SheetConfig['access_token']
SheetClient=smartsheet.Smartsheet(AccessToken)
sheet_id=SheetConfig['sheet_id']
sheet=SheetClient.Sheets.get_sheet(sheet_id)

#here i am using pandas library for data visualizing and analysing pandas have a method that is read_sql() inside i must provide the
query , and my connection Eg: "pd.read_sql(query,connection)"

#by using the pandas i can access the datas 

query = f"SELECT * FROM {MysqlTableConfig} LIMIT 100 OFFSET 120" # if your table records are more you can use the limit and offset keys in the query variable
df=pd.read_sql(query,connection)
df=df.replace(r'^\s*$',0,regex=True)
sheet_rows=sheet.rows

#i am applying the regular expression concept because some tables has blank spaces not none values , so i am using the "\s" for blankspace and i am replacing it with the 0 , 
#why i am using this regular expression is because i could not complete the update function() properly . so  i am using it

#then the program moves into take decisions according to the respective condition

if df.any:
df_rows = [str(row[0]) for index, row in df.iterrows()]
SheetRows = [str(rows.cells[0].value) for rows in sheet.rows]
isUpdate=False
isInsert=False
isDelete=False
for x in df_rows:
if x in SheetRows:
update()
isUpdate=True
elif x not in SheetRows:
insert(x)
isInsert=True
for y in SheetRows:
if y not in df_rows:
delete(y)
isDelete=True
if isUpdate and isDelete:
print("Row(s) deleted from the sheet and also Sheet Updated With Mysql Table")
elif isUpdate and isInsert:
print('Row(s) inserted to the sheet and also Sheet Updated With Mysql Table')
elif isInsert:
print("Rows only Inserted to the sheet")
elif isUpdate:
print('Sheet Usually Updated')
elif isDelete:
print("row only deleted from the sheet")
    
#the primary if condition is "df.any" , why its for? it checks for dataframes from the mysql table, that should not be empty (i.e)dataframes should always have some records , this condition will never fail, so i put it as primary. 

#initially sheet has null records
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/7d1ea1cf-8ce6-46a9-b9e1-266d255b941e)

#if the code runs it will take a list of df and list of sheet,both the lists contains the primary value , I am comparing the two lists and performing the functions accordingly.
#now its prompts us,
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/f91e6a04-e322-4427-9e18-7144b367fc0a)
#checking the sheet has having,
#yes records were inserted,
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/bdbb5057-9698-45a9-9c77-c81ec3ebb6a3)

#now i want to perform delete, when i should perform delete is, if the row of a sheet is not in mysql table row.
#so, now i am adding a extra row to the sheet , check what will happen.
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/415d4dd4-2013-42b7-bbfe-b1cfe1b8a1e4)
#so, now the row 101 is manually added by the user,now run the code again.
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/2a9cb804-d2ea-4949-abb0-bf7281adf3cf)
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/e820b97c-4fc5-449d-96ec-5e322dba2e58)
#the row which is not in mysql is deleted
#And Finally the update function works with delete and insert as well,
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/5f6e23b4-426b-4109-b405-58a5016ab98e)









