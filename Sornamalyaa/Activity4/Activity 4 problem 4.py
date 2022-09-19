#Activity Code : KL/EP-19/A-004
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: FUNCTIONS
#Dated: 19/09/2022


#Q4. 
def f1(*a,**b):
 print(type(a),type(b))
f1()

#a. <class ‘tuple’>   b. <class ‘tuple’> <class ‘dict’>   c. <class ‘dict’>

''' Output will be as <class ‘tuple’> <class ‘dict’> because in function
definition part

1st argument is as variable length argument (*a) which helps
to pass more values from function call to function so it consider as tuple.

2nd argument is as keyword argument (**b) which helps function call to
pass values in key and value pair wise so it considered as dictionary. '''
