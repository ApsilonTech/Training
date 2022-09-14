#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 13/09/2022

"""Question number-10:

Write a python program
Given tuple
Products=(“P1”,”P2”,”P3”,”P4”,”P5”)
display the list of products except P2 and P3 
Note : use for loop statement"""

Products=('P1','P2','P3','P4','P5')  #given tuple,products name as variable

l=list(Products)  #tuple changed to list
l1=[] #creating empty list
 
for i in Products:  #for loop used for line by line execution
    if i=="P2" or i=="P3": #if 'p2' and 'p3' are in i it will delete the values
        del(i) #del used for delete
    else: 
        l1.append(i) #append used to add the values in 'l1' empty list
        print(i)
