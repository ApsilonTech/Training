#Question4_activity3

'''
4. Write a python program
Given list structure
Emp = [ "e123,ram,sales,pune,1000",
"e132,kumar,prod,bglore,3423",
"e456,arun,prod,chennai,2456",
"e544,vijay,hr,mumbai,6500" ]

a. create an empty dictionary and name it as Emp
b. convert the above given list into dict format.
c. display list of key,value pairs from EMP dict
Note:- employee id as a key, emp name as value
'''

#activity_code:KL/EP-19/A-003
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

Employee=[ "e123,ram,sales,pune,1000", "e132,kumar,prod,bangalore,3423","e456,arun,prod,chennai,2456", "e544,vijay,hr,mumbai,6500"]
Emp={}
for a in Employee:
    b=a.split(",")
    Emp[b[0]] = b[1] 
print(Emp)
for a in Emp:
    print("keys:",a,"values:",Emp[a])







