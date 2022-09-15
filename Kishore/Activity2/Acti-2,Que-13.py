#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 14/09/2022

""" Question number-13:

Write a python script
Files=(“p1.log”,”p2.log”,”p3.log”,”p4.log”,”p5.log”)
Display all the files following format
Output:-
1. p1.log
2. p2.log
3. p3.log
4. p4.log
5. p5.log
Total No.of log files are: 5 """

Files=('p1.log','p2.log','p3.log','p4.log','p5.log')
a=0
for i in Files:
    a+=1
        
    print("{}.".format(a),i)                                          
print("Total No.of log files are:",len(Files))
    

