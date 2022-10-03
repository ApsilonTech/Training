#activity code:KL/EP-19/A-003
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#5. Given dictionary
#conf={"f1":"/etc/passwd","f2":"/etc/group",
#"f3": "/etc/sysconfig","f4":None
#}
#a. Determine the size of conf dictionary
#b. Add new configuration file (/etc/pam.d)
#c. Using keys() and get() display key,value details


conf={"f1":"/ect/passwd","f2":"/ect/group","f3":"/ect/sysconfig","f4":None}
print(len(conf))
conf["f4"]="/ect/pam.d"
for var in conf:
    print("keys:{}\t values:{}".format(var,conf.get(var)))
