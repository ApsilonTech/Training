#Activity Code: KL/EP-19/A-001
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 12/09/2022

"""Question number-15:

Test your python shell

    I. Given string is :s1="bin: usr: daemon: /bin/bash: x: /usr/bin/tcsh: false"
       a. Count the number of ":" placed in given string.
   II. Given string is :s2="This is sample test line\n"
       a. Remove \n character to from s2 string"""

s1="bin:usr:daemon:/bin/bash:x:/usr/bin/tcsh:false" #s1 as variable name
x=0
for i in s1: #forloop is used for repetation
    if i==":":#true block statement
        x=x+1 #count values
print("number of ':' present in s1 is:",x)#it shows output


s2="This is sample test line\n"#s2 as variable name
s2.strip() #'strip' is used to remove
print(s2) #shows the output
