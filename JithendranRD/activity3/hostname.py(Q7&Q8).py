#Question7_activity3
'''
7. Write a python program:
Step 1: create a new file host.py
Step 2 : create an empty dict
Step 3 : use looping statements – 5times
i) Read a hostname from <STDIN>
ii) Read a IP-Address from <STDIN>
iii) Add a input details to existing dict
iv) with hostname as a key and IP address as it’s value
Step 4 : display Key/ value details to monitor
'''

#activity_code:KL/EP-19/A-003
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

dictionary={}
a=0
while a<5:
    host_name=(input("enter the host name: "))
    ip_address=(input("enter the ip address: "))
    dictionary[host_name]=ip_address
    a+=1
for i in dictionary:
    print("keys:",i," values:",dictionary[i])


'''8. Write a python program – modify the above program (host.py)

Step 1: read a hostname from <STDIN>

Step 2: Use membership operator to test whether the input
hostname already exists or not.

Step 3: if it’s exists already, display pop up message “Sorry your
input hostname is exists”.   
'''

host_name=(input("enter the host name: "))
if host_name in dictionary:
    print("sorry your input hostname already exists")
