#Question15_activity1
'''
Test your python shell 
I. Given string is : 
s1="bin: usr: daemon: /bin/bash: x: /usr/bin/tcsh: false"
a. Count the number of ":" placed in given string.

II.  Given string is :
s2="This is sample test line\n"
a. Remove \n character to from s2 string
'''
#Activity-code: KL/EP-19/A-001
#Platform: python 3.10,winx 10
#author name="mr.JITHENDRAN"
#Role: Software Engineer, Apsilon


s1="bin: usr: daemon: /bin/bash: x: /usr/bin/tcsh: false"
a=0
for i in s1:
    if i==":":
        a=a+1
print("the number of ':' is : ",a)


s2="This is a sample test line\n"
s2.strip("\n")
print(s2)
        
