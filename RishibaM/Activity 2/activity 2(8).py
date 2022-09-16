#activity code:KL/EP-19/A-002
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:16.09.2022

#8. Write a python program
#Given List 
#LB=[‘0.13’,’14.4’,’1.34’,’3.24’,’2.44’]
#Calculate sum of load balance

LB=['0.13','14.4','1.34','3.24','2.44']
sum=0
for var in LB:
    sum += float(var)
print(sum)
