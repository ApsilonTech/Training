#Question5_activity3
'''
5. Given dictionary
conf={"f1":"/etc/passwd","f2":"/etc/group",
"f3": "/etc/sysconfig","f4":None
}
a. Determine the size of conf dictionary
b. Add new configuration file (/etc/pam.d)
c. Using keys() and get() display key,value details
'''
#activity_code:KL/EP-19/A-003
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

conf={"f1":"/etc/passwd","f2":"/etc/group","f3": "/etc/sysconfig","f4":None}
print(len(conf))
conf['f4']=('/etc/pam.d')
for a in conf:
    print("keys:",a,"values:",conf.get(a))
