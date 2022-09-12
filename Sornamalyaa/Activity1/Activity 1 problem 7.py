#Activity Code : KL/EP-19/A-001
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#Dated: 12/09/2022


#12. Given string
     # s='1A2B3C45d6e7'
     # calculate sum of digits
     # Note: use for loop and isdigit() method

s='1A2B3C45d6e7'
sum=0
for val in s:
    if val.isdigit():
        sum+=int(val)
print("Total sum of digits is:", sum)
