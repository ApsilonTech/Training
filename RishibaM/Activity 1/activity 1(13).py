#activity code:KL/EP-19/A-001
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:14.09.2022

#13. Given String 
#S=’welcome’
#Filter list of vowels and count number of vowels from given string.

r='welcome'
count=0
for var in r:
    if var=='a'or var=='e'or var=='i'or var=='o'or var=='u':
        print(var)
        count+=1
print("total no.of vowels in r 'welcome'is",count)
