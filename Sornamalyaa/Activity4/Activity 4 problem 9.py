#Activity Code : KL/EP-19/A-004
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: FUNCTIONS
#Dated: 19/09/2022


#Q9.
Fname="p1.log"
def fx():
    print(Fname)
    Fname="p2.log"
    print(Fname)
fx()
print(Fname)

''' Output will be as Unboundlocalerror because in function the print statement
tries get the value from global part without declaring the keyword.'''
