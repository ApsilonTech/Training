#Activity Code : KL/EP-19/A-003
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: DICTIONARY/SET
#Dated: 14/09/2022


#11. Predict the result of below set operations 
S1={'data1','data2','data3'}
S2={'data2','data3','data4','data5'}
print(S1-S2)   #Difference: see only unique value in s1 when compare to s1 and s2
print(S2-S1)   #            see only unique value in s2 when compare to s1 and s2
print(S1 ^ S2) #Symmetric difference: print unique values available in s1 and s2

''' o/p:
{'data1'}
{'data4', 'data5'}
{'data5', 'data1', 'data4'}
'''
