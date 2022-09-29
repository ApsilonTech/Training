#Activity Code : KL/EP-19/A-005
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#Dated: 20/09/2022


#Q5. Modify the above program (p4.py) and save it as p5.py
#Step 1: create a user defined function named pin_test and place the entire 
#p4.py code as function definition
#Step 2: from main script, make a function call to pin_test.

import time
def pin_test():
    pin=12345
    p_list=[]
    count=0
    i=0
    AH=open("E:\\python\\python-Activity-5\\pinlist3.txt","a")
    while (i<3):
        pin_no= int(input("Enter pin number: "))
        p_list.append(pin_no)
        AH.write('%s\n' %str(pin_no))
        count+=1
        if pin == pin_no:
            print("Pin number is matched at {} count".format(count))
            AH.write('%s\n' %str("Pin number is matched at {} count".format(count)))
            break
        else:
            print("Your have only {} chance to enter pin".format(3-count))
            AH.write('%s\n' %str("Your have only {} chance to enter pin".format(3-count)))
        i+=1
    else:
        print("Your pin is blocked")
        AH.write('%s\n' %str("Your pin is blocked"))
    
    c=time.ctime()
    print(c)
    AH.write('%s\n' %str(c))
    
    AH.close()

    Read_h=open("E:\\python\\python-Activity-5\\pinlist2.txt")
    r_handle=Read_h.read()

    print("Press 1 to view the inputs given")
    print("Else enter 'exit' to get exit from site")
    val=input("Enter details to go: ")
    if val=='1':
        print("Input Detail: ",r_handle)
    elif val=='exit':
        print("Thank you for visiting")
    Read_h.close()
pin_test()



