#Question6_activity3
'''
6. Given dict structure
Proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}
using pop() - delete 'fs' and 'sh' key entries
using del() - delete 'pid' and 'user' entries
# what's the difference between pop() and del()
using popitem() - delete Proc structure
'''

#activity_code:KL/EP-19/A-003
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer


Proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}
Proc.pop('fs')   
Proc.pop('sh')
del(Proc['pid'])
del(Proc['user'])
print(Proc) #nothing will appear exept {}, because we deleted it using pop() and del()
Proc.popitem()
print(Proc) #will display an error because Proc is empty as we deleted it
