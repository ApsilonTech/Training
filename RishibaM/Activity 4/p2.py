#activity code:KL/EP-19/A-005
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#Q2. Modify the above program (p1.py) and save it as p2.py 
#Step 1: create an empty list
#Step 2: append the user input to the list
 #Step 3: once the user is done with all three attempts, give the user
 #choice to view the inputs entered from list.

L=[]
pnumber=3456
count=0
i=0
while(i<3):
    p=int(input("enter a pin:"))
    L.append(p)
    count=count+1
    if(p==pnumber):
        print("success is matched at {} time.".format(count))
        break
    else:
        print("you have {} chance.".format(count+1))
    i=i+1
else:
     print("your pin is blocked") 
print(L)
print("if you want to see entered input enter ok")
print("if you don't want to see entered input enter exit")
p1=input("enter the value ")
if p1=="ok":
    print(L)
elif p1=="exit":
    print("Thank you")
