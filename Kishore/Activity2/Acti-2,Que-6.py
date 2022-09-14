#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 13/09/2022

"""Question number-6:

Write a python program:
Step 1: create an empty list
Step 2: display size of list 
Step 3: use while loop 5 times 
 i) To read a hostname from <STDIN>
 ii) To add a input hostname to existing list
Step 4: using for loop, display list of elements 
Step 5: display size of the list"""


l=[]    #creating empty list
print(len(l))  #'len' used to find length of values
a=0
while a<5: #while loop used for repetation
    host_name=(input("Enter host name:")) #getting host name from user using runtime input
    l.append(host_name)  #host name values will be append(add) to l
    a+=1   #used for incrementation and it runs 5 times because we have given condition 5 times
    
print(l) #it prints l values in list

for i in l: #for loop used for repetation process
    print(i)  #it displays l values 5 times
print(len(l)) #it shows length of the values





