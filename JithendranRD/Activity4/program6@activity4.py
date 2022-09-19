#question6_activity
"""
Identify the following errors, correct the below codes

def fx(a,b=0,*c,**d,e=None):
print(“Hello”)
fx(10)


The error will be a syntax error because 'e' is a default argument defined
after a keyword argument.
If we delete the parameter 'e' then the output will be "Hello"
"""

#activity_code:KL/EP-19/A-004
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

def fx(a,b=0,*c,**d):
    print("Hello")
fx(10)

