#activity code:KL/EP-19/A-002
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:16.09.2022

#10. Write a python program
#Given tuple
#Products=(“P1”,”P2”,”P3”,”P4”,”P5”)
#display the list of products except P2 and P3 
#Note : use for loop statement

produts=("p1","p2","p3","p4","p5")
for var in produts:
    if(var=="p2"or var=="p3"):
        continue
    else:
        print(var)
    
    
