from flask import *
import sqlite3
import json
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from random import *
from config import app
import os
import configparser
from configparser import ConfigParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from database import connect_to_database
import logging
from email.mime.base import MIMEBase
from email import encoders

connection = sqlite3.connect('timmins_db.db', check_same_thread=False)
cursor = connection.cursor()

logging.basicConfig(filename='error.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

email = ''
user_type = ''

mail = Mail(app)

config = configparser.ConfigParser()
config.read('config.ini')
timmins_mail = config['brochure-config']['timmins_mail']
timmins_password = config['brochure-config']['timmins_password']
timmins_second_mail = config['timmins-second-mail']['timmins_second_mail']
timmins_second_password = config['timmins-second-mail']['timmins_second_password']
third_mail = config['third-mail']['third_mail']

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = timmins_mail
app.config['MAIL_PASSWORD'] = timmins_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = timmins_mail
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

#mail = Mail(app)

def login():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            login_email = request.form['email']
            password = request.form['password']

            config = configparser.ConfigParser()
            config.read('config.ini')
            admin_username = config['admin']['username']
            admin_hashed_password = config['admin']['password']

            global user_type
            user_type = ""

            global email
            if login_email == admin_username and check_password_hash(admin_hashed_password, password):
                email = login_email
                user_type = "admin"
                return redirect('/for_scripting')
            else:
                # CHECKING IF ACCOUNT EXISTS
                cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(login_email))
                account = cursor.fetchone()

                if account:
                    password_rs = account[5]
                    if password_rs is not None and check_password_hash(password_rs, password):
                        email = login_email
                        user_type = "user"
                        return redirect('/for_scripting')
                    else:
                        flash('Incorrect Password')
                else:
                    flash('Incorrect Email/password')
                cursor.close()
                connection.close()
        return render_template("login.html")
    except Exception as login_error:
        logging.error("****An Error Occurred in login method" + "\n" + "An error occurred in: %s", str(login_error),exc_info=True)
        return redirect('/')



def for_scripting():
    try:
        email_value = email
        return render_template('for_scripting.html', email=email_value)
    except Exception as for_scripting_error:
        logging.error("****An Error Occurred in for_scripting method" + "\n" + "An error occurred in: %s", str(for_scripting_error),exc_info=True)
        return redirect('/')

def logout():
    try:
        global email
        email = ''
        return redirect(url_for('home'))
    except Exception as logout_error:
        logging.error("****An Error Occurred in logout method" + "\n" + "An error occurred in: %s", str(logout_error),exc_info=True)
        return redirect('/')



