#Activity Code : KL/EP-19/A-004
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: FUNCTIONS
#Dated: 19/09/2022


#Identify the following errors, correct the below codes 

#Q6. 
def fx(a,b=0,*c,**d,e=None):
 print("Hello")
fx(10)


''' Output will be as Syntax error because e=None(default argument) is given
after keyword argument.

Giving arguments should be in order like required argument, default argument,
variable length argument  and keyword argument. If it exits it shows as
syntax error.'''
