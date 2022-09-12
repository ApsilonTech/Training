#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 12/09/2022


#4. From Given tuple how to remove \n chars
    # T=("D1\n", "D2\n", "D3\n", "D4\n", "D5\n")


T=("D1\n", "D2\n", "D3\n", "D4\n", "D5\n")
lst=[]
for val in T:
    l= val.strip()
    lst.append(l)
print(tuple(lst))
