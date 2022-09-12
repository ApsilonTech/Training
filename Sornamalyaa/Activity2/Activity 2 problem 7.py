#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 12/09/2022

#7. write a python program
    #Given List 
    # DBs = ['oracle','sql','mysql','plsql']
    # Step 1: read a database name from <STDIN>
    # Step 2: test input database name is existing or not
    # Step 3: if input DB name exists, using index(), display index number
    # Step 4: If input DB does not exist, add the input DB name to the existing list.
    # Step 5: display list line by line using for loop

DBs = ['oracle','sql','mysql','plsql']
dn= input("Enter database name: ")
if dn in DBs:
    print("'{}' in existing list in an index of {}".format(dn,DBs.index(dn)))
else:
    DBs.append(dn)
for val in DBs:
    print(val)
