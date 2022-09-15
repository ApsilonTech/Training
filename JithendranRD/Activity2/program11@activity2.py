#Question11_activity2
"""
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
----------------------------------------------------------
"""

#activity_code:KL/EP-19/A-002
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer


EMP=('101,leo,sales,1000','102,paul,prod,2000','103,raj,HR,3000')
E1=list(EMP)
E2=[]
for a in E1:
    v=a.split(",")
    for v1 in v:
        E2.append(v1)
print("Emp name is",E2[1], "working department is",E2[2])
print("Emp name is",E2[5], "working department is",E2[6])
print("Emp name is",E2[9], "working department is",E2[10])
sum=int(E2[3])+int(E2[7])+int(E2[11])
print("-"*50)
print("Sum of Emp’s cost is: ",sum)
print("-"*50)
