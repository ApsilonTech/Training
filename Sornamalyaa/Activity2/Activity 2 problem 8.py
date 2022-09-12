#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 12/09/2022

#8. Write a python program
    #Given List 
    #LB=['0.13','14.4','1.34','3.24','2.44']
    #Calculate sum of load balance

LB=['0.13','14.4','1.34','3.24','2.44']
sum=0
for val in LB:
    sum+=float(val)
print("Sum of load balance of list: ",sum)
