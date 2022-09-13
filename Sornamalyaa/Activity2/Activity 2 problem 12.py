#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 13/09/2022


#12. Write a python program to iterate through the given list.
     #Given list
     #hosts=['host01','host02','host03','host04','host05']
     #Using membership operator test host03 exists or not
     #if 'host03' does not exists display suitable message to screen

hosts=['host01','host02','host03','host04','host05']
if 'host03' in hosts:
    print("'host03' is available in hosts list")
else:
    print("Sorry, 'host03' is not available in hosts list")
