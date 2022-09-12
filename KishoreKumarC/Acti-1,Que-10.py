#Activity Code: KL/EP-19/A-001
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 12/09/2022

"""Question number-10:

Write a python program:
    a.Read student name and 3 subject marks from STDIN(keyboard).
    b.Calculate sum and average of 3 subjects.
    c.Using membership operator,test whether a character 'x' is found in the input
      string."""

name=str(input("Enter student name:")) #declare 'name' as variable name and get input from user using runtime
Maths=int(input("Enter Maths mark:")) #get maths mark from user using runtime input.
Science=int(input("Enter Science mark:"))#get science mark from user using runtime input
Social=int(input("Enter Social mark:"))#get social mark from user using runtime input.
total=Maths+Science+Social #sum of 3 subjects
average=total/3 #average of 3 subjects
print("Name:",name,"\nMaths:",Maths,"\nScience:",Science,"\nSocial:",Social,"\nTotal marks is:",total,"\nAverage of three subject is:",average)
#it displays the output of name,3 subject marks,total,average.
