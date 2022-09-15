#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 13/09/2022


#15. Identify the errors in the below codes
     #a.var = ("/etc/passwd","/etc/pam.d","/var/log/")
     #  var.append("/etc/groups")

''' Here it shows as an attribute error because in tuple we unable to
make changes in the given tuple elements. ''' 
     
     #b. cmd = ["git","-a","branch","-C"]
     #   cmd[5]

''' It will shows as index error because index value given is out of index''' 
    
     #c. emptylist = []
     #  emptylist.append("Data1","Data2")

''' It will shows as an error becuase in list, if we trying to append value
means at a time we are able to give only one value using append that's why it
shows as an error. '''
     
     #d. S1 = "testing data"
     #   del(S1[2])

''' As mentioned it will be suitable in list but not in string that's
why it shows as Type Error'''
     
     #e. "ab" not in "abcd"

''' Here it will not display any thing because if we give print only
it will shows output as False otherwise it give null display.'''
