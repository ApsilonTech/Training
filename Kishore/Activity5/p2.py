#Activity Code: KL/EP-19/A-005    
#Platform: Python 3.10,windows 10 
#Author: Mr.Kishore Kumar C       
#Role: Software Engineer, Apsilon.
#Date: 19/09/2022                 

# Question number-2:

""" Modify the above program (p1.py) and save it as p2.py 
 Step 1: create an empty list
 Step 2: append the user input to the list
 Step 3: once the user is done with all three attempts, give the user
 choice to view the inputs entered from list. """


pin_number=1234
a=1
List=[]
while a<=3:
    pin=int(input("Enter Your Pin Number:"))
    List.append(pin)
    if (pin_number==pin):
        print("Pin Number is matched at count time")
        break
    a+=1
else:
    print("your pin is blocked")
while a in List:
    print("Thank you")
    break
while a not in List:
    print("1.View Entered Pins")
    print("2.Exit")
    choice=int(input("Enter your choice:"))
    if (choice==1):
        print("Your entered pins were",List)
        break
    elif (choice==2):
        print("Thankyou")
        break









    
