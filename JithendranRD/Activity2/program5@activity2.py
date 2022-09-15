#Question5_activity2
'''How to convert given tuple to list?
configs=(“/etc/passwd”,”/etc/shadow”,”/etc/pam.d/su”)
'''

#activity_code:KL/EP-19/A-002
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

configs=('/etc/passwd','/etc/shadow','/etc/pam.d/su') #declare a user-defined name
a=list(configs)                                       #using 'list' keyword covert the tuple into list
print(a)                                              

