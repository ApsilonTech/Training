
#activity code:KL/EP-19/A-001
#platform:python 3.10.7
#author:M.Rishibha
#role:software engineer.apsilon
#date:14.09.2022

#11. Write a python program:
#a. Read a business enquiry number from STDIN
#b. Test whether your enquiry number ranges between 500 - 600. If matched, read a 
#quotation number
#c. If your quotation number ranges between 550 -650, read a customer name and 
#check whether it matches with any of the following- "IBM" , "ORACLE" 
#,"HP","KLABS". If so, read PO number from STDIN.
#d. If customer name matches, Read a PO number & Test whether it ranges between 
#500-1000.
#e. If input PO matches, display all your business input details (enquiry number, 
#quotation number, customer name, PO Number)
#g. If any of the condition fails script won't take next input.
#Write suitable invalid message if condition is not matched

en=int(input("enter a enqury number:"))
if(en>=500 and en<=600):
    qn=int(input("enter a quotation number:"))
    if(qn>550 and qn<=650):
        cn=(input("enter a customer name:"))
        if cn=="IBM" or cn=="oracle" or cn=="HP" or cn=="KLABS":
            po=int(input("enter a po number:"))
            if po>=500 and po<=1000:
                print("\n enqury number:{}\nquotation number:{}\ncustomer name:{}\npo number:{}".format(en,qn,cn,po))
            else:
                print("enter a po is not matched")
        else:
            print("enter a cn is not matched")
    else:
        print("enter a qn is not matched")
else:
    print("enter a en is not matched")

          
