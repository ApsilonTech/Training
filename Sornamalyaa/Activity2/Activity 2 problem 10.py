#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 12/09/2022


# 10. Write a python program
      #Given tuple
      #Products=("P1","P2","P3","P4","P5")
      #display the list of products except P2 and P3 
      #Note : use for loop statement

Products=("P1","P2","P3","P4","P5")
lst=list(Products)
l1=[]
for val in lst:
    if val == "P2" or val == "P3":
        del(val)
    else:
        l1.append(val)
print(l1)
        
