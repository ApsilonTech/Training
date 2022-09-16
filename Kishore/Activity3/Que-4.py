#Activity Code: KL/EP-19/A-003
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 15/09/2022

"""Question number-4:

Write a python program
Given list structure
Emp = [ "e123,ram,sales,pune,1000",
"e132,kumar,prod,bglore,3423",
"e456,arun,prod,chennai,2456",
"e544,vijay,hr,mumbai,6500" ]
a. create an empty dictionary and name it as Emp 
b. convert the above given list into dict format.
c. display list of key,value pairs from EMP dict
Note:- employee id as a key, emp name as value"""




Employee = [ "e123,ram,sales,pune,1000", "e132,kumar,prod,bangalore,3423",
        "e456,arun,prod,chennai,2456", "e544,vijay,hr,mumbai,6500"]

Emp={}
for i in Employee:
    i2=i.split(',') #spliting commas
    Emp[i2[0]]=i2[1] 
print(Emp)
for i in Emp:
    print("Keys:",i,"Values:",Emp[i])









