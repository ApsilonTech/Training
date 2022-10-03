#activity code:KL/EP-19/A-002
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:19.09.2022

#15. Identify the errors in the below codes
  #a.var = ("/etc/passwd","/etc/pam.d","/var/log/")
  #var.append("/etc/groups")
'''
attributeerror 'tuple' is immutable
'''
  #b.cmd = ["git","-a","branch","-C"]
  #cmd[5]
'''output will be index error because index is not found in list'''
  #c. emptylist = []
  # emptylist.append(“Data1”,”Data2”)
'''The append in only one argument not 2'''  
  #d. S1 = ”testing data”
  #del(S1[2])
'''output wil be name error because "s1"is not defined'''
  #e. “ab” not in “abcd"
'''value will not print when we didnot given print'''
