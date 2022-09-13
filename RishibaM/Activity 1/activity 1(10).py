#activity code:KL/EP-19/A-001
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:13.09.2022

#10. Write a python program:
#a. Read a student name and 3 subject marks from STDIN (keyboard)
#b. Calculate sum and average of 3 subjects.
#c. Display all the details (name, subject, total, average) to monitor.
#Note: using single print ()

sn=input("enter the student name")
a=int(input("enter the tamil mark"))
b=int(input("enter the english mark"))
c=int(input("enter the science mark"))
sum=a+b+c
d=sum/3
print("student name:{}\ntamil mark:{}\nenglish mark:{}\nscience mark:{}\ntotal mark:{}\naverage mark:{}".format(sn,a,b,c,sum,d))
