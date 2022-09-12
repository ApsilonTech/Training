#Activity Code: KL/EP-19/A-001
#Platform: Python 3.10,windows 10
#Author: Mr.Kishore Kumar C
#Role: Software Engineer, Apsilon.
#Date: 12/09/2022

"""Question number-11:

Write a python program:
    a. Read a business enquiry number from STDIN
    b. Test whether your enquiry number ranges between 500 - 600. If matched, read a 
       quotation number
    c. If your quotation number ranges between 550 -650, read a customer name and 
       check whether it matches with any of the following- "IBM" , "ORACLE",
       "HP","KLABS". If so, read PO number from STDIN.
    d. If customer name matches, Read a PO number & Test whether it ranges between 
       500-1000.
    e. If input PO matches, display all your business input details (enquiry number, 
       quotation number, customer name, PO Number)
    g. If any of the condition fails script won't take next input.
       Write suitable invalid message if condition is not matched."""



print("Enter Business enquiry number from 500 to 600")
number=int(input("Business enquiry number:")) #get number from user using runtime input 

if number>500 and number<600: #True block statement set range from 500 to 600
    print("Enter quotation number from 550 to 650") #it shows the output
    quo_number=int(input("Enter the quotation number:"))#get number from user using runtime input 

    if quo_number>550 and quo_number<650:#True block statement set range from 550 to 650
        print("Customer names ibm,orcle,hp,klabs")#it shows the output
        cust_name=str(input("Enter customer name:"))#get name from user using runtime input
   
        
        if cust_name==('ibm') or cust_name==('orcle') or cust_name==('hp') or cust_name==('klabs'):#if any of these names matches it will take user to next step
            print("Enter PO number from 500 to 1000")#it shows the output
            po_number=int(input("Enter PO number:"))#get number from user using runtime input
       
            if po_number>500 and po_number<1000:#True block statement set range from 500 to 1000 to move next step
                print("Business enquiry number is:",number,"\nQuotation number is:",quo_number,"\nCustomer name is:",cust_name,"\nPO is:",po_number)
            else:#false block statement if it not matches with true block is shows output of false block
                print("PO number is not within range")#output of false block
        else:
            print("Customer name is not matched")#output of false block
    else:
        print("Quotation number is not within range")#output of false block
else:
    print("Business enquiry number is not matched")#output of false block
