#activity code:KL/EP-19/A-003
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#6. Given dict structure
#Proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}
#using pop() - delete 'fs' and 'sh' key entries
#using del() - delete 'pid' and 'user' entries
# what's the difference between pop() and del()
#using popitem() - delete Proc structure

proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}
proc.pop('fs')
proc.pop('sh')
del(proc['pid'])
del(proc['user'])
print(proc)
proc.popitem()
print(proc)
