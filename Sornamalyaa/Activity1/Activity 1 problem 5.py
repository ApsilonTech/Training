#Activity Code : KL/EP-19/A-001
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#Dated: 12/09/2022


#10. Write a python program:
     #a. read a student name and 3 subject marks from STDIN (keyword)
     #b. calculate sum and average of 3 subjects.
     #c. display all the details (name, subject, total, average) to monitor.
   #note: using single print()

sn= input("Enter Student name: ")
a=int(input("Enter the Tamil subject marks: "))
b=int(input("Enter the English subject marks: "))
c=int(input("Enter the Maths subject marks: "))
sum=a+b+c
avg=sum/3
print("Student name: {} \nTamil marks: {} \nEnglish marks: {} \nMaths marks: {} \nTotal marks scored: {} \nAverage marks got: {}".format(sn,a,b,c,sum,avg))

