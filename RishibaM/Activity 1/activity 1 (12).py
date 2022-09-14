#activity code:KL/EP-19/A-001
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:14.09.2022

#12. Given String 
#s='1A2B3C45d6e7'
#Calculate sum of digits
#Note: use for loop and isdigit() method

a='1A2B3C45d6e7'
sum=0
for var in a:
    if var.isdigit():
        sum += int(var)
print("total sum of digits is:",sum)
    
