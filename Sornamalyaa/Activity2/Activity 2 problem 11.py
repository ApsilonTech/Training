#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 12/09/2022


#11. Write a python program 
    #Given Tuple :
    #EMP=('101,leo,sales,1000','102,paul,prod,2000','103,raj,HR,3000')
    #Use for loop along with split() to get the following expected result.
    #Expected result:-
    #Emp name is leo working department is sales
    #Emp name is paul working department is prod
    #Emp name is raj working department is HR
    #---------------------------------------------------------
    #Sum of Emp’s cost is: 6000
    #---------------------------------------------------------

EMP=('101,leo,sales,1000','102,paul,prod,2000','103,raj,HR,3000')
Emp1=list(EMP)
val2=[]
for val in Emp1:
    v=val.split(",")
    for v1 in v:
        val2.append(v1)
#print(val2)
print("Emp name is {} working department is {}".format(val2[1],val2[2]))
print("Emp name is {} working department is {}".format(val2[5],val2[6]))
print("Emp name is {} working department is {}".format(val2[9],val2[10]))
print("-"*45)
sum=int(val2[3])+int(val2[7])+int(val2[11])
print("Sum of Emp’s cost is: ",sum)
print("-"*45)
