#Activity Code : KL/EP-19/A-003
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: DICTIONARY/SET
#Dated: 14/09/2022


#4. Write a python program
    #Given list structure
    #Employ = [ "e123,ram,sales,pune,1000",
    #       "e132,kumar,prod,bangalore,3423",
    #       "e456,arun,prod,chennai,2456",
    #       "e544,vijay,hr,mumbai,6500" ]

    #a. create an empty dictionary and name it as Emp 
    #b. convert the above given list into dict format.
    #c. display list of key,value pairs from EMP dict
    #Note:- employee id as a key, emp name as value

Employ = [ "e123,ram,sales,pune,1000", "e132,kumar,prod,bangalore,3423",
        "e456,arun,prod,chennai,2456", "e544,vijay,hr,mumbai,6500"]
Emp={}
for val in Employ:
    val1 = val.split(",")
    #print(val1)
    Emp[val1[0]] = val1[1] #Here in Emp[val1[0]] square bracket[] is important
print(Emp)
print()
for i in Emp:     #Here i gets key of Emp dictionary
    print("Keys: {} \t Values: {}".format(i,Emp[i]))


        
            
