#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 14/09/2022

""" Question number-11:

Write a python program 
Given Tuple :
EMP=(‘101,leo,sales,1000’,’102,paul,prod,2000’,’103,raj,HR,3000’)
Use for loop along with split() to get the following expected result.
Expected result:-
Emp name is leo working department is sales
Emp name is paul working department is prod
Emp name is raj working department is HR
---------------------------------------------------------
Sum of Emp’s cost is: 6000
--------------------------------------------------------- """

EMP=('101,leo,sales,1000','102,paul,prod,2000','103,raj,HR,3000')
Emp1=list(EMP)
lst=[]
for i in Emp1:
    v=i.split(",")
    for i1 in v:
        lst.append(i1)

print("Emp name is {} working department is {}".format(lst[1],lst[2]))
print("Emp name is {} working department is {}".format(lst[5],lst[6]))
print("Emp name is {} working department is {}".format(lst[9],lst[10]))
print("-"*45)
sum=int(lst[3])+int(lst[7])+int(lst[11])
print("Sum of Emp’s cost is: ",sum)
print("-"*45)

