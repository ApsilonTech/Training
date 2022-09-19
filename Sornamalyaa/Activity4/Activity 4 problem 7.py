#Activity Code : KL/EP-19/A-004
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: FUNCTIONS
#Dated: 19/09/2022


#Q7.
def fx(*a):
 print(a)
fx(db='sqlite3',usr='root',IP='10.20.30.40')


''' Output will be as TypeError because in function call we are trying to
give it as dictionary type value but in function definition we mentioned
it as variable length argument(*a) instead of keyword argument(**a) so
it unable to accept value. '''
