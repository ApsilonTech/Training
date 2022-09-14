#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 13/09/2022

"""Question number-7:

write a python program
Given List 
DBs = [‘oracle’,’sql’,’mysql’,’plsql’]
Step 1: read a database name from <STDIN>
Step 2: test input database name is existing or not
Step 3: if input DB name exists, using index(), display index number
Step 4: If input DB does not exist, add the input DB name to the existing list.
Step 5: display list line by line using for loop"""


DBs = ['oracle','sql','mysql','plsql'] #existing lists in DBs variable

data_base=input("enter DBs names:") #getting data base names from user

if data_base in DBs:  #if condition used to check if data_base name exists in DBs or not 
    print(DBs.index(data_base)) #if data_base name exist in DBs it will print the index number of DBs
else: #if data_base name not in DBs it will show the else block
    DBs.append(data_base) #append used to add new values in existing DBs 
for i in DBs: #for loop used for line by line execution
    print(i) #it displays the output of i
    

    
    








    
    
    
