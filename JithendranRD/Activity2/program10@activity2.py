#Question10_activity2
"""
Write a python program
Given tuple
Products=(“P1”,”P2”,”P3”,”P4”,”P5”)
display the list of products except P2 and P3

Note : use for loop statement
"""

#activity_code:KL/EP-19/A-002
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

products=('p1','p2','p3','p4','p5')
l=list(products)
l2=[]
for a in l:
    if (a=='p2' or a=='p3'):
        del(a)
    else:
        l2.append(a)
        print(a)
   
