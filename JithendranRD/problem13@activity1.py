#Question13_activity1
'''
s='welcome'
Filter list of vowels and count number of vowels from given string
'''


#Activity-code: KL/EP-19/A-001
#Platform: python 3.10,winx 10
#author name="mr.JITHENDRAN"
#Role: Software Engineer, Apsilon

s='welcome'       #declare a variable 's' and 'welcome' in it.
a=0               
for x in s:       
    if x=="a" or x=="e" or x=="i" or x=="o" or x=="u":
        print("vowels in s : ",x)
        a+=1
print("no.of vowels in s: ",a)
