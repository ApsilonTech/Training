#Question10_activity1
'''
a)Read a student name and 3 subject marks from STDIN(keyboard)
b)Calculate sum and average of 3 subjects.
c)Display all the details(name, subject, total, average)to monitor.
"note: Using single print()
'''
#Activity-code: KL/EP-19/A-001
#Platform: python 3.10,winx 10
#author name="mr.JITHENDRAN"
#Role: Software Engineer, Apsilon




stud_name=(input('enter student name : '))  #student_name is a variable declared and get input from user input
sub=3                                       #no of subjects given is 3
sub_1=(int(input('enter subject1 mark : ')))#declare variable as sub_1 and get input from the user for subject1 mark
sub_2=(int(input('enter subject2 mark : ')))#declare variable as sub_2 and get input from the user for subject2 mark
sub_3=(int(input('enter subject3 mark : ')))#declare variable as sub_3 and get input from the user for subject3 mark
total=sub_1+sub_2+sub_3                     #declare variable as total and using concatenation add sub 1,2,3 
average=total/sub                           #declare variable as average and divide the total(total) and no of subjects(sub)
print('name : ',stud_name,'\nno.of.subjects : ',sub,'\ntotal : ',total,'\naverage : ',average)
                                            #print the name of the variables which we need to display, and if you need a new line then use \n
