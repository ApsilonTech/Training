#Activity Code : KL/EP-19/A-001
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#Dated: 12/09/2022


#13. Given string
     # S= 'welcome'
     # Filter list of vowels and count number of vowels from given string.

S= 'welcome'
count=0
for val in S:
    if  val=='a' or val=='e' or val=='i' or val=='o' or val=='u' or val=='A' or val=='E' or val=='I' or val=='O' or val=='U':
       print(val)
       count+=1
print("Total no. of vowels present in S string is ",count)
