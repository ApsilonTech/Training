#activity code:KL/EP-19/A-001
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:14.09.2022

#15. Test your python shell 
#I. Given string is : 
#s1="bin: usr: daemon: /bin/bash: x: /usr/bin/tcsh: false"
#a. Count the number of ":" placed in given string.
#II. Given string is :
#s2="This is sample test line\n"
#a. Remove \n character to from s2 string

p1="bin: usr: daemon: /bin/bash: x: /usr/bin/tcsh: false"
count=0
for var in p1:
    if var ==":":
        count+=1
print(count)
        
   
p2="This is sample test line\n"
print(p2.strip('\n'))

