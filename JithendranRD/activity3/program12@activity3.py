#Question12_activity3

"""
12. A. How to test if a specific value exists in a set?
B. Given set is s={10,1.23,’data’}
How to add following items to an existing set

I. Host=”host01”
II. L=[“host02”,”host01”,”host03”]
"""

#activity_code:KL/EP-19/A-003
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

'''A. How to test if a specific value exists in a set?'''
s={10,20,30,40,50}
if 20 in s:
    print('20 exists')
else:
    print('20 not exists')


'''B. Given set is s={10,1.23,'data'}
      How to add following items to an existing set 
      I. Host="host01"
      II. L=["host02","host01","host03"]

'''
s={10,1.23,'data'}
Host="host01"
L=["host02","host01","host03"]
s.add(Host)
for a in L:
    s.add(a)
print(s)




