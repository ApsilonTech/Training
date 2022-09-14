#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 13/09/2022

"""Question number-12:

Write a python program to iterate through the given list.
Given list
hosts=['host01','host02','host03','host04','host05']
Using membership operator test host03 exists or not
if ‘host03’ does not exists display suitable message to screen"""


hosts=['host01','host02','host03','host04','host05']  #hosts as variable name and there are 5 values in lists

if 'host03' in hosts:  #if is true block statement and it checks whether condition is matching
    print("host03 is exist") #if condition of if is true then it will display this result
else:  #else block is false block statement 
    print("host03 is not exist in hosts")
