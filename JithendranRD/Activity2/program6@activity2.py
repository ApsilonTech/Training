#Question6_activity2
'''
Write a python program:
Step 1: create an empty list
Step 2: display size of list
Step 3: use while loop 5 times
i) To read a hostname from <STDIN>
ii) To add a input hostname to existing list
Step 4: using for loop, display list of elements
Step 5: display size of the list
'''

#activity_code:KL/EP-19/A-002
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

l=[]                            #create a empty list
print(len(l))                   #print the size of the list
i=0                             
while i<5:                      #using while,declare the number of times the input should display
    host_name=(input("enter the hostname: "))#create a var named host_name
    l.append(host_name)                      #to add the host_name to 'l' use the append method
    i+=1
print(l)
for a in l:                     #using for loop display the name of the elements
    print(a)                     
print("size of the list is: ",len(l))
