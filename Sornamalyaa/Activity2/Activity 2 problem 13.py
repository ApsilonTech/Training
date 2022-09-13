#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 13/09/2022


#13. Write a python script
     #Files=("p1.log","p2.log","p3.log","p4.log","p5.log")
     #Display all the files following format
     #Output:-
       #1. p1.log
       #2. p2.log
       #3. p3.log
       #4. p4.log
       #5. p5.log
     #Total No.of log files are: 5

Files=("p1.log","p2.log","p3.log","p4.log","p5.log")
num=0
for val in Files:
    num+=1
    print("{}.".format(num),val)
print("Total no. of log files are: ", num)
