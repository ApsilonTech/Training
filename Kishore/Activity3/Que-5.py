#Activity Code: KL/EP-19/A-003
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 15/09/2022

"""Question number-5:

Given dictionary
conf={"f1":"/etc/passwd","f2":"/etc/group",
"f3": "/etc/sysconfig","f4":None
}
a. Determine the size of conf dictionary
b. Add new configuration file (/etc/pam.d)
c. Using keys() and get() display key,value details"""


conf={"f1":"/etc/passwd","f2":"/etc/group","f3": "/etc/sysconfig","f4":None}

print(len(conf))

conf["f4"]="/etc/pam.d"
print(conf)
for i in conf:
      print("keys: {} \t values: {}".format(i,conf.get(i)))
