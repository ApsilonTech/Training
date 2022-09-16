#Activity Code: KL/EP-19/A-003    
#Platform: Python 3.10,windows 10 
#Author: Mr.Kishore Kumar C       
#Role: Software Engineer, Apsilon.
#Date: 16/09/2022                 

""" Question number-7:

Write a python program:
Step 1: create a new file host.py 
Step 2 : create an empty dict
Step 3 : use looping statements – 5times
 i) Read a hostname from <STDIN>
 ii) Read a IP-Address from <STDIN>
 iii) Add a input details to existing dict
 iv) with hostname as a key and IP address as it’s value
Step 4 : display Key/ value details to monitor """

dictionary={}  #creating empty dictionary

a=0
while a<5:  #loop will run 5 times
    hostname=str(input("Enter Host name:"))  #getting input from user
    IPaddress=str(input("Enter IP address:")) 
    dictionary[hostname]=IPaddress #used to show keys and values
    a+=1
 
for i in dictionary:            
    print("keys: {} Values: {}".format(i,dictionary[i]))



""" Question number-8:

Write a python program – modify the above program (host.py) 
Step 1: read a hostname from <STDIN> 
Step 2: Use membership operator to test whether the input 
hostname already exists or not.
Step 3: if it’s exists already, display pop up message “Sorry your 
input hostname is exists” """

name=str(input("Enter Host name:"))
if (name in dictionary): #Checking whether our hostname is already there or not
    print("Sorry your input hostname is exists")
















    
