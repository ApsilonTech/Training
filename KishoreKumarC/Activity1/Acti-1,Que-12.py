#Activity Code: KL/EP-19/A-001
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 12/09/2022

"""Question number-11:

s='1A2B3C45d6e7'

Calculate sum of digits

Note: use for loop and isdigit()method"""


s='1A2B3C45d6e7' #s as variable name
sum=0
for i in s: #forloop for repetation
    if i.isdigit(): #true block statement
        sum+=int(i) #increment for counting
        
print('total number of digit is:',sum) #print is used to show the output
