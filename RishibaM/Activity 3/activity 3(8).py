#activity code:KL/EP-19/A-003
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:03.10.2022

#8.Write a python program – modify the above program (host.py) 
#Step 1: read a hostname from <STDIN> 
#Step 2: Use membership operator to test whether the input 
#hostname already exists or not.
#Step 3: if it’s exists already, display pop up message “Sorry your 
#input hostname is exists”.

d={}
i=0
while i <5:
    hn=input ("enter host name:")
    ip =input("enter IP address:")
    d[hn]=ip
    i+=1
for var in d:
    print("keys:{}\t values:{}".format(var,d[var]))
    print()
    hn1=input("enter host name:")
if hn1 in d:
    print("sorry,input hostname already exists")
else:
        print("enter host name not in dictionary so add to it")
        ip=input("enter ip address:")
        d[hn]=ip
print(d)
