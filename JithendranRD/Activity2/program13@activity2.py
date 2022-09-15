#Question13_activity2
"""
Write a python script
Files=(“p1.log”,”p2.log”,”p3.log”,”p4.log”,”p5.log”)
Display all the files following format
Output:-
1. p1.log
2. p2.log
3. p3.log
4. p4.log
5. p5.log

Total No.of log files are: 5
"""

#activity_code:KL/EP-19/A-002
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

Files=('p1.log','p2.log','p3.log','p4.log','p5.log')
L=list(Files)
a=0
for var in Files:
    a+=1
    print(a,".",var)
print("Total no. of log files are: ", a)

       
