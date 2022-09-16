#activity code:KL/EP-19/A-002
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:16.09.2022

#4. From Given tuple how to remove \n chars 
#T = (“D1\n”,”D2\n”,”D3\n”,”D4\n”,”D5\n”)


T=("D1\n","D2\n","D3\n","D4\n","D5\n")
ls=[]
for var in T:
    l=var.strip('\n') #remove\n
    ls.append(l)  #add the list value
print(tuple (ls))
