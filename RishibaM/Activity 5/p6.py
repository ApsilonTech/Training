#activity code:KL/EP-19/A-005
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#In OS Command line 
#Duplicate p5.py file and save it as p6.py
#Note: p6.py must be loadable.
#In python shell, import p6.py file (module) and use help () to know about 
#p6 module invoke pin_test function do pin test

import time
def pin_test():
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
