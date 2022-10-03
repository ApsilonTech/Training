#activity code:KL/EP-19/A-005
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#Q4. Modify the above program (p3.py) and save it as p4.py
#Step 1: using ctime() from time module, capture the date/time along with 
#the user input and write it to the file as well.
#Step 2: once the user is done with all three attempts, give the user choice 
#to view the inputs entered from file. (Reading from file)

import time
pnumber=3456
L=[]
count=0
i=0
FH=open("D:\\file.txt","a")
while(i<3):
    p=int(input("enter a pin:"))
    L.append(p)
    FH.write('%s\n' %str(p))
    count+=1
    if(p==pnumber):
        print("success is matched at {} time.".format(count))
        FH.write('%s\n' %str("success is matched at {} time.".format(count)))
        break
    else:
        print("you have {} chance.".format(count+1))
        FH.write('%s\n' %str("you have {} chance.".format(count+1)))
    i=i+1
else:
    print("your pin is blocked")
    FH.write('%s\n' %str("your pin is blocked"))  
    
c=time.ctime()
print(c)
FH.write('%s\n' %str(c))

FH.close()

var =open("D:\\file.txt")
p2read=var.read()
print("if you want to see entered input enter ok")
print("if you don't want to see entered input enter exit")
p1=input("enter the value ")
if p1=="ok":
    print("input value:",p2read)
elif p1=="exit":
    print("Thank you")
var.close()
         
