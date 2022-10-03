#activity code:KL/EP-19/A-005
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#Q1. Write a program:
#Step 1: create a file name p1.py
#Step 2: declare & initialize the pin number (ex: pin=1234)
#Step 3: Use while loop to iterate following statement thrice
#(i) Read a pin number from <STDIN>
#(ii) Compare a input pin with existing pin number
#(iii) If both pin numbers are matched, display pin number is matched at count 
 #time & exit from loop.
#(iv) If all 3 attempts fails, display message “your pin is blocked.”


pnumber=3456
count=0
i=0
while(i<3):
    p=int(input("enter a pin:"))
    count=count+1
    if(p==pnumber):
        print("success is matched at {} time.".format(count))
        break
    else:
        print("you have {} chance.".format(count+1))
    i=i+1
else:
     print("your pin is blocked") 
        
