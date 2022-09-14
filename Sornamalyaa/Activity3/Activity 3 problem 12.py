#Activity Code : KL/EP-19/A-003
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: DICTIONARY/SET
#Dated: 14/09/2022



#12.A. How to test if a specific value exists in a set?
'''
s1={12,23,34,45,56}
if 23 in s1:
    print("23 is existing in set")
else:
    print("23 is not existing in set")'''

   #B. Given set is s={10,1.23,'data'}
   #How to add following items to an existing set 
     # I. Host="host01"
     # II. L=["host02","host01","host03"]

'''
s={10,1.23,'data'}
Host="host01"
L=["host02","host01","host03"]
s.add(Host)
for val in L:
    s.add(val)
print(s)
'''
