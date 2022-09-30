#Activity Code: KL/EP-19/A-005    
#Platform: Python 3.10,windows 10 
#Author: Mr.Kishore Kumar C       
#Role: Software Engineer, Apsilon.
#Date: 19/09/2022                 

# Question number-1:

"""Write a program:

Step 1: create a file name p1.py
Step 2: declare & initialize the pin number (ex: pin=1234)
Step 3: Use while loop to iterate following statement thrice
(i) Read a pin number from <STDIN>
(ii) Compare a input pin with existing pin number
(iii) If both pin numbers are matched, display pin number is matched at count 
 time & exit from loop.
(iv) If all 3 attempts fails, display message “your pin is blocked."""


pin_number=1234
a=1
while a<=3:
    pin=int(input("Enter Your Pin Number:"))
    if (pin_number==pin):
        print("Pin Number is matched at count time")
        break
    a+=1
else:
    print("your pin is blocked")































    
