#Activity Code: KL/EP-19/A-003    
#Platform: Python 3.10,windows 10 
#Author: Mr.Kishore Kumar C       
#Role: Software Engineer, Apsilon.
#Date: 16/09/2022                 

""" Question number-12:


A. How to test if a specific value exists in a set?
B. Given set is s={10,1.23,’data’}
How to add following items to an existing set 
I. Host=”host01”
II. L=[“host02”,”host01”,”host03”] """



s1={1,2,3,4,5,6,7}
if 7 in s1:
    print("7 is exist")
else:
    print("7 is not exist")

   
s={10,1.23,'data'}
Host="host01"
L=["host02","host01","host03"]
s.add(Host)
for i in L:
    s.add(i)
print(s)
