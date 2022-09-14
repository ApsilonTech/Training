#Activity Code : KL/EP-19/A-003
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: DICTIONARY/SET
#Dated: 14/09/2022


#7. Write a python program:
    #Step 1: create a new file host.py 
    #Step 2 : create an empty dict
    #Step 3 : use looping statements – 5times
             #i) Read a hostname from <STDIN>
             #ii) Read a IP-Address from <STDIN>
             #iii) Add a input details to existing dict
             #iv) with hostname as a key and IP address as it’s value
    #Step 4 : display Key/ value details to monitor 

dic={}
i=0
while i<5:
    hn=input("Enter host name: ")
    ip=input("Enter IP address: ")
    dic[hn]=ip
    i+=1
for val in dic:
    print("keys: {} \t values: {}".format(val,dic[val]))
print()

#8. Write a python program – modify the above program (host.py) 
    #Step 1: read a hostname from <STDIN> 
    #Step 2: Use membership operator to test whether the input 
            #hostname already exists or not.
    #Step 3: if it’s exists already, display pop up message “Sorry your 
            #input hostname is exists”.


hn2=input("Enter host name: ")
if hn2 in dic:
    print("Sorry, your input hostname already exists")
else:
    print("Entered host name not in dictionary so added to it")
    ip=input("Enter IP address: ")
    dic[hn]=ip
print(dic)
