#activity code:KL/EP-19/A-002
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:19.09.2022

#7. write a python program
#Given List 
#DBs = [‘oracle’,’sql’,’mysql’,’plsql’]
#Step 1: read a database name from <STDIN>
#Step 2: test input database name is existing or not
#Step 3: if input DB name exists, using index(), display index number
#Step 4: If input DB does not exist, add the input DB name to the existing list.
#Step 5: display list line by line using for loop

DBs=['oracle','sql','mysql','plsql']
db=input("enter a  database name")
if db in DBs:
    print("given database name is existing")
else:
    print("DBs{}is db at{}index".format(DBs,db.index(DBs)))
for var in DBs:
        print(var)
    
