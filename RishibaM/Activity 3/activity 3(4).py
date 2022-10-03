#activity code:KL/EP-19/A-003
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#4.Write a python program
#Given list structure
#Emp = [ "e123,ram,sales,pune,1000",
#"e132,kumar,prod,bglore,3423",
#"e456,arun,prod,chennai,2456",
#"e544,vijay,hr,mumbai,6500" ]

#a. create an empty dictionary and name it as Emp 
#b. convert the above given list into dict format.
#c. display list of key,value pairs from EMP dict
#Note:- employee id as a key, emp name as value

EMP1=["e123,ram,sales,pune,1000","e123,kumar,prod,bglore,3423","e456,arun,prod,chennai,2456","e544,vijay,hr,mumbai,6500"]
emp={}
for var in EMP1:
    var1=var.split(",")
    emp[var1[0]]=var1[1]
print(emp)
print()
for i in emp:
     print("keys:{}\tvalues:{}".format(i,emp[i]))
