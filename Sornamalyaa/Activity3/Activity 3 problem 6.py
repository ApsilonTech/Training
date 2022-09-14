#Activity Code : KL/EP-19/A-003
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: DICTIONARY/SET
#Dated: 14/09/2022


#6. Given dict structure
    #Proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}
    #using pop() - delete 'fs' and 'sh' key entries
    #using del() - delete 'pid' and 'user' entries
    # what's the difference between pop() and del()
    #using popitem() - delete Proc structure

Proc={'pid':12,'fs':'/proc','user':'root','sh':'/bin/bash'}
#using pop, if you give statement of pop in print then it will print the popped element
Proc.pop('fs')   
Proc.pop('sh')

#using del, it will delete the value of given key (or)
#if you just given the del(Proc) it will delete the whole dictionary elements
del(Proc['pid'])
del(Proc['user'])

print(Proc) #o/p as {} because using pop and del we removed all elements in dict.
print()

#using popitem() - special feature of this: it will delete the last element in the dictionary
Proc.popitem()
print(Proc) #shows as KeyError because dictionary is empty so popitem() will not work
