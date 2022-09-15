#Activity Code: KL/EP-19/A-002
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 13/09/2022

"""Question number-4:

From Given tuple how to remove \n chars
T = (“D1\n”,”D2\n”,”D3\n”,”D4\n”,”D5\n”)"""

T=("D1\n", "D2\n", "D3\n", "D4\n", "D5\n") #given tuple
lst=[] #creating empty list
for i in T: #using for loop giving T as i
    l= i.strip() #strip is used to remove the \n
    lst.append(l) #append used to add values in list
print(tuple(lst)) #keyword tuple will show the values in tuple
