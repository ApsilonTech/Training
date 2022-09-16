#Activity Code: KL/EP-19/A-003    
#Platform: Python 3.10,windows 10 
#Author: Mr.Kishore Kumar C       
#Role: Software Engineer, Apsilon.
#Date: 15/09/2022                 

""" Question number-6:

Given dict structure
Proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}
using pop() - delete 'fs' and 'sh' key entries
using del() - delete 'pid' and 'user' entries
# what's the difference between pop() and del()
using popitem() - delete Proc structure """

Proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}

Proc.pop('fs') #pop will remove the values
Proc.pop('sh')

del(Proc['pid']) #delete will delete the values
del(Proc['user'])


Proc.popitem() #pop item will remove the last item in dictionary
print(Proc) #we cannot popiems in dictionary because dictionary is empty

