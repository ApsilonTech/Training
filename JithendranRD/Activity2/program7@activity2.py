#Question7_activity2
'''
write a python program
Given List
DBs = [‘oracle’,’sql’,’mysql’,’plsql’]
Step 1: read a database name from <STDIN>
Step 2: test input database name is existing or not
Step 3: if input DB name exists, using index(), display index number
Step 4: If input DB does not exist, add the input DB name to the existing list.
Step 5: display list line by line using for loop
'''
#activity_code:KL/EP-19/A-002
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

DBs=['oracle','sql','mysql','plsql']            #declare a var name as DBs
Database1=(input("enter the database name: "))  #declare another var name Database and get the input from the user
if Database1 in DBs:                            #check if the input name exists in DBs
    print("index number of the name : ",DBs.index(Database1))#if exists then print the index no. using index()
    print("")
    print("the lists are:")
    print("")
else:
    print('')
    print("only these are the accepted names: ")
    DBs.append(Database1)                       #if not exists print the DBs name list using append
for a in DBs:                                   #using for loop print the names one by one.
    print(a)
    
    
