#Activity Code: KL/EP-19/A-001
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 12/09/2022

"""Question number-9:

Write a python program:
    a.Declare a string variable as os
    b.Initialize your working os name as its value(ex:if your working operating
      is aix, os="aix")
    c.Using membership operator,test whether a character "x" is found in the
      input string"""

os="Windows"    #declare 'os' as variable name and 'windows' as its value.
if ("W" in os): #if block is true block and it checks whether 'w'letter is in os value.
    print("Yes,W is in windows") #print to show the output.
else:          #else part is false block.
    print("W is not in windows") #if 'w' letter is not is os value it will display this output.
