#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 12/09/2022


#6. Write a python program
    #Step 1: create an empty list
    #step 2: display size of list
    #step 3: use while loop 5 times
          #i) To read a hostname from <STDIN>
          #ii) To add an input hostname to existing list
    #step 4: using for loop, display list of elements
    #step 5: display size of the list

lst=[]
print("Size of the list before adding value: ",len(lst))
i=0
while i<5:
    hn=input("Enter the host name: ")
    lst.append(hn)
    i+=1
for var in lst:
    print(var)
print("Size of the list after adding value: ",len(lst))
