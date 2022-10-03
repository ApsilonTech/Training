#activity code:KL/EP-19/A-002
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:19.09.2022

#11. Write a python program 
#Given Tuple :
#EMP=(‘101,leo,sales,1000’,’102,paul,prod,2000’,’103,raj,HR,3000’)
#Use for loop along with split() to get the following expected result.
#Expected result:-
#Emp name is leo working department is sales
#Emp name is paul working department is prod
#Emp name is raj working department is HR
#---------------------------------------------------------
#Sum of Emp’s cost is: 6000
#----------------------------------------------------------

EMP=('101,leo,sales,1000','102,paul,prod,2000','103,raj,HR,3000')
EMP1=list(EMP)
for var in EMP:
    L=[]
    i=var.split(",")
    for var1 in i:
        L.append(var1)
    print(L)    
