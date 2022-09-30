#Question2_activity
"""
Modify the above program (p1.py) and save it as p2.py
Step 1: create an empty list
Step 2: append the user input to the list
Step 3: once the user is done with all three attempts, give the user
choice to view the inputs entered from list.
"""
#activity_code:KL/EP-19/A-005
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

pin=1234
L=[]
a=0
while a<3:
    pin1=(int(input("enter your pin number: ")))
    L.append(pin1)
    a+=1
    if pin1==pin:
        print("Pin number matched at count time")
        break
else:
    print("")
    print("your pin is blocked")

    while a in L:
        print("")
        break
    while a not in L:
        print("")
        print("enter '1' to view your used choices")
        print("enter '2' for exit")
        enter=int(input("enter your choice: "))
        if enter==1:
            print("your choices were: ",L)
            break
        else:
            print("")
            break
    




