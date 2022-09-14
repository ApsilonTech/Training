#Activity Code : KL/EP-19/A-003
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: DICTIONARY/SET
#Dated: 14/09/2022


#5. Given dictionary
    #conf={"f1":"/etc/passwd","f2":"/etc/group",
    #      "f3": "/etc/sysconfig","f4":None}

    #a. Determine the size of conf dictionary
    #b. Add new configuration file (/etc/pam.d)
    #c. Using keys() and get() display key,value details


conf={"f1":"/etc/passwd","f2":"/etc/group",
      "f3": "/etc/sysconfig","f4":None}
print(len(conf))
conf["f4"]="/etc/pam.d"
#print(conf)
for i in conf: #Here we are trying to print keys and values separately
    print("keys: {} \t values: {}".format(i,conf.get(i)))
