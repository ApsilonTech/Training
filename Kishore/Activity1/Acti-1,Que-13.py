#Activity Code: KL/EP-19/A-001
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 12/09/2022

"""Question number-13:

Given String

S="welcome"

Filter list of vowels and count numbers of vowels from given string."""

s='welcome' #declare 's' as variable name
x=0  
for i in s: #for used to repeat
    if i=='a' or i=='e' or i=='o' or i=='i' or i=='u':#true block statement to check whether given letters are present here
        print("vowels present in s=",i) #shows the output
        
        x+=1 #increment in loops
print("total number of vowels is:",x) #shows in output

