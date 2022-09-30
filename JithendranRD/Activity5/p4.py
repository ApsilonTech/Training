'''
Q3. Modify the above program (p1.py) and save it as p3.py
Step 1: Create a new file in append mode.
Step 2: Write all user inputs to the file created
Step 3: Once the user is done with all three attempts, give the user
choice to view the inputs entered from file. (Reading from file)
'''
#activity_code:KL/EP-19/A-005
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer 

pin=1234
a=1
List=[]
count=0
import time
while a<=3:
    pin_entry=int(input("Enter Your Pin Number:"))
    List.append(pin_entry)
    count+=1
    FH=open("D:\\python workout\\Activity5\\pintest1.txt",'a')
    FH.write("%s\n" %str(pin_entry))
    if (pin==pin_entry):
        print("Pin Number is matched at count time",count)
        FH.write("%s\n" %str("Pin Number is matched at count time",count))
        break
    a+=1
else:
    print("your pin is blocked")
    #FH.write("%s\n" %str("your pin is blocked"))
Time=time.ctime()
print(Time)
FH.write('%s\n' %str(Time))
FH.close()
       
RH=open("D:\\python workout\\Activity5\\pintest1.txt")
Read=RH.read()
while a in List:
    print("Thank you")
    break
while a not in List:
    print("Enter '1' to view your attempts")
    print("Enter '2' to exit")
    choice=int(input("Enter your choice:"))
    if (choice==1):
        print("Your attempted pins:\n",Read)
        break
    elif (choice==2):
        print()
        break
RH.close()
























