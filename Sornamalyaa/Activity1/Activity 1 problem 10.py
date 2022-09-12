#Activity Code : KL/EP-19/A-001
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#Dated: 12/09/2022


#15. Test your python shell (done in python shell)
    #I. Given string is:
       # s1= "bin: usr: daemon: /bin/bash: x: /usr/bin/tcsh: false"
       #a. Count the number of ":" placed in given string

s1= "bin: usr: daemon: /bin/bash: x: /usr/bin/tcsh: false"
count=0
for val in s1:
    if val==":":
        count+=1
print("Number of ':' present in '{}' is {} ".format(s1,count))


    #II. Given string is:
       # s2= "This is sample test line\n"
       #a. Remove \n character to from s2 string 

'''
s2= "This is sample test line\n"
print(s2.strip())
'''
