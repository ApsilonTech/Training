#activity code:KL/EP-19/A-003
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#12. A. How to test if a specific value exists in a set?
 #B. Given set is s={10,1.23,’data’}
#How to add following items to an existing set 
#I. Host=”host01”
#II. L=[“host02”,”host01”,”host03”]

#a.
s1={36,15,25,46,45}
if 36 in s1:
    print("36 is  existing in set")
else:
    print("36 is not existing in set")

#b.
 s={10,1.23,'data'}
Host="host01"
L=["host02","host01","host03"]
s.add(Host)
for var in L:
    s.add(var)
    print(s)   
