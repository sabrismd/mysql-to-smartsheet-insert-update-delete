# mysql-to-smartsheet-insert-update-delete
This Project is Based on Automating the insertion/deletion/updation of sheets with the mysql reterieval

# first of all install the required packages by typing the following command
**pip install -r Requirements.txt**



# then load the configuration file 
config = json.load(open('config.json'))

#why i am using the config file here for,whenever if we want to change our mysql server or database we dont move into code ,instead of we change the path or anything in the config file itself.
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/3a86820a-ca81-421f-8564-302680f46d93)


# sql connection
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/520d27a0-fde0-47b2-8b04-c9736d813cfe)

# Accessing The Sheet
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/3dbeb418-166e-4b16-8ab9-b8f7c6a5e93a)


#here i am using pandas library for data visualizing and analysing pandas have a method that is read_sql() inside i must provide the
query , and my connection Eg: "pd.read_sql(query,connection)"

# by using the pandas i can access the datas 

![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/a66e1c19-8c1f-4feb-94da-dfd89afccb16)


#i am applying the regular expression concept because some tables has blank spaces not none values , so i am using the "\s" for blankspace and i am replacing it with the 0 , 
#why i am using this regular expression is because i could not complete the update function() properly . so  i am using it

# then the program moves into take decisions according to the respective condition

![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/9e69bedf-c4b2-482f-97da-c3f672129e66)


# the primary if condition is "df.any" , why its for? it checks for dataframes from the mysql table, that should not be empty (i.e)dataframes should always have some records , this condition will never fail, so i put it as primary. 

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
# And Finally the update function works with delete and insert as well,
![image](https://github.com/sabrismd/mysql-to-smartsheet-insert-update-delete/assets/90912183/5f6e23b4-426b-4109-b405-58a5016ab98e)









