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


#Q2. Modify the above program (p1.py) and save it as p2.py 
# Step 1: create an empty list
# Step 2: append the user input to the list
# Step 3: once the user is done with all three attempts, give the user
# choice to view the inputs entered from list.


#Q3. Modify the above program (p1.py) and save it as p3.py
# Step 1: Create a new file in append mode.
# Step 2: Write all user inputs to the file created
# Step 3: Once the user is done with all three attempts, give the user 
# choice to view the inputs entered from file. (Reading from file)


pin=12345
count=0
i=0
AH=open("E:\\python\\python-Activity-5\\pinlist2.txt","a")
while (i<3):
    pin_no= int(input("Enter pin number: "))
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
    AH.write('%s\n' %str("Your pin is blocked"))    #Because write part in file handling always accept str values not others
      #In notepad if you want values in newlines then you use this method only('%s\n' %var_name)
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

                                #     (or)

'''
pin=12345
p_list=[]
count=0
i=0
while (i<3):
    pin_no= int(input("Enter pin number: "))
    p_list.append(pin_no)
    count+=1
    if pin == pin_no:
        print("Pin number is matched at {} count".format(count))
        break
    else:
        print("Your have only {} chance to enter pin".format(3-count))
    i+=1
else:
    print("Your pin is blocked")
AH=open("E:\\python\\python-Activity-5\\pinlist.txt","a")
for var in p_list:              #Because write part in file handling always accept str values not others
    AH.write('%s\n' %str(var))  #In notepad if you want values in newlines then you use this method only('%s\n' %var_name)
AH.close()

print("Press 1 to view the inputs given")
print("Else enter 'exit' to get exit from site")
val=input("Enter details to go: ")
if val=='1':
    print("Input Detail: ",p_list)
elif val=='exit':
    print("Thank you for visiting")

'''
        
