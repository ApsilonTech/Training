#Question7_activity4
"""
def fx(*a):
print(a)
fx(db=’sqlite3’,usr=’root’,IP=’10.20.30.40’)
_____________________________________________________________________________________
OUTPUT:
error will be displayed as "TypeError: fx() got an unexpected keyword argument 'db'
because, fx() here is a variable length args.so it will not consider the keywords
like db, usr, IP.So delete the keywords (OR)
change the var len args into keyword
function call...Eg.fx(**a)
______________________________________________________________________________________
"""
#activity_code:KL/EP-19/A-004
#platform: python 3.10,winx 10
#Author:Mr.Jithendran
#Role:Software Engineer

def fx(*a):
    print(a)
fx('sqlite3','root','10.20.30.40')
        #OR

def fx(**a):
    print(a)
fx(db='sqlite3',usr='root',IP='10.20.30.40')
