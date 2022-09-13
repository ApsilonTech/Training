#Activity Code : KL/EP-19/A-002
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#TOPICS: LIST/TUPLE
#Dated: 13/09/2022


#14. What Is The Output Of The Following Python Code Fragment? Justify
  #Your Answer.
    #A. list = ['a','b','c','d','e']
    #   print (list[10:])

''' It shows as empty list [] because it working as list slicing '''
    
    #B. for var in ["mon","tue","wed","Thu","Fri"]:
    #       if (var == "wed"):
    #           continue
    #       else:
    #           print(var)

''' It will print mon, tue, thu, fri but won't print wed because on
if statement we mentioned continue on wed that's why it omitted wed.'''

    #C. Logfiles = ("Test1.log","Test2.log","Test3.log","Test4.log")
    #   if("Test2.log" not in Logfiles):
    #       print("Found")
    #   else:
    #       print("NOT-FOUND")

''' Output will be as "NOT-FOUND" because "Test2.log" is there in Logfiles
list but we asking it as is not there? that's why it shows as false'''
    
    #D. v="root:x:/bin/bash-123:text:bin:text"
    #   v.split("/")[-1]

''' Here we are splitting the string value according to / after that
it will be created as separate value in list on that we are mentioning to
print the last value'''
    
    #E. weekdays = ['sun','mon','tue','wed','thu','fri','sun','mon','mon']
    #   print (weekdays.count('mon'))

''' Here we are trying to count no. of mon in the list for that we are
using the keyword as count and within the parentheses we will mention
the what value it should count then it will perform and shows the counted value'''

    #F. testList = [1, 3, 5]
    #   testList.sort (reverse=True)
    #   print(testList)

''' Here we are trying to reverse the value what given in list by using sort
keyword and with the command as reverse=True which will print the value in
decending order. '''
