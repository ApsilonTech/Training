#Question12_activity1

'''
s='1A2B3C45d6e7'
calculate the sum of digits
note: use for loop and isdigit() method
'''
#Activity-code: KL/EP-19/A-001
#Platform: python 3.10,winx 10
#author name="mr.JITHENDRAN"
#Role: Software Engineer, Apsilon




s='1A2B3C45d6e7'     #declare a variable 's'
a=0                  #declare a variable accordingly
for i in s:          #using for loop test the 'i'condition
    if i.isdigit():  #using 'if' condition check whether the 'i' has number values or not
        a+=int(i)    #increment operator can be used and mention it as integer
print('the sum of digits is : ',a)        #print the sum of digits and declare a.
