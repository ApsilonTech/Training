#Activity Code : KL/EP-19/A-005
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#Dated: 19/09/2022


#Q1. Write a program:
#Step 1: create a file name p1.py
#Step 2: declare & initialize the pin number (ex: pin=1234)
#Step 3: Use while loop to iterate following statement thrice
#(i) Read a pin number from <STDIN>
#(ii) Compare a input pin with existing pin number
#(iii) If both pin numbers are matched, display pin number is matched at count 
 #time & exit from loop.
#(iv) If all 3 attempts fails, display message “your pin is blocked."

pin=12345
count=0
i=0
while (i<3):
    pin_no= int(input("Enter pin number: "))
    count+=1
    if pin == pin_no:
        print("Pin number is matched at {} count".format(count))
        break
    else:
        print("Your have only {} chance to enter pin".format(3-count))
    i+=1
else:
    print("Your pin is blocked")

