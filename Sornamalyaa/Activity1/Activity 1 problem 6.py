#Activity Code : KL/EP-19/A-001
#Platform : Python 3.10.2, Windows 10
#Author: Sornamalyaa M
#Role : Software Engineer, Apsilon
#Dated: 12/09/2022


#11. write a python program
     #a. read a business enquiry number from STDIN
     #b. Test whether your enquiry numer rangea between 500-600. If matched,
   #read a quotation number
     #c. IF your quotatio numbert ranges between 550-650, read a customer name
   #and check whether it matches with any of the following- "IBM", "ORACLE",
   #"HP", "KLABS". If so, read PO number from STDIN
     #d. If customer name matches, Read a PO number & test whether it ranges
   #between 500-1000
     #e. If input PO matches, display all your business input details (enguiry
   #number, quotation number, customer name, PO number)
     #f.If any of the condition fails script won't take next input.
   #Write suitable invalid message if condition is not matched

en=int(input("Enter the enquiry number: "))
if en>=500 and en<=600:
    qn=int(input("Enter the quotation number: "))
    if qn>=550 and qn<=650:
        print("'Please enter customer name in UPPER CASE'")
        cn=input("Enter customer name: ")
        if cn=="IBM" or cn=="ORACLE" or cn=="HP" or cn=="KLABS" :
            po=int(input("Enter PO number: "))
            if po>=500 and po<=1000:
                print("\nEnquiry number: {} \nQuotation number: {} \nCustomer name: {} \nPO number: {}".format(en,qn,cn,po))
            else:
                print("Sorry, Entered PO number is not matched")
        else:
            print("Sorry, given customer name is not matched")
    else:
        print("Sorry, entered quotation number is not matched")
else:
    print("Sorry, entered enquiry number is not matched")
