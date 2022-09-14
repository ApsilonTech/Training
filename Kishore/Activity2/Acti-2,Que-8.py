#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 13/09/2022

"""Question number-8:

Write a python program
Given List 
LB=[‘0.13’,’14.4’,’1.34’,’3.24’,’2.44’]
Calculate sum of load balance"""


LB=['0.13','14.4','1.34','3.24','2.44'] #floating numbers are in list 

sum=0              #declaring 0 as value
for i in LB:       #for loop used for repetation and replacing lb in i
    print(i)  
    sum+=float(i)  #it is used for increment
print(sum)         #it displays the output of sum
