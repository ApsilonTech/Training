#activity code:KL/EP-19/A-002
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:16.09.2022

#6. Write a python program:
#Step 1: create an empty list
#Step 2: display size of list 
#Step 3: use while loop 5 times 
 #i) To read a hostname from <STDIN>
 #ii) To add a input hostname to existing list
#Step 4: using for loop, display list of elements 
#Step 5: display size of the list

l=[]
s=len(l)
print(s)
i=0
while(i<5):
    var=input("enter a hostname:")
    l.append(var)
    i=i+1
for var in l:
    print(var)
print("size:{}".format(len(l)))
    
                         


