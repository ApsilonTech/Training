#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 13/09/2022

"""Question number-5:

How to convert given tuple to list?
configs=(“/etc/passwd”,”/etc/shadow”,”/etc/pam.d/su”)"""


configs=("/etc/passwd","/etc/shadow","/etc/pam.d/su")  #values are in tuple
l=list(configs)    #square bracket used to convert to list
print(type(l),l) #displaying tuple to list using print