def register():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("select * from categories where category_status = 'Enable'")
        category = cursor.fetchall()
        if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'phone' in request.form and 'country' in request.form and 'email' in request.form and 'password' in request.form:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            phone = request.form['phone']
            country = request.form['country']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            domain_choice =  request.form.getlist('domain_choice1')
            print(domain_choice)

            domain_choice_string = ', '.join(str(value) for value in domain_choice)
            print(domain_choice_string)

            _hashed_password = generate_password_hash(password)
            cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(email))
            account = cursor.fetchone()

            user_domain_name = []
            for domain_choice_loop in domain_choice:
                cursor.execute('SELECT name FROM relation WHERE relation_id = "{}"'.format(domain_choice_loop))
                domain_name = cursor.fetchone()
                user_domain_name.append(domain_name[0])

            config = configparser.ConfigParser()
            config.read('config.ini')
            admin_username = config['admin']['username']

            # If account exists show error and validation checks
            if account is not None:
                flash('Account already exists!')
            elif email == admin_username:
                flash("Invalid email address")
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not re.match(r'^[A-Za-z]+$', firstname):
                flash('Firstname must contain only characters!')
            elif not re.match(r'^[A-Za-z]+$', lastname):
                flash('Lastname must contain only characters!')
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                flash('password must contain atleast(1 uppercase),( 1 special character),(1 lowercase),(total of 8 characters) ')
            elif confirm_password != password:
                flash('Both Confirm password and created password must be same')
            elif not firstname or not lastname or not password or not email:
                flash('Please enter all details in the form!')
            else:
                # Account doesn't exist and the form data is valid, now insert new account into users table
                cursor.execute("INSERT INTO users (first_name, last_name, phone_number,country, email, password, relation_id) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(firstname, lastname, phone,country, email, _hashed_password, domain_choice_string))
                connection.commit()
                smtp_host = 'smtp.mail.yahoo.com'
                smtp_port = 587
                sender_email = timmins_second_mail
                sender_password = timmins_second_password
                recipient_email = (timmins_mail, third_mail)
                email_message = MIMEMultipart()
                email_message['From'] = sender_email
                email_message['To'] = ','.join(recipient_email)
                email_message['Subject'] = 'Timmins: New User Registration'
                body = f'First Name: {firstname}\nLast Name: {lastname}\nPhone: {phone}\nEmail: {email}\nCountry: {country}\nDomain: {user_domain_name}'
                email_message.attach(MIMEText(body, "plain"))
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(sender_email, sender_password)
                smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
                smtp_server.quit()

                smtp_host = 'smtp.mail.yahoo.com'
                smtp_port = 587
                sender_email = timmins_second_mail
                sender_password = timmins_second_password
                recipient_email = email
                email_message = MIMEMultipart()
                email_message['From'] = sender_email
                email_message['To'] = recipient_email
                email_message['Subject'] = 'Welcome! Your account has been created in Timmins'
                body = f'Welcome to Timmins!\n\nExplore our wide range of training courses and certification programs\n\nwww.timmins-consulting.com\n\nThank you'
                email_message.attach(MIMEText(body, "plain"))
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(sender_email, sender_password)
                smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
                smtp_server.quit()
                return render_template('login.html')
        elif request.method == 'POST':
            flash('Please fill out the form!')
        cursor.close()
        connection.close()
        return render_template("register.html", category=category)
    except Exception as register_error:
        logging.error("****An Error Occurred in register method" + "\n" + "An error occurred in: %s", str(register_error),exc_info=True)
        return redirect('/')

def forgot_password():
    try:
        if request.method == 'POST':
            otp = randint(000000, 9999999)
            global email_for_otp
            email_for_otp = request.form['email_for_otp']
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute('select email from users where email="{}"'.format(email_for_otp))
            email_availability = cursor.fetchone()
            if email_availability:
                smtp_host = 'smtp.mail.yahoo.com'
                smtp_port = 587
                sender_email = timmins_second_mail
                sender_password = timmins_second_password
                recipient_email = email_for_otp
                email_message = MIMEMultipart()
                email_message['From'] = sender_email
                email_message['To'] = recipient_email
                email_message['Subject'] = 'OTP'
                body = f'Your OTP is:'+ str(otp)
                email_message.attach(MIMEText(body, "plain"))
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(sender_email, sender_password)
                smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
                smtp_server.quit()
                cursor.execute('update users set otp="{}" where email="{}"'.format(otp, email_for_otp))
                connection.commit()
                return render_template("otp_verification.html")
            else:
                flash("No such Email-id is associated with Timmins Consulting")
            cursor.close()
            connection.close()
        return render_template("forgot_password.html")
    except Exception as forgot_password_error:
        logging.error("****An Error Occurred in forgot_password method" + "\n" + "An error occurred in: %s", str(forgot_password_error),exc_info=True)
        return redirect('/')

def otp_verification():
    try:
        if request.method == 'POST':
            otp_entry = request.form['otp_entry']
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select otp from users where email='{}'".format(email_for_otp))
            otp_from_db = cursor.fetchone()
            if int(otp_from_db[0]) == int(otp_entry):
                return render_template("new_password.html")
            else:
                flash("Invalid OTP, please Recheck and Enter again")
            cursor.close()
            connection.close()
        return render_template("otp_verification.html")
    except Exception as otp_verification_error:
        logging.error("****An Error Occurred in otp_verification method" + "\n" + "An error occurred in: %s", str(otp_verification_error),exc_info=True)
        return redirect('/')


def new_password():
    try:
        if request.method == 'POST':
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password != confirm_password:
                flash("Both passwords must be same")
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                flash('password must contain atleast(1 uppercase),( 1 special character),(1 lowercase),(total of 8 characters) ')
            else:
                _hashed_password = generate_password_hash(password)
                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute("select user_id from users where email = '{}'".format(email_for_otp))
                user_id = cursor.fetchone()
                update_query = "UPDATE users SET password=? where user_id=?"
                cursor.execute(update_query,(_hashed_password, user_id[0]))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect('/login')
        return render_template("new_password.html")
    except Exception as new_password_error:
        logging.error("****An Error Occurred in new_password method" + "\n" + "An error occurred in: %s", str(new_password_error),exc_info=True)
        return redirect('/')

def new_user_password():
    try:
        email = request.args.get('email')
        flash_type = request.args.get('flash_type')
        flash_msg = request.args.get('flash_msg')
        return render_template("new_user_password.html", email=email, flash_type=flash_type, flash_msg=flash_msg)
    except Exception as new_user_password_error:
        logging.error("****An Error Occurred in new_user_password method" + "\n" + "An error occurred in: %s", str(new_user_password_error),exc_info=True)
        return redirect('/')

def new_user_password_update():
    try:
        if request.method == "POST":
            email = request.form['email']
            create_password = request.form['create_password']
            confirm_password = request.form['confirm_password']
            if create_password != confirm_password:
                flash_type = "not_same"
                flash_msg = "Both passwords must be same"
                return redirect(url_for("new_user_password",email=email,flash_type=flash_type,flash_msg=flash_msg))
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', create_password):
                flash_type = "not_match"
                flash_msg = 'password must contain atleast(1 uppercase),( 1 special character),(1 lowercase),(total of 8 characters)'
                return redirect(url_for("new_user_password", email=email, flash_type=flash_type, flash_msg=flash_msg))
            else:
                _hashed_password = generate_password_hash(create_password)
                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute("select user_id from users where email = '{}'".format(email))
                user_id = cursor.fetchone()
                update_query = "UPDATE users SET password=? where user_id=?"
                cursor.execute(update_query,(_hashed_password, user_id[0]))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect('/login')
    except Exception as new_user_password_update_error:
        logging.error("****An Error Occurred in new_user_update_password method" + "\n" + "An error occurred in: %s", str(new_user_password_update_error),exc_info=True)
        return redirect('/')

def admin_user_profile_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                hashed_password = generate_password_hash(password)
                config = configparser.ConfigParser()
                config.read('config.ini')
                config.set('admin', 'username', username)
                config.set('admin', 'password', hashed_password)
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                return render_template('admin_panel.html')
            return render_template('admin-user-profile.html')
        else:
            return redirect("/")
    except Exception as admin_user_profile_update_error:
        logging.error("****An Error Occurred in admin_user_profile_update method" + "\n" + "An error occurred in: %s", str(admin_user_profile_update_error),exc_info=True)
        return redirect('/')

def header():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("select * from categories where category_status = 'Enable'")
        category = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('header.html',category=category,course=course)
    except Exception as header_error:
        logging.error("****An Error Occurred in header method" + "\n" + "An error occurred in: %s", str(header_error),exc_info=True)
        return redirect('/')

def footer():
    return render_template('footer.html')


def contact_details_update():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * from categories where category_status = 'Enable'")
        category = cursor.fetchall()
        cursor.execute("SELECT * FROM courses where course_status = 'Enable'")
        course = cursor.fetchall()
        if request.method == "POST" and 'first_name' in request.form and 'last_name' in request.form and 'email' in request.form and 'selected_option1' in request.form and 'message' in request.form:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            selected_option = request.form['selected_option1']
            message = request.form['message']
            cursor.execute("insert into contact_update (first_name,last_name,email,how_can_we_help,message) values ('{}','{}','{}','{}','{}')".format(first_name, last_name, email, selected_option, message))
            connection.commit()

            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = (timmins_mail, third_mail)
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = ','.join(recipient_email)
            email_message['Subject'] = 'Timmins: Contact us'
            body = f'First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nSelected option: {selected_option}\nMessage: {message}'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = email
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = recipient_email
            email_message['Subject'] = 'Thank you! Your request has been received by Timmins'
            body = f'Greetings from Timmins!\n\nThank you for reaching out. Our team is currently reviewing your request and will reply to you in due course.\n\nwww.timmins-consulting.com\n\nThank you'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            cursor.close()
            connection.close()
            return redirect("/")
        return render_template("contact_us_timmins.html", course=course, category=category)
    except Exception as contact_details_update_error:
        logging.error("****An Error Occurred in contact_details_update method" + "\n" + "An error occurred in: %s", str(contact_details_update_error),exc_info=True)
        return redirect('/')

def request_for_training_update():
    try:
        if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'email' in request.form and 'phone' in request.form and 'course' in request.form and 'country' in request.form and 'message' in request.form:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            course = request.form['course']
            country = request.form['country']
            # selected_option = request.form['selected_option1']
            message = request.form['message']
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("insert into request_for_training_update(first_name,last_name,email,phone,course,country,message) values ('{}','{}','{}','{}','{}','{}','{}')".format(first_name, last_name, email, phone, course, country, message))
            connection.commit()

            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = (timmins_mail, third_mail)
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = ','.join(recipient_email)
            email_message['Subject'] = 'Timmins: Requested for a Training Course'
            body = f'First Name: {first_name}\nLast Name: {last_name}\nPhone: {phone}\nEmail: {email}\nCountry: {country}\nCourse: {course}'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = email
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = recipient_email
            email_message['Subject'] = 'Thank you! Your training request has been received by Timmins'
            body = f'Greetings from Timmins!\n\nWe appreciate your interest, and our team will be in touch with you shortly.\n\nwww.timmins-consulting.com\n\nThank you'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            cursor.close()
            connection.close()
            return redirect("/")
        return render_template("request_for_training.html")
    except Exception as request_for_training_update_error:
        logging.error("****An Error Occurred in request_for_training_update method" + "\n" + "An error occurred in: %s", str(request_for_training_update_error),exc_info=True)
        return redirect('/')

def buy_ticket_update():
    try:
        if request.method == "POST":
            batch_id = request.form['batch_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            country = request.form['country']
            event_name = request.form['event_name']
            batch_name = request.form['batch_name']
            batch_date = request.form['batch_date']
            batch_time = request.form['batch_time']
            quantity = request.form['quantity']
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("insert into buy_ticket_update(first_name,last_name,phone,country,email,event_name,batch_name,batch_date,batch_time,quantity) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(first_name,last_name,email,phone,country,event_name,batch_name,batch_date,batch_time,quantity))
            connection.commit()
            cursor.execute("select user_id from users where email='{}'".format(email))
            check_user_id = cursor.fetchall()
            if check_user_id == []:       #checking user is already registered or not
                user = "new_user"
                cursor.execute("""insert into users(first_name,last_name,email,phone_number,country,relation_id)
                            values('{}','{}','{}','{}','{}','{}')""".format(first_name,last_name,email,phone,country,"1"))
                connection.commit()
            else:
                user = "old_user"
            cursor.execute("select user_id from users where email='{}'".format(email))
            user_id = cursor.fetchone()
            cursor.execute("select user_ids from event_registration where batch_id='{}'".format(batch_id))
            event_registration = cursor.fetchone()
            if event_registration:
                user_list = event_registration[0].split(",")
                if user_id[0] not in user_list:
                    user_list.extend([str(user_id[0])])
                    user_list_join = ",".join(user_list)
                    cursor.execute("update event_registration set user_ids='{}' where batch_id='{}'".format(user_list_join,batch_id))
                    connection.commit()
            else:
                cursor.execute("""insert into event_registration(batch_id,user_ids) 
                                                values ('{}','{}')""".format(batch_id, user_id[0]))
                connection.commit()
            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = (timmins_mail, third_mail)
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = ','.join(recipient_email)
            email_message['Subject'] = 'Timmins: Event Registration'
            body = f'First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone: {phone}\nCountry: {country}\nEvent name: {event_name}\nBatch name: {batch_name}\nBatch date: {batch_date}\nBatch time: {batch_time}\nQuantity: {quantity}'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = email
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = recipient_email
            if user == "old_user":
                email_message['Subject'] = 'Thank you! Your request has been received by Timmins'
                body = f'Greetings from Timmins!\n\nThank you for registration. Now, you are the member in {event_name}-{batch_name}. Our team will reply to you regarding the event details.\n\nwww.timmins-consulting.com\n\nThank you'
            elif user == "new_user":
                email_message['Subject'] = 'Thank you! Your request has been received by Timmins'
                body =  f'Greetings from Timmins!\n\nThank you for registration. Now, you are the member in {event_name}-{batch_name}. Our team will reply to you regarding the event details.\n\nClick the link below to set the password:\nhttp://your-flask-server:5000/new_user_password?email={email}\n\nwww.timmins-consulting.com\n\nThank you'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            cursor.close()
            connection.close()
            return redirect('/')
        return render_template("buy_ticket.html")
    except Exception as buy_ticket_update_error:
        logging.error("****An Error Occurred in buy_ticket_update method" + "\n" + "An error occurred in: %s", str(buy_ticket_update_error),exc_info=True)
        return redirect('/')

def brochure_update():
    try:
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            country = request.form['country']
            inquiring = request.form['inquiring']
            certification_name = request.form['certification_name']
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address')
            elif not re.match(r'^[A-Za-z]+$', first_name):
                flash('Firstname must contain only characters!')
            elif not re.match(r'^[A-Za-z]+$', last_name):
                flash('Lastname must contain only characters!')
            else:
                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute("insert into brochure_update (first_name,last_name,email,phone_number,country,inquiring) values ('{}','{}','{}','{}','{}','{}')".format(first_name, last_name, email, phone_number, country, inquiring))
                connection.commit()
                cursor.execute("""select brochure_link from certification_courses 
                            where certification_course_name = '{}' and certification_status = 'Enable'
                            """.format(certification_name))
                brochure_link = cursor.fetchone()
                print('brochure link:',brochure_link[0])
                '''
                pdf_file = os.path.join(app.root_path, 'static', brochure_link[0])
                
                msg = Message('Thank you! Please find the attached document from Timmins', sender = timmins_second_mail, recipients=[email])
                msg.body = "Dear recipient,\n\nThank you for your interest. Our team will reply to you in due course regarding the certification details.\n\nwww.timmins-consulting.com\n\nThank you"
                #with app.open_resource(pdf_file) as fp:
                    #msg.attach(brochure_link[0], 'application/pdf', fp.read())
                mail.send(msg)
                '''
                recipient_email = email
                pdf_path = os.path.join('static', brochure_link[0])
                email_message = MIMEMultipart()
                email_message['From'] = timmins_second_mail
                email_message['To'] = recipient_email
                email_message['Subject'] = 'Timmins: PDF Attachment'
                body = 'Please find attached PDF file'
                email_message.attach(MIMEText(body, 'plain'))
                with open(pdf_path, 'rb') as file:
                    pdf_attachment = MIMEBase('application', 'octet-stream')
                    pdf_attachment.set_payload(file.read())
                encoders.encode_base64(pdf_attachment)
                pdf_attachment.add_header('content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
                email_message.attach(pdf_attachment)
                smtp_host = 'smtp.mail.yahoo.com'
                smtp_port = 587
                sender_email = timmins_second_mail
                sender_password = timmins_second_password
                #smtp_server = smtplib.SMTP(smtp_host, smtp_port)
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(sender_email,sender_password)
                smtp_server.sendmail(sender_email,recipient_email,email_message.as_string())
                smtp_server.quit()


                smtp_host = 'smtp.mail.yahoo.com'
                smtp_port = 587
                sender_email = timmins_second_mail
                sender_password = timmins_second_password
                recipient_email = (timmins_mail, third_mail)
                email_message = MIMEMultipart()
                email_message['From'] = sender_email
                email_message['To'] = ','.join(recipient_email)
                email_message['Subject'] = 'Timmins: Download Brochure Submission'
                body = f'First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone number: {phone_number}\nCountry: {country}\nInquiring: {inquiring}\nCertification Program: {certification_name}'
                email_message.attach(MIMEText(body, "plain"))
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(sender_email, sender_password)
                smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
                smtp_server.quit()

                cursor.close()
                connection.close()
                return redirect("/")
        return render_template("certification1.html")
    except Exception as brochure_update_error:
        logging.debug("****An Error Occurred in brochure_update method" + "\n" + "An error occurred in: %s", str(brochure_update_error),exc_info=True)
        return redirect('/')

def book_a_demo_update():
    try:
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            selected_option = request.form['selected_option1']
            message = request.form['message']
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("insert into book_a_demo_update (first_name,last_name,email,how_can_we_help,message) values ('{}','{}','{}','{}','{}')".format(first_name, last_name, email, selected_option, message))
            connection.commit()

            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = (timmins_mail, third_mail)
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = ','.join(recipient_email)
            email_message['Subject'] = 'Timmins: Book a demo'
            body = f'First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nSelected option: {selected_option}\nMessage: {message}'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 587
            sender_email = timmins_second_mail
            sender_password = timmins_second_password
            recipient_email = email
            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = recipient_email
            email_message['Subject'] = 'Thank you! Your request has been received by Timmins'
            body = f'Greetings from Timmins!\n\nThank you for reaching out. Our team is currently reviewing your request and will reply to you in due course.\n\nwww.timmins-consulting.com\n\nThank you'
            email_message.attach(MIMEText(body, "plain"))
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipient_email, email_message.as_string())
            smtp_server.quit()

            cursor.close()
            connection.close()

            return redirect("/")
        return render_template("book_a_demo.html")
    except Exception as book_a_demo_update_error:
        logging.error("****An Error Occurred in book_a_demo_update method" + "\n" + "An error occurred in: %s", str(book_a_demo_update_error),exc_info=True)
        return redirect('/')




