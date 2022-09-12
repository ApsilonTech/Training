#Question11_activity1
'''
a. Read a business enquiry number from STDIN
b. Test whether your enquiry number ranges between 500 - 600. If matched, read a 
quotation number
c. If your quotation number ranges between 550 -650, read a customer name and 
check whether it matches with any of the following- "IBM" , "ORACLE" 
,"HP","KLABS". If so, read PO number from STDIN.
d. If customer name matches, Read a PO number & Test whether it ranges between 
500-1000.
e. If input PO matches, display all your business input details (enquiry number, 
quotation number, customer name, PO Number)
g. If any of the condition fails script won't take next input.
Write suitable invalid message if condition is not matched.
'''
#Activity-code: KL/EP-19/A-001
#Platform: python 3.10,winx 10
#author name="mr.JITHENDRAN"
#Role: Software Engineer, Apsilon



en_num=(int(input('enter your business enquiry number: ')))    #Declare a var name as en_num(business enquiry number) and get input from the user
if en_num>500 and en_num<600:                                   #using 'if' condition check whether the en_num value is >500 and <600, if true declare next variable
    q_num=(int(input('enter your quatation number: ')))         #Declare a var name q_num(quotation number) and get input from the user
    if q_num>550 and q_num<650:                                 #using 'if' condition check whether the q_num value is >550 and <650, if true declare the next variable
        name=(input('customer name: '))                         #Declare a var name as name(customer name)and get input from the customer.
        if name==('oracle' or 'ibm' or 'hp' or 'klabs'):        #using if condition check whether the entered name is as given in the question, if true declare the next variable.
            po_number=(int(input('enter your PO number: ')))    #declare a var name as PO_number and get input from the user.
            if po_number>500 and po_number<1000:                #using 'if' condition check whether the po_number is >500 and <1000, if true print the details we need to display.
              print('')  
              print("enquiry number: ",en_num,"\nquatation number: ",q_num,"\ncustomer name: ",name,"\nPO number: ",po_number)
            else:
                print("PO number out of range")                 #using 'else' condition ,print the message you need to display if the po_number is not in range.
        else:
            print("customer name not matched")                  #using 'else' condition ,print the message you need to display if the name is not matched.
    else:
        print("quatation number out of range")                  #using 'else' condition ,print the message you need to display if the q_num is not in range.
else:
    print("business enquiry number out of range")               ##using 'else' condition ,print the message you need to display if the en_num is not in range.

