from flask import *

import auth
import re
from werkzeug.security import generate_password_hash, check_password_hash
import os
from config import app
import datetime
import configparser
from configparser import ConfigParser
from database import connect_to_database
import logging

config = configparser.ConfigParser()
config.read('config.ini')
admin_mail = config['admin']['username']

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

seo_value = None
def seo():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        global seo_value
        cursor.execute("select seo_value from seo")
        seo_value = cursor.fetchone()
        cursor.close()
        connection.close()
    except Exception as seo_page_error:
        logging.error("****An Error Occurred in seo method" + "\n" + "An error occurred in: %s",str(seo_page_error), exc_info=True)
        return redirect('/')

def home():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute("select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))

        cursor.execute("select * from banner")
        banner_details = cursor.fetchall()

        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        cursor.execute("select * from testimonials where testimonial_status = 'Enable'")
        testimonials = cursor.fetchall()

        cursor.execute("""SELECT courses.course_name, courses.image_link, courses.course_id, 
                        categories.category_name from courses INNER JOIN
                        categories ON categories.category_id = courses.category_id WHERE courses.order_sequence = 1 AND courses.course_status = 'Enable'
                        AND categories.category_status = 'Enable'""")
        popular_courses = cursor.fetchall()  # -------->COURSES NAME AND IMAGE FOR POPULAR COURSES

        cursor.execute("""SELECT batches.batch_id, batches.event_id, batches.start_date, events.course_id
                        FROM batches INNER JOIN events ON batches.event_id = events.event_id
                         WHERE batches.batch_enabling_status='Enable' AND events.event_enabling_status='Enable' 
                         ORDER BY batches.batch_id DESC LIMIT 8""")
        batch_details = cursor.fetchall()       #contains batch details & course_id------------*
        events = []
        for batch_loop in batch_details:
            cursor.execute("SELECT session_start_time,session_date from sessions where batch_id='{}'".format(batch_loop[0]))
            session_details = cursor.fetchall()        #takes related batch 1st session start time..  session_time[0][0]
            cursor.execute("""SELECT course_name,image_link,short_description from courses where course_id='{}'
                        """.format(batch_loop[3]))
            course_details = cursor.fetchone()
            batch_start_date = datetime.datetime.strptime(batch_loop[2], "%Y-%m-%d")
            batch_end_date = datetime.datetime.strptime(session_details[-1][1], "%Y-%m-%d")
            current_date = datetime.datetime.now()
            if current_date < batch_start_date:  # Upcoming
                day_status = "Upcoming"
            elif batch_start_date <= current_date <= batch_end_date:  # Happening    #current_date >= batch_start_date and current_date <= batch_end_date
                day_status = "Happening"
            else:  # Expired
                day_status = "Expired"
            inside_loop_list = [batch_loop[2],session_details[0][0],course_details[0],course_details[1],batch_loop[3],course_details[2],batch_loop[1],batch_loop[0],day_status]
            events.append(inside_loop_list)
            #inside_loop_list contains start_date,start_time,course_name,image_link,course_id,short_description,event_id,batch_id,day_status(expired,happening,upcoming)

        events_list = []
        for event in events:
            event_start_date_str = event[0]
            event_time = event[1]

            # Convert the date string to a datetime object
            event_start_date = datetime.datetime.strptime(event_start_date_str, "%Y-%m-%d")

            # Format the date as "21-05-2023" (day-month-year)
            formatted_date = event_start_date.strftime("%d-%m-%Y")

            # Parse the time string into a datetime object
            time_obj = datetime.datetime.strptime(event_time, "%H:%M:%S")

            # Format the time object in "10:00 am" or "04:25 pm" format
            formatted_time = time_obj.strftime("%I:%M %p")

            # Append the formatted date and time to the event tuple
            formatted_event = [formatted_date, formatted_time] + event[2:]
            events_list.append(formatted_event)

        if auth.email != '':
            if auth.user_type == "admin":
                return render_template("index.html", category=category, course=course, user_name="admin", user_email=auth.email, popular_courses=popular_courses, events=events_list,certification_courses=certification_courses,banner_details=banner_details, testimonials=testimonials,seo_value=seo_value)
            elif auth.user_type == "user":
                cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(auth.email))
                user_details = cursor.fetchall()
                if user_details:
                    user_name = user_details[0][1]
                    relation_id = user_details[0][6]
                    relation_id_list = relation_id.split(",")
                    ids_list = []
                    for relation_id_list_loop in relation_id_list:
                        cursor.execute("select course_ids from relation where relation_id='{}'".format(relation_id_list_loop))
                        course_ids = cursor.fetchone()
                        ids = course_ids[0].split(",")
                        for ids_loop in ids:
                            if ids_loop not in ids_list:
                                ids_list.append(ids_loop)
                    recommended_courses = []
                    for course_id_loop in ids_list:
                        course_details = []
                        cursor.execute("select course_name, image_link,category_id from courses where course_id = '{}' and course_status = 'Enable'".format(course_id_loop))
                        courses = cursor.fetchall()
                        course_details.append(courses[0][0])
                        course_details.append(courses[0][1])
                        cursor.execute("select category_name from categories where category_id = '{}' and category_status = 'Enable'".format(courses[0][2]))
                        category_name = cursor.fetchone()
                        course_details.append(category_name[0])
                        course_details.append(course_id_loop)
                        recommended_courses.append(course_details)
                    cursor.close()
                    connection.close()
                    return render_template("index.html", category=category, course=course, user_details = user_details, user_name = user_name, recommended_courses = recommended_courses, user_email=auth.email, popular_courses=popular_courses, events=events_list, certification_courses=certification_courses,banner_details=banner_details, testimonials=testimonials,seo_value=seo_value)
        else:
            return render_template("index.html", category=category, course=course, popular_courses=popular_courses, events=events_list, certification_courses=certification_courses,banner_details=banner_details,testimonials=testimonials,seo_value=seo_value)
        return render_template("index.html", category=category, course=course,popular_courses=popular_courses,events=events, certification_courses=certification_courses,banner_details=banner_details,testimonials=testimonials,seo_value=seo_value)
    except Exception as home_error:
        logging.error("****An Error Occurred in home method" + "\n" + "An error occurred in: %s", str(home_error), exc_info=True)


def event():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute(
                "select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        cursor.execute("""SELECT batches.batch_id, batches.event_id, batches.start_date, 
                           batches.location, events.course_id, events.event_name, batches.batch_name FROM
                           batches INNER JOIN events ON batches.event_id = events.event_id
                           WHERE batches.batch_enabling_status='Enable' AND events.event_enabling_status='Enable'
                           ORDER BY batches.start_date ASC""")
        batch_details = cursor.fetchall()  # contains batch details & course_id------------*

        upcoming_events_list = []
        happening_events_list = []
        expired_events_list = []
        for batch_loop in batch_details:
            cursor.execute("select image_link, short_description from courses where course_id='{}'".format(batch_loop[4]))
            course_details = cursor.fetchone()

            cursor.execute("""select session_date,session_start_time,session_duration from sessions
                            where batch_id='{}'""".format(batch_loop[0]))
            session_details = cursor.fetchall()
            session_start_time = session_details[0][1]
            session_duration = session_details[0][2]
            end_date = session_details[-1][0]
            start_date = batch_loop[2]

            calc_duration = 0
            for session_loop in session_details:
                session_loop_duration = re.findall(r'\b\d+(?:\.\d+)?(?=(?:\s|$|[^\d.]))',session_loop[2])  # ['4.0'] or ['4.5']
                session_int_duration = float(session_loop_duration[0])
                calc_duration +=session_int_duration
            if calc_duration % 1 == 0:
                total_duration = str(int(calc_duration)) + " hours"
            else:
                total_duration = str(float(calc_duration)) + " hours"

            #-------------------for start date and end date part----------------------------------
            # Convert the start and end date strings to datetime objects
            batch_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            batch_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            # Format the date range
            if batch_start_date == batch_end_date:
                formatted_date = batch_start_date.strftime("%b %d ,%Y")  # 12 June 2023
            else:
                if batch_start_date.month == batch_end_date.month:  # 12-14 June 2023
                    formatted_date = batch_start_date.strftime("%b %d") + "-" + batch_end_date.strftime("%d ,%Y")
                else:   # 12 June-02 July 2023
                    formatted_date = batch_start_date.strftime("%b %d") + "-" + batch_end_date.strftime("%b %d ,%Y")
            split_date_and_year = formatted_date.split(",")  # Split the formatted date using comma 12 June-02 July(0th index) and 2022(1st index)

            #-------------------------- for start time and end time ------------------------------------
            #calculate session_end_time using session_start_time and session_duration
            start_time = datetime.datetime.strptime(session_start_time, '%H:%M:%S')
            duration_numbers = re.findall(r'\b\d+(?:\.\d+)?(?=(?:\s|$|[^\d.]))', session_duration)  #['4.0'] or ['4.5']
            int_duration = float(duration_numbers[0])
            duration = datetime.timedelta(hours=int_duration)   #4:00:00

            end_time = start_time + duration
            session_end_time = end_time.strftime('%H:%M:%S')

            # Parse the time string into a datetime object
            batch_start_time_obj = datetime.datetime.strptime(session_start_time, "%H:%M:%S")
            batch_end_time_obj = datetime.datetime.strptime(session_end_time, "%H:%M:%S")

            # Format the time object in "10:00 am" or "04:25 pm" format
            formatted_start_time = batch_start_time_obj.strftime("%I:%M %p")
            formatted_end_time = batch_end_time_obj.strftime("%I:%M %p")
            both_timing = formatted_start_time + " - " + formatted_end_time  #06:20 PM - 10:20 PM

            #---------------- split as upcoming, happening and expired based on current date ---------------------
            loop_list = [batch_loop[0], batch_loop[1], split_date_and_year[0], split_date_and_year[1], batch_loop[5],course_details[0]]  # batch_id,event_id,date,year,event_name,image_link
            loop_list.extend([batch_loop[6], both_timing, batch_loop[3],total_duration])  # batch_name,both_start&end_timing,location,total_duration

            current_date = datetime.datetime.now()

            if current_date < batch_start_date: #Upcoming
                day_status = "Upcoming"
                loop_list.extend([day_status])
                upcoming_events_list.append(loop_list)
            elif batch_start_date <= current_date <= batch_end_date: #Happening    #current_date >= batch_start_date and current_date <= batch_end_date
                day_status = "Happening"
                loop_list.extend([day_status])
                happening_events_list.append(loop_list)
            else: #Expired
                day_status = "Expired"
                loop_list.extend([day_status])
                expired_events_list.append(loop_list)
        return render_template("event.html", upcoming_event=upcoming_events_list, happening_event=happening_events_list,expired_event=expired_events_list, course=course, category=category,certification_courses=certification_courses,seo_value=seo_value)
    except Exception as event_error:
        logging.error("****An Error Occurred in event method" + "\n" + "An error occurred in: %s", str(event_error),exc_info=True)
        return redirect("/")

def event_details():
    batch_id = ''
    day_status = ''
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute(
                "select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))

        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        if request.method == 'POST':
            batch_id = request.form['batch_id']
            day_status = request.form['day_status']
        if request.method == 'GET':
            batch_id = request.args.get('batch_id')
        cursor.execute("""select batches.batch_name, batches.start_date, batches.location, 
                        batches.image_link, events.event_name, events.course_id,batches.timezone 
                        from batches INNER JOIN events ON batches.event_id = events.event_id 
                        WHERE batches.batch_id='{}'""".format(batch_id))
        batch_details = cursor.fetchone()
        memories = batch_details[3]

        cursor.execute("""select testimonial_student_name, testimonial_company_name,testimonial_feedback, 
                        testimonial_date from courses where course_id='{}'""".format(batch_details[5]))
        course_ids_details = cursor.fetchone()
        testimonial_student_name = course_ids_details[0]
        testimonial_company_name = course_ids_details[1]
        testimonial_feedback = course_ids_details[2]
        testimonial_date = course_ids_details[3]

        cursor.execute("""select key_takeaways,who_is_it_for,prerequisite,language,quizzes,assessments
                        from courses where course_id='{}'""".format(batch_details[5]))
        course_details = cursor.fetchone()
        key_takeaways = course_details[0].split("$")
        who_is_it_for = course_details[1].split("$")
        prerequisite = course_details[2].split("$")

        cursor.execute("""select session_date, session_start_time, session_duration from sessions
                        where batch_id='{}'""".format(batch_id))
        session_details = cursor.fetchall()
        batch_session_details = []      #to show the list of batch's sessions in UI
        calc_duration = 0
        for loop_session in session_details:
            session_start_time_obj = datetime.datetime.strptime(loop_session[1], "%H:%M:%S")
            session_loop_time = session_start_time_obj.strftime("%I:%M %p")
            loop_list = [loop_session[0],session_loop_time,loop_session[2]]
            batch_session_details.append(loop_list)
            #for total duration
            session_loop_duration = re.findall(r'\b\d+(?:\.\d+)?(?=(?:\s|$|[^\d.]))',loop_session[2])  # ['4.0'] or ['4.5']
            session_int_duration = float(session_loop_duration[0])
            calc_duration += session_int_duration
        total_sessions = len(session_details)
        session_start_time = session_details[0][1]
        session_duration = session_details[0][2]
        end_date = session_details[-1][0]
        start_date = batch_details[1]
        if calc_duration % 1 == 0:
            total_duration = str(int(calc_duration)) + " hours"
        else:
            total_duration = str(float(calc_duration)) + " hours"
        # -------------------for start date and end date part----------------------------------
        # Convert the start and end date strings to datetime objects
        batch_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        batch_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # Format the date range
        if batch_start_date == batch_end_date:
            formatted_date = batch_start_date.strftime("%b %d ,%Y")  # 12 June 2023
        else:
            if batch_start_date.month == batch_end_date.month:  # 12-14 June 2023
                formatted_date = batch_start_date.strftime("%b %d") + "-" + batch_end_date.strftime("%d ,%Y")
            else:  # 12 June-02 July 2023
                formatted_date = batch_start_date.strftime("%b %d") + "-" + batch_end_date.strftime("%b %d ,%Y")
        split_date_and_year = formatted_date.split(",")  # Split the formatted date using comma 12 June-02 July(0th index) and 2022(1st index)

        # -------------------------- for start time and end time ------------------------------------
        # calculate session_end_time using session_start_time and session_duration
        start_time = datetime.datetime.strptime(session_start_time, '%H:%M:%S')
        duration_numbers = re.findall(r'\b\d+(?:\.\d+)?(?=(?:\s|$|[^\d.]))', session_duration)  # ['4.0'] or ['4.5']
        int_duration = float(duration_numbers[0])
        duration = datetime.timedelta(hours=int_duration)  # 4:00:00

        end_time = start_time + duration
        session_end_time = end_time.strftime('%H:%M:%S')

        # Parse the time string into a datetime object
        batch_start_time_obj = datetime.datetime.strptime(session_start_time, "%H:%M:%S")
        batch_end_time_obj = datetime.datetime.strptime(session_end_time, "%H:%M:%S")

        # Format the time object in "10:00 am" or "04:25 pm" format
        formatted_start_time = batch_start_time_obj.strftime("%I:%M %p")
        formatted_end_time = batch_end_time_obj.strftime("%I:%M %p")
        both_timing = formatted_start_time + " - " + formatted_end_time  # 06:20 PM - 10:20 PM

        details = [batch_details[4],batch_details[0],both_timing,formatted_date]   #event_name,batch_name,both_time,both_date
        details.extend([batch_details[2],total_duration,total_sessions,session_duration])  #location,total_duration,total_session,session_duration
        details.extend([course_details[3],course_details[4],course_details[5],batch_details[6],day_status]) #language,quizzes,assessments,timezone,day_status
        if memories is None or memories == "None":
            cursor.execute("""select batches.batch_id,batches.event_id,batches.start_date,batches.batch_name,
                            events.event_name,events.course_id from batches INNER JOIN events
                            ON batches.event_id = events.event_id WHERE events.event_enabling_status='Enable'
                            AND batch_enabling_status='Enable' ORDER BY batches.batch_id DESC LIMIT 5""")
            other_batches_details = cursor.fetchall()

            other_events = []
            for other_loop in other_batches_details:
                cursor.execute("""select image_link, short_description from courses where course_id='{}'
                                """.format(other_loop[5]))
                other_batch_course = cursor.fetchone()

                cursor.execute("""select session_date, session_start_time, session_duration from
                                sessions where batch_id='{}'""".format(other_loop[0]))
                other_batch_sessions = cursor.fetchall()
                other_session_start_time = other_batch_sessions[0][1]
                other_session_duration = other_batch_sessions[0][2]
                other_end_date = other_batch_sessions[-1][0]
                other_start_date = other_loop[2]
                # -------------------for start date and end date part----------------------------------
                # Convert the start and end date strings to datetime objects
                other_batch_start_date = datetime.datetime.strptime(other_start_date, "%Y-%m-%d")
                other_batch_end_date = datetime.datetime.strptime(other_end_date, "%Y-%m-%d")

                current_date = datetime.datetime.now()

                if current_date < other_batch_start_date:  # Upcoming
                    other_day_status = "Upcoming"
                elif other_batch_start_date <= current_date <= other_batch_end_date:  # Happening    #current_date >= batch_start_date and current_date <= batch_end_date
                    other_day_status = "Happening"
                else:  # Expired
                    other_day_status = "Expired"

                # Format the date range
                if other_batch_start_date == other_batch_end_date:
                    other_formatted_date = other_batch_start_date.strftime("%b %d ,%Y")  # 12 June 2023
                else:
                    if other_batch_start_date.month == other_batch_end_date.month:  # 12-14 June 2023
                        other_formatted_date = other_batch_start_date.strftime("%b %d") + "-" + other_batch_end_date.strftime("%d ,%Y")
                    else:  # 12 June-02 July 2023
                        other_formatted_date = other_batch_start_date.strftime("%b %d") + "-" + other_batch_end_date.strftime("%b %d ,%Y")
                other_split_date_and_year = other_formatted_date.split(",")  # Split the formatted date using comma 12 June-02 July(0th index) and 2022(1st index)

                # -------------------------- for start time and end time ------------------------------------
                # calculate session_end_time using session_start_time and session_duration
                other_start_time = datetime.datetime.strptime(other_session_start_time, '%H:%M:%S')
                other_duration_numbers = re.findall(r'\b\d+(?:\.\d+)?(?=(?:\s|$|[^\d.]))', other_session_duration)  # ['4.0'] or ['4.5']
                other_int_duration = float(other_duration_numbers[0])
                other_duration = datetime.timedelta(hours=other_int_duration)  # 4:00:00

                other_end_time = other_start_time + other_duration
                other_session_end_time = other_end_time.strftime('%H:%M:%S')

                # Parse the time string into a datetime object
                other_batch_start_time_obj = datetime.datetime.strptime(other_session_start_time, "%H:%M:%S")
                other_batch_end_time_obj = datetime.datetime.strptime(other_session_end_time, "%H:%M:%S")

                # Format the time object in "10:00 am" or "04:25 pm" format
                other_formatted_start_time = other_batch_start_time_obj.strftime("%I:%M %p")
                other_formatted_end_time = other_batch_end_time_obj.strftime("%I:%M %p")
                other_both_timing = other_formatted_start_time + " - " + other_formatted_end_time  # 06:20 PM - 10:20 PM

                inner_loop_list = [other_loop[0],other_split_date_and_year[0],other_split_date_and_year[1]]    #batch_id,both_date,both_date's year
                inner_loop_list.extend([other_loop[4],other_loop[3],other_both_timing])  #event_name,batch_name,other_both_timing
                inner_loop_list.extend([other_batch_course[0],other_batch_course[1],other_day_status]) #course_image_link,short_description,day_status
                other_events.append(inner_loop_list)
            if testimonial_student_name is None or testimonial_student_name == "None":
                return render_template('event_details2.html', batch_id=batch_id, details=details, key_takeaways=key_takeaways, who_is_it_for=who_is_it_for,prerequisite=prerequisite,memories="no", testimonial_student_name_list="", testimonial_company_name_list="", testimonial_feedback_list="",testimonial_date="", other_events=other_events, course=course, category=category,certification_courses=certification_courses,batch_session_details=batch_session_details,seo_value=seo_value)
            else:
                testimonial_student_name_list = testimonial_student_name.split("$")
                testimonial_company_name_list = testimonial_company_name.split("$")
                testimonial_feedback_list = testimonial_feedback.split("$")
                testimonial_date = testimonial_date
                return render_template('event_details2.html', batch_id=batch_id, details=details, key_takeaways=key_takeaways,who_is_it_for=who_is_it_for, prerequisite=prerequisite, memories="no", testimonial_student_name_list=testimonial_student_name_list, testimonial_company_name_list=testimonial_company_name_list, testimonial_feedback_list=testimonial_feedback_list,testimonial_date=testimonial_date,other_events=other_events, course=course, category=category,certification_courses=certification_courses,batch_session_details=batch_session_details,seo_value=seo_value)
        elif memories is not None:
            memories_list = memories.split(",")
            if testimonial_student_name is None or testimonial_student_name == "None":
                return render_template('event_details2.html', batch_id=batch_id, details=details, key_takeaways=key_takeaways, who_is_it_for=who_is_it_for,prerequisite=prerequisite, testimonial_student_name_list="", testimonial_company_name_list="", testimonial_feedback_list="",testimonial_date="",memories_list=memories_list, memories="yes", course=course, category=category,certification_courses=certification_courses,batch_session_details=batch_session_details,seo_value=seo_value)
            else:
                testimonial_student_name_list = testimonial_student_name.split("$")
                testimonial_company_name_list = testimonial_company_name.split("$")
                testimonial_feedback_list = testimonial_feedback.split("$")
                testimonial_date = testimonial_date
                return render_template('event_details2.html', batch_id=batch_id, details=details, key_takeaways=key_takeaways,who_is_it_for=who_is_it_for, prerequisite=prerequisite, testimonial_student_name_list=testimonial_student_name_list, testimonial_company_name_list=testimonial_company_name_list, testimonial_feedback_list=testimonial_feedback_list,testimonial_date=testimonial_date,memories_list=memories_list, memories="yes", course=course, category=category,certification_courses=certification_courses,batch_session_details=batch_session_details,seo_value=seo_value)
        cursor.close()
        connection.close()
        return render_template('event_details2.html')
    except Exception as event_details_error:
        logging.error("****An Error Occurred in event_details method" + "\n" + "An error occurred in: %s",str(event_details_error), exc_info=True)
        return redirect("/")

def all_courses():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute("select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        cursor.close()
        connection.close()
        return render_template("all_courses.html", course=course, category=category,certification_courses=certification_courses, seo_value=seo_value)
    except Exception as all_courses_error:
        logging.error("****An Error Occurred in all_courses method" + "\n" + "An error occurred in: %s", str(all_courses_error),exc_info=True)
        return redirect("/")

def course_details():
    course_name = ''
    key_takeaways = ''
    prerequisites = ''
    who_is_it_for = ''
    Right_side_contents = ''
    course_image = ''

    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()

        global course_id
        if request.method == 'GET':
            course_id = request.args.get('course_id')
        if request.method == 'POST':
            course_id = request.form['course_id']
        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute(
                "select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        cursor.execute("select * from courses where course_id='{}' and course_status = 'Enable'".format(course_id))
        individual_course_details = cursor.fetchall()  # ------>COURSES LIST DOWN ON SELECTION OF CATEGORIES

        cursor.close()
        connection.close()
        if individual_course_details:
            course_name = individual_course_details[0][2]
            course_image = individual_course_details[0][3]
            key_takeaways = individual_course_details[0][5].split("$")
            prerequisites = individual_course_details[0][7].split("$")
            who_is_it_for = individual_course_details[0][6].split("$")
            Right_side_contents = [individual_course_details[0][8],individual_course_details[0][9],individual_course_details[0][10],individual_course_details[0][11],individual_course_details[0][12]]
        return render_template("course_details.html", category=category, course=course,individual_course_details=individual_course_details, course_name=course_name,key_takeaways=key_takeaways, prerequisites=prerequisites, who_is_it_for=who_is_it_for,Right_side_contents=Right_side_contents, course_image=course_image,certification_courses=certification_courses,seo_value=seo_value)
    except Exception as course_details_error:
        logging.error("****An Error Occurred in course_details method" + "\n" + "An error occurred in: %s", str(course_details_error),exc_info=True)
        return redirect("/")


def profile():
    try:
        if request.method == 'POST' and 'email' in request.form:
            email = request.form['email']
            connection = connect_to_database()
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(email))
            user_details = cursor.fetchall()

            cursor.execute("select category_id from categories where category_status = 'Enable'")
            category_ids = cursor.fetchall()

            cursor.execute("select * from courses where course_status = 'Enable'")
            course = cursor.fetchall()

            category = []
            for category_loop in category_ids:
                cursor.execute("select * from courses where course_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_check = cursor.fetchall()
                if category_check:
                    cursor.execute(
                        "select * from categories where category_status = 'Enable' and category_id='{}'".format(
                            category_loop[0]))
                    category_details = cursor.fetchone()
                    category.append(list(category_details))
            cursor.execute("select * from certification_courses where certification_status = 'Enable'")
            certification_courses = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template("profile.html",user_details=user_details, category=category, course=course, certification_courses=certification_courses,id_name="edit-profile")
        else:
            return redirect("/login")
    except Exception as profile_error:
        logging.error("****An Error Occurred in profile method" + "\n" + "An error occurred in: %s", str(profile_error),exc_info=True)
    return render_template("profile.html")

def edit_profile():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM categories where category_status = 'Enable'")
        categories = cursor.fetchall()
        cursor.execute("SELECT * FROM courses where course_status = 'Enable'")
        courses = cursor.fetchall()
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'email' in request.form:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']

            cursor.execute('update users SET first_name = "{}", last_name="{}" where email = "{}"'.format(first_name,last_name,email))
            connection.commit()
            cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(email))
            user_details = cursor.fetchall()

            cursor.close()
            connection.close()

            alert_message = "Profile Details Updated successfully"
            return render_template("profile.html",user_details=user_details, categories=categories, courses=courses,id_name="edit-profile",alert_message=alert_message, certification_courses=certification_courses)
        return render_template("profile.html", categories=categories, courses=courses,certification_courses = certification_courses,id_name="edit-profile")
    except Exception as edit_profile_error:
        logging.error("****An Error Occurred in edit_profile method" + "\n" + "An error occurred in: %s", str(edit_profile_error),exc_info=True)
        return redirect("/")

def change_password():
    email = None
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categories where category_status = 'Enable'")
        categories = cursor.fetchall()
        cursor.execute("SELECT * FROM courses where course_status = 'Enable'")
        courses = cursor.fetchall()
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form and 'confirm_password' in request.form and 'email' in request.form:
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            email = request.form['email']
            cursor.execute('select * from users where email="{}"'.format(email))
            old_password_check = cursor.fetchone()
            stored_hashed_password = old_password_check[5]
            if check_password_hash(stored_hashed_password, old_password):
                if new_password != confirm_password:
                    flash('Both passwords must be same')
                elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', new_password):
                    flash('password must contain atleast(1 uppercase),( 1 special character),(1 lowercase),(total of 8 characters) ')
                else:
                    _hashed_password = generate_password_hash(new_password)
                    cursor.execute('UPDATE users SET password="{}" WHERE email="{}"'.format(_hashed_password, email))
                    connection.commit()
                    cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(email))
                    user_details = cursor.fetchall()
                    alert_message = "Password Updated successfully"
                    return render_template("profile.html", user_details=user_details, categories=categories, courses=courses, password_success="success",id_name="change-password",alert_message=alert_message, certification_courses=certification_courses)
            else:
                flash('Incorrect Old Password')
        cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(email))
        user_details = cursor.fetchall()

        cursor.close()
        connection.close()
        return render_template("profile.html", user_details=user_details, categories=categories, courses=courses,id_name="change-password", certification_courses=certification_courses)
    except Exception as change_password_error:
        logging.error("****An Error Occurred in change_password method" + "\n" + "An error occurred in: %s", str(change_password_error),exc_info=True)
        return redirect("/")

def my_preference():
    email = None
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM categories where category_status = 'Enable'")
        category = cursor.fetchall()
        cursor.execute("SELECT * FROM courses where course_status = 'Enable'")
        course = cursor.fetchall()
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        if request.method == 'POST':
            domain_choice = request.form.getlist('domain_choice1')
            user_email = request.form['email']
            domain_choice_string = ', '.join(str(value) for value in domain_choice)

            cursor.execute("update users set relation_id = '{}' where email = '{}'".format(domain_choice_string,user_email))
            connection.commit()
            cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(user_email))
            user_details = cursor.fetchall()
            user_name = user_details[0][1]
            relation_id = user_details[0][6]
            relation_id_list = relation_id.split(",")
            ids_list = []
            for relation_id_list_loop in relation_id_list:
                cursor.execute("select course_ids from relation where relation_id='{}'".format(relation_id_list_loop))
                course_ids = cursor.fetchone()
                ids = course_ids[0].split(",")
                for ids_loop in ids:
                    if ids_loop not in ids_list:
                        ids_list.append(ids_loop)
            recommended_courses = []
            for course_id_loop in ids_list:
                course_details = []
                cursor.execute("""select course_name, image_link,category_id from courses 
                                    where course_id = '{}' and course_status = 'Enable'""".format(course_id_loop))
                courses = cursor.fetchall()
                course_details.append(courses[0][0])
                course_details.append(courses[0][1])
                cursor.execute("""select category_name from categories 
                                    where category_id = '{}' and category_status = 'Enable'""".format(courses[0][2]))
                category_name = cursor.fetchone()
                course_details.append(category_name[0])
                course_details.append(course_id_loop)
                recommended_courses.append(course_details)
            alert_message = "Preference Updated successfully"
            return render_template("profile.html", user_details=user_details,course=course, category=category,recommended_courses=recommended_courses, user_email=user_email, user_name=user_name,preference_success="success",id_name="my-preference",alert_message=alert_message, certification_courses=certification_courses)
        cursor.execute('SELECT * FROM users WHERE email = "{}"'.format(email))
        user_details = cursor.fetchall()

        cursor.close()
        connection.close()
        return render_template("profile.html", user_details=user_details, course=course, category=category,id_name="my-preference", certification_courses=certification_courses)
    except Exception as my_preference_error:
        logging.error("****An Error Occurred in my_preference method" + "\n" + "An error occurred in: %s",str(my_preference_error), exc_info=True)
        return redirect("/")

def why_timmins():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute(
                "select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template("why_timmins.html",course=course, category=category, certification_courses=certification_courses,seo_value=seo_value)
    except Exception as why_timmins_error:
        logging.error("****An Error Occurred in why_timmins method" + "\n" + "An error occurred in: %s", str(why_timmins_error), exc_info=True)
        return redirect("/")

def blogs_timmins():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute("select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        return render_template("blogs_timmins.html", course=course, category=category, certification_courses=certification_courses,seo_value=seo_value)
    except Exception as blogs_timmins_error:
        logging.error("****An Error Occurred in blogs_timmins method" + "\n" + "An error occurred in: %s", str(blogs_timmins_error), exc_info=True)
        return redirect("/")

def blogs_detail_timmins():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute("select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        return render_template("blogs_detail_timmins.html",course=course, category=category, certification_courses=certification_courses,seo_value=seo_value)
    except Exception as blogs_detail_timmins_error:
        logging.error("****An Error Occurred in blogs_detail_timmins method" + "\n" + "An error occurred in: %s", str(blogs_detail_timmins_error), exc_info=True)
        return redirect("/")

def contact_us_timmins():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute("select * from courses where course_status = 'Enable' and category_id='{}'".format(category_loop[0]))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id='{}'".format(
                    category_loop[0]))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        if request.method == 'POST' and 'arrayValue' in request.form:
            array_value = request.form['arrayValue']
            list_value = array_value.split(",")
            if array_value == ",":
                return render_template("contact_us_timmins.html", course=course, category=category, firstname="", lastname="", email_id="", certification_courses=certification_courses,seo_value=seo_value)
            else:
                if list_value[1] == "admin":
                    return render_template("contact_us_timmins.html", course=course, category=category, firstname="",lastname="", email_id="", certification_courses=certification_courses,seo_value=seo_value)
                else:
                    cursor.execute("select * from users where email='{}'".format(list_value[0]))
                    user_details = cursor.fetchall()
                    return render_template("contact_us_timmins.html", course=course, category=category, firstname=user_details[0][1], lastname=user_details[0][2], email_id=user_details[0][3], certification_courses=certification_courses,seo_value=seo_value)
        cursor.close()
        connection.close()
        return render_template("contact_us_timmins.html", course=course, category=category, certification_courses=certification_courses)
    except Exception as contact_us_timmins_error:
        logging.error("****An Error Occurred in contact_us_timmins method" + "\n" + "An error occurred in: %s", str(contact_us_timmins_error), exc_info=True)
        return redirect("/")


def request_for_training():
    try:
        if request.method == 'POST' and 'arrayValue' in request.form and 'courses_for_training' in request.form:
            array_value = request.form['arrayValue']
            courses_for_training = request.form['courses_for_training']
            list = array_value.split(",")
            if array_value == ",":
                return redirect(url_for('login'))
            else:
                if list[1] == "admin":
                    return render_template("request_for_training.html", first_name='', last_name='', email='', phone_number= '',country='Select Country',courses_for_training=courses_for_training)
                else:
                    connection = connect_to_database()
                    cursor = connection.cursor()
                    cursor.execute("select * from users where email = '{}'".format(list[0]))
                    user_details = cursor.fetchall()

                    cursor.close()
                    connection.close()

                    return render_template("request_for_training.html", first_name=user_details[0][1], last_name=user_details[0][2], email=user_details[0][3] , phone_number=user_details[0][4], country=user_details[0][10],courses_for_training=courses_for_training)
    except Exception as request_for_training_error:
        logging.error("****An Error Occurred in request_for_training method" + "\n" + "An error occurred in: %s", str(request_for_training_error), exc_info=True)
        return redirect("/")
    return render_template("request_for_training.html")

def buy_ticket():
    try:
        if request.method == 'POST':
            user_array_value = request.form['arrayValue']
            batch_id = request.form['batch_id']
            event_name = request.form['event_name']
            batch_name = request.form['batch_name']
            batch_time = request.form['batch_time']
            batch_date = request.form['batch_date']
            list = user_array_value.split(",")
            if user_array_value == ",":
                #return redirect(url_for('login'))
                return render_template("buy_ticket.html", first_name='', last_name='', email='', phone='', country='', batch_id=batch_id, event_name=event_name, batch_name=batch_name, batch_time=batch_time, batch_date=batch_date)
            else:
                if list[1] == "admin":
                    return render_template("buy_ticket.html", first_name='', last_name='',email='', phone='', country='', batch_id=batch_id, event_name=event_name,batch_name=batch_name, batch_time=batch_time, batch_date=batch_date)
                else:
                    connection = connect_to_database()
                    cursor = connection.cursor()
                    cursor.execute("select * from users where email='{}'".format(list[0]))
                    user_details = cursor.fetchall()
                    cursor.close()
                    connection.close()
                    return render_template("buy_ticket.html", first_name=user_details[0][1], last_name=user_details[0][2],email=user_details[0][3], phone=user_details[0][4], country=user_details[0][10], batch_id=batch_id, event_name=event_name, batch_name=batch_name, batch_time=batch_time, batch_date=batch_date)
    except Exception as buy_ticket_error:
        logging.error("****An Error Occurred in buy_ticket method" + "\n" + "An error occurred in: %s", str(buy_ticket_error), exc_info=True)
        return redirect("/")
    return render_template("buy_ticket.html")


def book_a_demo():
    try:
        if request.method == 'POST' and 'arrayValue' in request.form:
            array_value = request.form['arrayValue']
            list = array_value.split(",")
            if array_value == ",":
                return render_template("book_a_demo.html", firstname="", lastname="", email_id="")
            else:
                if list[1] == "admin":
                    return render_template("book_a_demo.html", firstname="", lastname="", email_id="")
                else:
                    connection = connect_to_database()
                    cursor = connection.cursor()
                    cursor.execute("select * from users where email='{}'".format(list[0]))
                    user_details = cursor.fetchall()
                    cursor.close()
                    connection.close()
                    return render_template("book_a_demo.html", firstname=user_details[0][1], lastname=user_details[0][2], email_id=user_details[0][3])
    except Exception as book_a_demo_error:
        logging.error("****An Error Occurred in book_a_demo method" + "\n" + "An error occurred in: %s", str(book_a_demo_error), exc_info=True)
        return redirect("/")
    return render_template("book_a_demo.html")

def admin_panel():
    try:
        email_person = request.form.get('email_person') or request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select user_id from users")
            all_users = cursor.fetchall()
            number_of_users = len(all_users)

            cursor.execute("select course_id from courses")
            all_course_id = cursor.fetchall()
            number_of_courses = len(all_course_id)

            cursor.execute("select batch_id from batches")
            all_batches_id = cursor.fetchall()
            number_of_events = len(all_batches_id)

            cursor.execute("select certification_course_id from certification_courses")
            all_certification_course_id = cursor.fetchall()
            number_of_certification_courses = len(all_certification_course_id)

            cursor.close()
            connection.close()
            return render_template("admin_panel.html", number_of_users=number_of_users, number_of_courses=number_of_courses, number_of_events=number_of_events, number_of_certification_courses=number_of_certification_courses)
        else:
            return redirect("/")
    except Exception as admin_panel_error:
        logging.error("****An Error Occurred in admin_panel method" + "\n" + "An error occurred in: %s", str(admin_panel_error), exc_info=True)
        return redirect("/")

def admin_courses_main():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select * from courses order by course_id desc")
            courses_details = cursor.fetchall()
            courses_list = []
            for courses_details_loop in courses_details:
                sub_list = [courses_details_loop[2], courses_details_loop[0]]
                cursor.execute("SELECT category_name FROM categories WHERE category_id = ?", (courses_details_loop[1],))
                category_id = cursor.fetchone()
                sub_list.append(category_id[0])
                courses_list.append(sub_list)
            cursor.close()
            connection.close()
            return render_template("admin-courses-main.html", courses_list=courses_list)
        else:
            return redirect("/")
    except Exception as admin_courses_main_error:
        logging.error("****An Error Occurred in admin_courses_main method" + "\n" + "An error occurred in: %s", str(admin_courses_main_error), exc_info=True)
        return redirect("/")



def admin_course_individual():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == 'POST' and 'course_name' in request.form:
                course_name = request.form['course_name']
                cursor.execute("select * from courses where course_name = ?",(course_name,))
                global individual_details
                individual_details = cursor.fetchone()

                category_id = individual_details[1]
                cursor.execute("select category_name from categories")
                global all_category_name
                all_category_name = cursor.fetchall()
                cursor.execute("select category_name from categories where category_id = ?",(category_id,))
                global selected_category_name
                selected_category_name = cursor.fetchone()
                cursor.close()
                connection.close()
                return render_template("admin-course-individual.html", individual_details=individual_details, all_category_name=all_category_name,selected_category_name=selected_category_name[0])
        else:
            return redirect("/")
    except Exception as admin_course_individual_error:
        logging.error("****An Error Occurred in admin_course_individual function" + "\n" + "An error occurred in: %s", str(admin_course_individual_error), exc_info=True)
        return redirect('/')
    return render_template("admin-course-individual.html")

def admin_course_individual_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()

            if request.method == 'POST' and 'course_id' in request.form and 'category_name' in request.form and 'course_name' in request.form and 'edit_image' in request.files and 'image_link' in request.form and 'prerequisite' in request.form and 'who_it_is_for' in request.form and 'key_takeaways' in request.form and 'short_description' in request.form and 'quizzes' in request.form and 'duration' in request.form and 'language' in request.form and 'assessment' in request.form and 'hands_on' in request.form:
                course_id = request.form['course_id']
                category_name = request.form['category_name']
                cursor.execute("SELECT category_id FROM categories WHERE category_name=?", (category_name,))
                category_id_final = cursor.fetchone()[0]
                course_name = request.form['course_name']

                edit_image = request.files['edit_image']
                app.config['UPLOAD_FOLDER'] = 'static/assets/images'
                filename = edit_image.filename

                image_link = request.form['image_link']

                prerequisite = request.form['prerequisite']
                who_it_is_for = request.form['who_it_is_for']
                key_takeaways = request.form['key_takeaways']
                quizzes = request.form['quizzes']
                duration = request.form['duration']
                language = request.form['language']
                assessment = request.form['assessment']
                hands_on = request.form['hands_on']
                short_description = request.form['short_description']
                course_status = request.form['course_status']

                if edit_image and filename:
                    edit_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute("""UPDATE courses SET category_id=?, course_name=?, image_link=?, prerequisite=?,
                            who_is_it_for=?, key_takeaways=?, short_description=?, quizzes=?, duration=?,
                            language=?, assessments=?, hans_on=?, course_status=? WHERE course_id=?
                            """, (category_id_final, course_name, image_link, prerequisite, who_it_is_for, key_takeaways, short_description, quizzes, duration, language, assessment, hands_on, course_status, course_id))
                    connection.commit()
                    return redirect(url_for('admin_panel',email_person="admin"))
                else:
                    cursor.execute("""UPDATE courses SET category_id=?, course_name=?, prerequisite=?,
                    who_is_it_for=?, key_takeaways=?, short_description=?, quizzes=?, duration=?,
                    language=?, assessments=?, hans_on=?, course_status=? WHERE course_id=?
                    """, (category_id_final, course_name, prerequisite, who_it_is_for, key_takeaways, short_description, quizzes, duration, language, assessment, hands_on, course_status, course_id))
                    connection.commit()
                    return redirect(url_for('admin_panel',email_person="admin"))
            cursor.close()
            connection.close()
            return render_template("admin-course-individual.html", individual_details=individual_details,all_category_name=all_category_name, selected_category_name=selected_category_name[0])
        else:
            return redirect("/")
    except Exception as admin_course_individual_update_error:
        logging.error("****An Error Occurred in admin_course_individual_update method" + "\n" + "An error occurred in: %s", str(admin_course_individual_update_error),exc_info=True)
        return redirect('/')

def admin_new_course_upload():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("SELECT category_name FROM categories")
            category_names = cursor.fetchall()
            if request.method == 'POST':
                category_name = request.form['category_name']
                course_name = request.form['course_name']
                image_upload = request.files['image_upload']
                image_link = request.form['image_link']
                prerequisite = request.form['prerequisite']
                who_it_is_for = request.form['who_it_is_for']
                key_takeaways = request.form['key_takeaways']
                quizzes = request.form['quizzes']
                duration = request.form['duration']
                language = request.form['language']
                assessment = request.form['assessment']
                hands_on = request.form['hands_on']
                short_description = request.form['short_description']
                course_status = request.form['course_status']

                if not re.match(r'^[A-Za-z\s]+$', quizzes):
                    flash('Quizzes must contain only characters!')
                elif not re.match(r'^[a-zA-Z0-9\s\W]+$',course_name):
                    flash("Course name must consist only characters and numbers")
                elif not re.match(r'^[A-Za-z\s,]+$', language):
                    flash('Language must contain only characters!')
                elif not re.match(r'^[A-Za-z]+$', assessment):
                    flash('Assessment must contain only characters!')
                else:
                    cursor.execute("SELECT category_id FROM categories WHERE category_name = ?", (category_name,))
                    category_id_final = cursor.fetchone()

                    cursor.execute("SELECT MAX(order_sequence) FROM courses WHERE category_id = ?", (category_id_final[0],))
                    highest_order_sequence = cursor.fetchone()[0]

                    next_order_sequence = highest_order_sequence + 1 if highest_order_sequence else 1

                    filename = image_upload.filename
                    image_upload.save(os.path.join('static/assets/images', filename))

                    insert_query = """INSERT INTO courses (category_id, course_name, image_link, order_sequence, who_is_it_for, prerequisite,
                        key_takeaways, quizzes, duration, language, assessments, hans_on, short_description,course_status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)"""

                    cursor.execute(insert_query, (category_id_final[0], course_name, image_link, next_order_sequence, who_it_is_for, prerequisite, key_takeaways, quizzes, duration, language, assessment, hands_on, short_description,course_status))

                    connection.commit()
                    return redirect(url_for('admin_panel',email_person="admin"))

            cursor.close()
            connection.close()
            return render_template("admin_new_course_upload.html", category_name=category_names)
        else:
            return redirect("/")
    except Exception as admin_new_course_upload_error:
        logging.error("****An Error Occurred in admin_new_course_upload method" + "\n" + "An error occurred in: %s", str(admin_new_course_upload_error),exc_info=True)
        return redirect('/')

def admin_course_individual_delete():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            course_id = request.form['course_id']
            cursor.execute(f"select * FROM events WHERE course_id=?", (course_id,))
            event_details = cursor.fetchall()
            if event_details:
                cursor.execute("select * from courses where course_id = ?",(course_id,))
                individual_details = cursor.fetchone()

                category_id = individual_details[1]

                cursor.execute("select category_name from categories")
                all_category_name = cursor.fetchall()

                cursor.execute("select category_name from categories where category_id =?",(category_id,))
                selected_category_name = cursor.fetchone()
                cursor.close()
                connection.close()
                alert_info = "Events exists in this course so you can only disable."
                return render_template("admin-course-individual.html", individual_details=individual_details,all_category_name=all_category_name,selected_category_name=selected_category_name[0],alert_info=alert_info,alert_msg="yes")
            else:
                cursor.execute(f"DELETE FROM courses WHERE course_id=?",(course_id,))
            connection.commit()
            connection.close()
            return redirect(url_for("admin_panel",email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_course_individual_delete_error:
        logging.error("****An Error Occurred in admin_course_individual_delete method" + "\n" + "An error occurred in: %s", str(admin_course_individual_delete_error),exc_info=True)
        return redirect('/')


def admin_domain_create():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            return render_template("admin_domain_create.html")
        else:
            return redirect("/")
    except Exception as admin_domain_create_error:
        logging.error("****An Error Occurred in admin_domain_create method" + "\n" + "An error occurred in: %s", str(admin_domain_create_error),exc_info=True)
        return redirect('/')


def admin_domain_upload():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST' and 'domain_name' in request.form:
                domain_name = request.form['domain_name']
                domain_status = request.form['domain_status']
                if not re.match(r'^[a-zA-Z0-9\s]+$', domain_name):
                    flash("Domain name must consist only characters and numbers")
                else:
                    connection = connect_to_database()
                    cursor = connection.cursor()

                    insert_query = "INSERT INTO categories (category_name,category_status) VALUES (?,?)"
                    cursor.execute(insert_query, (domain_name,domain_status))

                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
            return redirect(url_for("admin_domain_create",email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_domain_upload_error:
        logging.error("****An Error Occurred in admin_domain_upload method" + "\n" + "An error occurred in: %s", str(admin_domain_upload_error),exc_info=True)
        return redirect('/')


def admin_domain_view():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select * from categories order by category_id desc")
            all_categories = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("admin_domain_view.html", all_categories=all_categories)
        else:
            return redirect("/")
    except Exception as admin_domain_view_error:
        logging.error("****An Error Occurred in admin_domain_view method" + "\n" + "An error occurred in: %s", str(admin_domain_view_error),exc_info=True)
        return redirect('/')


def admin_domain_edit():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST' and 'domain_id' in request.form:
                domain_id = request.form['domain_id']
                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute("select * from categories where category_id =?",(domain_id,))
                all_domain = cursor.fetchall()
                cursor.close()
                connection.close()
                return render_template("admin_domain_edit.html", domain_name=all_domain[0][1], domain_id=all_domain[0][0],domain_status=all_domain[0][2])
            return render_template("admin_domain_edit.html")
        else:
            return redirect("/")
    except Exception as admin_domain_edit_error:
        logging.error("****An Error Occurred in admin_domain_edit method" + "\n" + "An error occurred in: %s", str(admin_domain_edit_error),exc_info=True)
        return redirect('/')


def admin_domain_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST' and 'domain_id' in request.form and 'domain_name' in request.form:
                domain_id = request.form['domain_id']
                domain_name = request.form['domain_name']
                domain_status = request.form['domain_status']
                connection = connect_to_database()
                cursor = connection.cursor()

                update_query = "UPDATE categories SET category_name = ?, category_status = ? WHERE category_id = ?"
                cursor.execute(update_query, (domain_name, domain_status, domain_id))

                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('admin_panel',email_person="admin"))
            return render_template("admin_domain_edit.html")
        else:
            return redirect("/")
    except Exception as admin_domain_update_error:
        logging.error("****An Error Occurred in admin_domain_update method" + "\n" + "An error occurred in: %s", str(admin_domain_update_error),exc_info=True)
        return redirect('/')

def admin_domain_edit_delete():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            domain_id = request.form['domain_id']
            cursor.execute(f"select * FROM courses WHERE category_id=?", (domain_id,))
            course_details = cursor.fetchall()
            if course_details:
                cursor.execute("select * from categories where category_id =?",(domain_id,))
                all_domain = cursor.fetchall()
                alert_info = "Course exists in this category so you can only disable."
                return render_template("admin_domain_edit.html", domain_name=all_domain[0][1], domain_id=all_domain[0][0],domain_status=all_domain[0][2],alert_info=alert_info,alert_msg="yes")
            else:
                cursor.execute(f"DELETE FROM categories WHERE category_id=?",(domain_id,))
            connection.commit()
            connection.close()
            return redirect(url_for('admin_panel',email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_domain_edit_delete_error:
        logging.error("****An Error Occurred in admin_domain_edit_delete method" + "\n" + "An error occurred in: %s", str(admin_domain_edit_delete_error),exc_info=True)
        return redirect('/')

def admin_certification_create_new():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("SELECT course_name FROM courses")
            course_name = cursor.fetchall()

            if request.method == 'POST':
                certification_course_name = request.form['certification_course_name']
                sub_text = request.form['sub_text']
                who_is_this_program_for = request.form['who_is_this_program_for']
                program_courses = request.form['program_courses']
                selected_courses = request.form['selected_courses']
                program_topic_paragraphs = request.form['program_topic_paragraphs']
                key_takeaways = request.form['key_takeaways']
                last_day_to_enroll = request.form['last_day_to_enroll']
                duration = request.form['duration']
                program_fee = request.form['program_fee']
                banner_image_upload = request.files['banner_image_upload']
                banner_image_link = request.form['banner_image_link']
                image_upload = request.files['image_upload']
                image_link = request.form['image_link']
                brochure_upload = request.files['brochure_upload']
                brochure_link = request.form['brochure_link']
                certification_status = request.form['certification_status']
                short_description = request.form['short_description']
                about_topic = request.form['about_topic']
                about_description = request.form['about_description']

                if selected_courses == "":
                    flash("Select Related Courses")
                if not re.match(r'^[a-zA-Z0-9\s]+$', certification_course_name):
                    flash("certification Course Name must consist only characters and numbers")
                elif brochure_link == "":
                    flash("Upload Brochure")
                elif image_link == "":
                    flash('Upload Image')
                elif banner_image_link == "":
                    flash('Upload Banner Image')
                else:
                    banner_image_filename = banner_image_upload.filename
                    banner_image_upload.save(os.path.join('static/assets/timmins_images/certifications', banner_image_filename))

                    filename = image_upload.filename
                    image_upload.save(os.path.join('static/assets/timmins_images/certifications', filename))

                    brochure_filename = brochure_upload.filename
                    brochure_upload.save(os.path.join('static/assets/timmins_images/certifications', brochure_filename))

                    insert_query = """INSERT INTO certification_courses (certification_course_name, sub_text,
                    who_is_this_program_for, selected_courses, program_topic_paragraphs, key_takeaways,
                    last_day_to_enroll, duration, program_fee, banner_image_link, image_link, brochure_link, certification_status, 
                    short_description, about_topic, about_description) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                    cursor.execute(insert_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee, banner_image_link, image_link, brochure_link, certification_status, short_description, about_topic, about_description))

                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
            return render_template("admin_certification_create_new.html", course_name=course_name)
        else:
            return redirect("/")
    except Exception as admin_certification_create_new_error:
        logging.error("****An Error Occurred in admin_certification_create_new method" + "\n" + "An error occurred in: %s", str(admin_certification_create_new_error),exc_info=True)
        return redirect('/')

def admin_certification_view():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("""select certification_course_id, certification_course_name
            from certification_courses""")
            all_certification_courses = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("admin_certification_view.html", all_certification_courses=all_certification_courses)
        else:
            return redirect("/")
    except Exception as admin_certification_view_error:
        logging.error("****An Error Occurred in admin_certification_view method" + "\n" + "An error occurred in: %s", str(admin_certification_view_error),exc_info=True)
        return redirect('/')

def admin_certification_course_edit():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("SELECT course_name FROM courses")
            course_name = cursor.fetchall()
            if request.method == 'POST' and 'certification_course_name' in request.form:
                certification_course_name = request.form['certification_course_name']
                cursor.execute("SELECT * FROM certification_courses where certification_course_id =?",(certification_course_name,))
                global certification_course_individual_details
                certification_course_individual_details = cursor.fetchall()
                return render_template("admin_certification_edit.html", certification_course_individual_details=certification_course_individual_details, course_name=course_name)
            cursor.close()
            connection.close()
            return render_template("admin_certification_edit.html")
        else:
            return redirect("/")
    except Exception as admin_certification_course_edit_error:
        logging.error("****An Error Occurred in admin_certification_course_edit method" + "\n" + "An error occurred in: %s", str(admin_certification_course_edit_error),exc_info=True)
        return redirect('/')


def admin_certification_course_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST':
                certification_course_id = request.form['certification_course_id']
                certification_course_name = request.form['certification_course_name']
                sub_text = request.form['sub_text']
                who_is_this_program_for = request.form['who_is_this_program_for']
                selected_courses = request.form['selected_courses']
                short_description = request.form['short_description']
                program_topic_paragraphs = request.form['program_topic_paragraphs']
                key_takeaways = request.form['key_takeaways']
                last_day_to_enroll = request.form['last_day_to_enroll']
                duration = request.form['duration']
                program_fee = request.form['program_fee']
                banner_image_upload = request.files['banner_image_upload']
                banner_image_link = request.form['banner_image_link']
                image_upload = request.files['image_upload']
                image_link = request.form['image_link']
                brochure_upload = request.files['brochure_upload']
                brochure_link = request.form['brochure_link']
                certification_status = request.form['certification_status']
                about_topic = request.form['about_topic']
                about_description = request.form['about_description']

                if selected_courses == "":
                    flash("Select Related Courses")
                elif not re.match(r'^[a-zA-Z0-9\s]+$', certification_course_name):
                    flash("Certification Course Name must consist only of characters and numbers")
                elif banner_image_upload and brochure_upload and image_upload:
                    banner_image_filename = banner_image_upload.filename
                    banner_image_upload.save(os.path.join('static/assets/timmins_images/certifications', banner_image_filename))
                    filename = image_upload.filename
                    image_upload.save(os.path.join('static/assets/timmins_images/certifications', filename))
                    brochure_filename = brochure_upload.filename
                    brochure_upload.save(os.path.join('static/assets/timmins_images/certifications', brochure_filename))

                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?,
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?,
                    key_takeaways = ?, last_day_to_enroll = ?, duration = ?, program_fee = ?,
                    certification_status=?, image_link = ?, brochure_link = ?, banner_image_link = ?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, image_link, brochure_link, banner_image_link, about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
                elif banner_image_upload and image_upload:
                    banner_image_filename = banner_image_upload.filename
                    banner_image_upload.save(os.path.join('static/assets/timmins_images/certifications', banner_image_filename))
                    filename = image_upload.filename
                    image_upload.save(os.path.join('static/assets/timmins_images/certifications', filename))

                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?,
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?,
                    key_takeaways = ?, last_day_to_enroll = ?, duration = ?, program_fee = ?,
                    certification_status=?, image_link = ?, banner_image_link = ?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, image_link, banner_image_link, about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
                elif brochure_upload and image_upload:
                    filename = image_upload.filename
                    image_upload.save(os.path.join('static/assets/timmins_images/certifications', filename))
                    brochure_filename = brochure_upload.filename
                    brochure_upload.save(os.path.join('static/assets/timmins_images/certifications', brochure_filename))

                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?,
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?,
                    key_takeaways = ?, last_day_to_enroll = ?, duration = ?, program_fee = ?,
                    certification_status=?, image_link = ?, brochure_link = ?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, image_link, brochure_link, about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
                elif banner_image_upload and brochure_upload:
                    banner_image_filename = banner_image_upload.filename
                    banner_image_upload.save(os.path.join('static/assets/timmins_images/certifications', banner_image_filename))
                    brochure_filename = brochure_upload.filename
                    brochure_upload.save(os.path.join('static/assets/timmins_images/certifications', brochure_filename))

                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?,
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?,
                    key_takeaways = ?, last_day_to_enroll = ?, duration = ?, program_fee = ?,
                    certification_status=?, brochure_link = ?, banner_image_link = ?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, brochure_link, banner_image_link, about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
                elif brochure_upload:
                    brochure_filename = brochure_upload.filename
                    brochure_upload.save(os.path.join('static/assets/timmins_images/certifications', brochure_filename))

                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?, 
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?, key_takeaways = ?,
                    last_day_to_enroll = ?, duration = ?, program_fee = ?, certification_status=?,
                    brochure_link = ?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, brochure_link, about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
                elif image_upload:
                    filename = image_upload.filename
                    image_upload.save(os.path.join('static/assets/timmins_images/certifications', filename))

                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?, 
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?, key_takeaways = ?,
                    last_day_to_enroll = ?, duration = ?, program_fee = ?, certification_status=?,
                    image_link = ?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, image_link,about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
                elif banner_image_upload:
                    banner_image_filename = banner_image_upload.filename
                    banner_image_upload.save(os.path.join('static/assets/timmins_images/certifications', banner_image_filename))

                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?,
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?,
                    key_takeaways = ?, last_day_to_enroll = ?, duration = ?, program_fee = ?,
                    certification_status=?, banner_image_link = ?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, banner_image_link,about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
                else:
                    connection = connect_to_database()
                    cursor = connection.cursor()
                    update_query = """UPDATE certification_courses SET certification_course_name = ?, sub_text = ?, who_is_this_program_for = ?,
                    selected_courses = ?, short_description = ?, program_topic_paragraphs = ?,
                    key_takeaways = ?, last_day_to_enroll = ?, duration = ?, program_fee = ?,
                    certification_status=?, about_topic = ?, about_description = ? WHERE certification_course_id = ?"""
                    cursor.execute(update_query, (certification_course_name, sub_text, who_is_this_program_for, selected_courses, short_description, program_topic_paragraphs, key_takeaways, last_day_to_enroll, duration, program_fee,certification_status, about_topic, about_description, certification_course_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('admin_panel',email_person="admin"))
            return render_template("admin_certification_edit.html",certification_course_individual_details=certification_course_individual_details)
        else:
            return redirect("/")
    except Exception as admin_certification_course_update_error:
        logging.error("****An Error Occurred in admin_certification_course_update method" + "\n" + "An error occurred in: %s",str(admin_certification_course_update_error), exc_info=True)
        return redirect('/')

def admin_certification_course_edit_delete():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            certification_course_id = request.form['certification_course_id']
            cursor.execute(f"DELETE FROM certification_courses WHERE certification_course_id=?",(certification_course_id,))
            connection.commit()
            connection.close()
            return redirect(url_for('admin_panel',email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_certification_course_edit_delete_error:
        logging.error("****An Error Occurred in admin_certification_course_edit_delete method" + "\n" + "An error occurred in: %s", str(admin_certification_course_edit_delete_error),exc_info=True)
        return redirect('/')

def admin_user_profile():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            return render_template("admin-user-profile.html")
        else:
            return redirect("/")
    except Exception as admin_user_profile_error:
        logging.error("****An Error Occurred in admin_user_profile method" + "\n" + "An error occurred in: %s", str(admin_user_profile_error),exc_info=True)
        return redirect('/')

def admin_training_calendar_new():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select course_name from courses")
            course_name = cursor.fetchall()

            if request.method == 'POST':
                course_name = request.form['course_name']
                cursor.execute("select course_id from courses where course_name =?",(course_name,))
                course_id_final = cursor.fetchone()
                event_enabling_status = request.form['event_enabling_status']
                batch_value1 = request.form['batch_value1']
                batch_name1 = request.form['batch_name1']
                batch_values = request.form.getlist('batch_value')
                batch_names = request.form.getlist('batch_name')
                cursor.execute("insert into events (course_id, event_name, event_enabling_status) values (?,?,?)",(course_id_final[0],course_name,event_enabling_status))
                connection.commit()
                cursor.execute("select event_id from events where event_name =?",(course_name,))
                event_id_fetchall_values = cursor.fetchall()
                event_id = event_id_fetchall_values[-1][0]

                #for batch 1
                cursor.execute("insert into batches (event_id,batch_order,batch_name) values (?,?,?)",(event_id,batch_value1,batch_name1))
                connection.commit()

                #for other batches
                for index, batch_names_loop in enumerate(batch_names):
                    cursor.execute("insert into batches (event_id,batch_order,batch_name) values (?,?,?)",(event_id, batch_values[index], batch_names_loop))
                    connection.commit()
                return redirect(url_for("admin_calendar_batches_list",event_id = event_id,email_person="admin"))
            cursor.close()
            connection.close()
            return render_template("admin_training_calendar_new.html", course_name=course_name)
        else:
            return redirect("/")
    except Exception as admin_training_calendar_new_error:
        logging.error("****An Error Occurred in admin_training_calendar_new method" + "\n" + "An error occurred in: %s", str(admin_training_calendar_new_error),exc_info=True)
        return redirect('/')

def admin_calendar_batches_list():  #send the event_id value along with url_for as... url_for("admin_calendar_batches_list",event_id = event_id)
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()

            event_id = request.args.get('event_id') or request.form.get('event_id')
            #request.args.get('event_id')   ----> important to get the value from url_for
            #request.form.get('event_id')   ----> used when try to access this from html page

            cursor.execute("select event_name from events where event_id =?",(event_id,))
            event_name = cursor.fetchone()
            cursor.execute("select * from batches where event_id =?",(event_id,))
            individual_event_batch_details = cursor.fetchall()
            print("individual_event_batch_details",individual_event_batch_details)
            cursor.close()
            connection.close()
            return render_template("admin_calendar_batches_list.html",individual_event_batch_details=individual_event_batch_details, event_name=event_name[0], event_id=event_id)
        else:
            return redirect("/")
    except Exception as admin_calendar_batches_list_error:
        logging.error("****An Error Occurred in admin_calendar_batches_list method" + "\n" + "An error occurred in: %s", str(admin_calendar_batches_list_error),exc_info=True)
        return redirect('/')

def admin_calendar_individual_batch():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST':
                batch_id = request.form.get('batch_id')
                event_id = request.form.get('event_id')

                connection = connect_to_database()
                cursor = connection.cursor()

                cursor.execute("select event_name from events where event_id = ?",(event_id,))
                event_name = cursor.fetchone()
                cursor.execute("select batch_name from batches where batch_id = ?",(batch_id,))
                batch_name = cursor.fetchone()
                cursor.execute("select shortform from timezone")
                timezone_shortform = cursor.fetchall()

                cursor.close()
                connection.close()
                return render_template("admin_calendar_batch_details.html",batch_id=batch_id, event_id=event_id, event_name=event_name[0], batch_name=batch_name[0], timezone_shortform=timezone_shortform)
            else:
                return redirect("/")
    except Exception as admin_calendar_individual_batch_error:
        logging.error("****An Error Occurred in admin_calendar_individual_batch method" + "\n" + "An error occurred in: %s",str(admin_calendar_individual_batch_error), exc_info=True)
        return redirect('/')

def admin_calendar_batch_details():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                event_id = request.form['event_id']
                batch_id = request.form['batch_id']
                location = request.form['location']
                event_fee = request.form['event_fee']
                timezone = request.form['timezone']
                image_upload = request.files.getlist('image_upload')
                batch_enabling_status = request.form['batch_enabling_status']
                start_date = request.form['start_date']
                meeting = request.form['meeting']

                if meeting == "recurring":
                    recurrence = request.form['recurrence']
                    recurrence_start_time = request.form['recurrence_start_time']
                    recurrence_duration = request.form['recurrence_duration']

                    if len(recurrence_start_time) == 8:
                        recurrence_start_time_final = recurrence_start_time
                    else:
                        recurrence_start_time_final = str(recurrence_start_time) + ":00"

                    if recurrence == "Daily":
                        repeat_days = request.form['repeat_days']
                        daily_end_date = request.form['daily_end_date']
                        start_date_daily_result = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')  # Specify your start date
                        end_date_daily_result = datetime.datetime.strptime(str(daily_end_date), '%Y-%m-%d')  # Specify your end date
                        daily_dates = []
                        while start_date_daily_result <= end_date_daily_result:
                            daily_dates.append(start_date_daily_result.strftime('%Y-%m-%d'))
                            start_date_daily_result += datetime.timedelta(days=int(repeat_days))

                        cursor.execute("DELETE from sessions where batch_id=?",(batch_id,))
                        connection.commit()
                        for daily_dates_loop in daily_dates:
                            cursor.execute("""insert into sessions (batch_id,session_date,session_start_time,session_duration)
                                       values (?,?,?,?)""",(batch_id, daily_dates_loop,recurrence_start_time_final,recurrence_duration))
                            connection.commit()
                        if not image_upload or not any(photos for photos in image_upload):
                            cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                           batch_enabling_status=?, start_date=?, meeting=?,recurrence=?,
                                           recurrence_repeat_every=?, recurrence_end_date=? where batch_id=?
                                          """,(location, timezone, event_fee, batch_enabling_status,
                                        start_date, meeting, recurrence,repeat_days,daily_end_date,batch_id))
                            connection.commit()
                            return redirect(url_for("admin_calendar_sessions_list", event_id=event_id,batch_id=batch_id,update_alert="no", go_back="create",email_person="admin"))
                        else:
                            app.config['UPLOAD_FOLDER'] = 'static/assets/images/expired_events_images'
                            for file in image_upload:
                                filename = file.filename
                                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            image_link = request.form['image_link']
                            cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                       batch_enabling_status=?, image_link=?,start_date=?, 
                                      meeting=?,recurrence=?,recurrence_repeat_every=?, recurrence_end_date=? 
                                      where batch_id=?""",(location, timezone, event_fee,
                                      batch_enabling_status,image_link,start_date,meeting, recurrence, repeat_days,
                                      daily_end_date, batch_id))
                            connection.commit()
                            return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id,update_alert="no", go_back="create",email_person="admin"))
                    elif recurrence == "Weekly":
                        repeat_weeks = request.form['repeat_weeks']
                        selected_days = request.form.getlist('day')
                        selected_days_string = '$'.join(selected_days)     #for day details to be entered in db
                        weekly_end_date = request.form['weekly_end_date']
                        start_date_result = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                        end_date_result = datetime.datetime.strptime(weekly_end_date, '%Y-%m-%d')

                        # Find the first occurrence of the selected days in the specified week
                        first_day = start_date_result
                        while first_day.strftime('%a') not in selected_days:
                            first_day += datetime.timedelta(days=1)

                        weekly_dates = []
                        selected_days_count = 0
                        while first_day <= end_date_result:
                            for day in selected_days:
                                if first_day.strftime('%a') == day:
                                    weekly_dates.append(first_day.strftime('%Y-%m-%d'))
                                    selected_days_count += 1
                                    if selected_days_count == len(selected_days):
                                        selected_days_count = 0
                                        first_day += datetime.timedelta(days=(7 * (int(repeat_weeks) - 1)))
                                        while first_day.strftime('%a') not in selected_days:
                                            first_day += datetime.timedelta(days=1)
                                        break
                            first_day += datetime.timedelta(days=1)

                        cursor.execute("DELETE from sessions where batch_id='{}'".format(batch_id))
                        connection.commit()

                        for weekly_dates_loop in weekly_dates:
                            cursor.execute("""insert into sessions (batch_id,session_date,session_start_time,session_duration)
                                         values (?,?,?,?)""",(batch_id,weekly_dates_loop,recurrence_start_time_final,recurrence_duration))
                            connection.commit()

                        if not image_upload or not any(photos for photos in image_upload):
                            cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                         batch_enabling_status=?, start_date=?, meeting=?,
                                         recurrence=?, recurrence_repeat_every=?, recurrence_end_date=?, 
                                         recurrence_weekly_day=? where batch_id=?
                                         """,(location, timezone, event_fee, batch_enabling_status, start_date,meeting, recurrence, repeat_weeks, weekly_end_date,selected_days_string,batch_id))
                            connection.commit()
                            return redirect(url_for("admin_calendar_sessions_list", event_id=event_id,batch_id=batch_id,update_alert="no", go_back="create",email_person="admin"))
                        else:
                            app.config['UPLOAD_FOLDER'] = 'static/assets/images/expired_events_images'
                            for file in image_upload:
                                filename = file.filename
                                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            image_link = request.form['image_link']
                            cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                         batch_enabling_status=?,image_link=?, start_date=?, meeting=?,
                                         recurrence=?, recurrence_repeat_every=?, recurrence_end_date=? where batch_id=?
                                         """,(location, timezone, event_fee,
                                         batch_enabling_status, image_link, start_date, meeting,
                                         recurrence, repeat_weeks, weekly_end_date,batch_id))
                            connection.commit()
                            return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id,update_alert="no", go_back="create",email_person="admin"))
                    elif recurrence == 'Monthly':
                        repeat_months = request.form['repeat_months']
                        monthly_end_date = request.form['monthly_end_date']
                        start_date_monthly_result = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                        end_date_monthly_result = datetime.datetime.strptime(monthly_end_date, '%Y-%m-%d')
                        monthly_dates = []
                        current_date = start_date_monthly_result
                        print("_____",current_date)

                        while current_date <= end_date_monthly_result:
                            monthly_dates.append(current_date.strftime('%Y-%m-%d'))
                            # Calculate the new month and year
                            new_month = (current_date.month + int(repeat_months) - 1) % 12 + 1
                            new_year = current_date.year + (current_date.month + int(repeat_months) - 1) // 12
                            # Create a new datetime object with the adjusted month and year
                            current_date = current_date.replace(year=new_year, month=new_month)

                        cursor.execute("DELETE from sessions where batch_id=?",(batch_id,))
                        connection.commit()

                        for monthly_dates_loop in  monthly_dates:
                            cursor.execute("""insert into sessions (batch_id,session_date,session_start_time,session_duration)
                                       values (?,?,?,?)""",(batch_id,monthly_dates_loop,recurrence_start_time_final,recurrence_duration))
                            connection.commit()
                        if not image_upload or not any(photos for photos in image_upload):
                            cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                      batch_enabling_status=?, start_date=?, meeting=?,
                                      recurrence=?,recurrence_repeat_every=?, recurrence_end_date=? where batch_id=?
                                      """,(location, timezone, event_fee, batch_enabling_status,start_date, meeting,recurrence, repeat_months, monthly_end_date, batch_id))
                            connection.commit()
                            return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id,update_alert="no", go_back="create",email_person="admin"))
                        else:
                            app.config['UPLOAD_FOLDER'] = 'static/assets/images/expired_events_images'
                            for file in image_upload:
                                filename = file.filename
                                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            image_link = request.form['image_link']
                            cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                        batch_enabling_status=?, image_link=?, start_date=?, 
                                        meeting=?,recurrence=?,recurrence_repeat_every=?, recurrence_end_date=? 
                                        where batch_id=?""",(location, timezone, event_fee,
                                        batch_enabling_status, image_link,start_date, meeting,recurrence, repeat_months,
                                        monthly_end_date,batch_id))
                            connection.commit()
                            return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id,update_alert="no", go_back="create",email_person="admin"))
                elif meeting == "individual":
                    session_date1 = request.form['session_date1']
                    session_start_time1 = request.form['session_start_time1']
                    session_duration1 = request.form['session_duration1']
                    session_dates = request.form.getlist('session_date')
                    session_start_times = request.form.getlist('session_start_time')
                    session_durations = request.form.getlist('session_duration')

                    if len(session_start_time1) == 8:
                        session_start_time1_final = session_start_time1
                    else:
                        session_start_time1_final = str(session_start_time1) + ":00"

                    cursor.execute("DELETE from sessions where batch_id=?",(batch_id,))
                    connection.commit()

                    cursor.execute("""insert into sessions (batch_id,session_date,session_start_time,session_duration)
                                   values (?,?,?,?)""",(batch_id, session_date1,
                                   session_start_time1_final,session_duration1))
                    connection.commit()

                    for index, session_date_loop in enumerate(session_dates):
                        if len(session_start_times[index]) == 8:
                            session_start_time_final = session_start_times[index]
                        else:
                            session_start_time_final = str(session_start_times[index]) + ":00"
                        cursor.execute("""insert into sessions (batch_id,session_date,session_start_time,session_duration)
                                     values (?,?,?,?)""",(batch_id, session_date_loop,
                                     session_start_time_final,session_durations[index]))
                        connection.commit()

                    if not image_upload or not any(photos for photos in image_upload):
                        cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                         batch_enabling_status=?, start_date=?, meeting=? where batch_id=?
                                        """,(location,timezone,event_fee,batch_enabling_status,start_date,meeting,batch_id))
                        connection.commit()
                        return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id, update_alert="no", go_back="create",email_person="admin"))
                    else:
                        app.config['UPLOAD_FOLDER'] = 'static/assets/images/expired_events_images'
                        for file in image_upload:
                            filename = file.filename
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_link = request.form['image_link']
                        cursor.execute("""UPDATE batches SET location=?,timezone=?, event_fee=?,
                                      batch_enabling_status=?, image_link=?, start_date=?, 
                                      meeting=? where batch_id=?""",(location, timezone, event_fee,
                                      batch_enabling_status, image_link, start_date, meeting,batch_id))
                        connection.commit()
                        return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id, update_alert="no", go_back="create",email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_batch_details_error:
        logging.error("****An Error Occurred in admin_calendar_batch_details method" + "\n" + "An error occurred in: %s",str(admin_calendar_batch_details_error), exc_info=True)
        return redirect('/')

def admin_calendar_sessions_list():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()

            event_id = request.args.get('event_id')  # important to get the value from url_for
            batch_id = request.args.get('batch_id')
            update_alert = request.args.get('update_alert')
            go_back = request.args.get('go_back')

            cursor.execute("select event_name from events where event_id =?",(event_id,))
            event_name = cursor.fetchone()
            cursor.execute("select batch_name,location from batches where batch_id =?",(batch_id,))
            batch_details = cursor.fetchone()
            cursor.execute("select * from sessions where batch_id = ?",(batch_id,))
            session_details = cursor.fetchall()
            if batch_details[1] is not None:
                return render_template("admin_calendar_sessions_list.html", event_id=event_id, batch_id=batch_id,event_name=event_name[0], batch_name=batch_details[0],session_details=session_details, update_alert=update_alert, go_back=go_back)
            else:
                return redirect(url_for("admin_calendar_no_batch_details",event_id=event_id,batch_id=batch_id,email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_sessions_list_error:
        logging.error("****An Error Occurred in admin_calendar_sessions_list method" + "\n" + "An error occurred in: %s",str(admin_calendar_sessions_list_error), exc_info=True)
        return redirect('/')

def admin_calendar_sessions_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                session_id = request.form['session_id']
                batch_id = request.form['batch_id']
                event_id = request.form['event_id']
                session_date = request.form['session_date']
                session_start_time = request.form['session_start_time']
                session_duration = request.form['session_duration']
                action = request.form['action']
                go_back = request.form['go_back']
                if action == "edit":
                    cursor.execute("""UPDATE sessions SET session_date='{}', session_start_time='{}', session_duration='{}'
                            where session_id='{}'""".format(session_date,session_start_time,session_duration,session_id))
                    connection.commit()
                    return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id, update_alert="yes_edited", go_back=go_back,email_person="admin"))
                elif action == "delete":
                    cursor.execute("DELETE from sessions where session_id=?",(session_id,))
                    connection.commit()
                    cursor.execute("select * from sessions where batch_id=?",(batch_id,))
                    session_details = cursor.fetchall() #for to session_details is empty or not
                    if not session_details:     #consider as session_details == []
                        cursor.execute("""update batches set location=NULL, timezone=NULL, event_fee=NULL,
                                        total_duration=NULL,image_link=NULL,batch_enabling_status=NULL,
                                        start_date=NULL, meeting=NULL, recurrence=NULL,
                                        recurrence_repeat_every=NULL, recurrence_end_date=NULL,
                                        recurrence_weekly_day=NULL where batch_id=?""",(batch_id,))
                        connection.commit()
                        return redirect(url_for("admin_calendar_no_batch_details", event_id=event_id, batch_id=batch_id,email_person="admin"))
                    else:
                        return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id, update_alert="yes_deleted", go_back=go_back,email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_sessions_update_error:
        logging.error("****An Error Occurred in admin_calendar_sessions_update method" + "\n" + "An error occurred in: %s",str(admin_calendar_sessions_update_error), exc_info=True)
        return redirect('/')

def admin_calendar_add_new_session():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                batch_id = request.form['batch_id']
                event_id = request.form['event_id']
                session_date1 = request.form['session_date1']
                session_start_time1 = request.form['session_start_time1']
                session_duration1 = request.form['session_duration1']
                session_dates = request.form.getlist('session_date')
                session_start_times = request.form.getlist('session_start_time')
                session_durations = request.form.getlist('session_duration')

                session_start_time1_final = str(session_start_time1) + ":00"

                cursor.execute("""insert into sessions (batch_id,session_date,session_start_time,session_duration)
                                 values (?,?,?,?)""",(batch_id, session_date1,session_start_time1_final,session_duration1))
                connection.commit()
                for index, session_date_loop in enumerate(session_dates):
                    session_start_time_final = str(session_start_times[index]) + ":00"
                    cursor.execute("""insert into sessions (batch_id,session_date,session_start_time,session_duration)
                                   values (?,?,?,?)""",(batch_id, session_date_loop,session_start_time_final,session_durations[index]))
                    connection.commit()
                return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id, update_alert="no",go_back="create",email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_add_new_session_error:
        logging.error("****An Error Occurred in admin_calendar_add_new_session method" + "\n" + "An error occurred in: %s",str(admin_calendar_add_new_session_error), exc_info=True)
        return redirect('/')

def admin_calendar_list_view():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            alert_message = request.args.get('alert_message')
            cursor.execute("""SELECT events.event_id,events.event_name,events.event_enabling_status,
                                batches.start_date from events INNER JOIN batches ON events.event_id=batches.event_id 
                                WHERE batches.batch_order='Batch 1' ORDER BY events.event_id DESC""")
            event_details = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("admin_calendar_list_view.html", event_details=event_details, alert_message=alert_message)
        else:
            return redirect("/")
    except Exception as admin_calendar_list_view_error:
        logging.error("****An Error Occurred in admin_calendar_list_view method" + "\n" + "An error occurred in: %s",str(admin_calendar_list_view_error), exc_info=True)
        return redirect('/')

def admin_calendar_edit_batches_list():
    try:
        email_person = request.args.get('email_person') or request.form.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()

            event_id = request.args.get('event_id') or request.form.get('event_id')
            update_alert = request.args.get('update_alert')
            cursor.execute("select event_name from events where event_id=?",(event_id,))
            event_name = cursor.fetchone()
            cursor.execute("select batch_id, batch_order, batch_name from batches where event_id=?",(event_id,))
            all_batch_details = cursor.fetchall()

            cursor.close()
            connection.close()
            return render_template("admin_calendar_edit_batches_list.html", event_id=event_id, event_name=event_name[0],all_batch_details=all_batch_details,update_alert=update_alert)
        else:
            return redirect("/")
    except Exception as admin_calendar_edit_batches_list_error:
        logging.error("****An Error Occurred in admin_calendar_edit_batches_list method" + "\n" + "An error occurred in: %s",str(admin_calendar_edit_batches_list_error), exc_info=True)
        return redirect('/')

def admin_calendar_edit_batch_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                batch_id = request.form['batch_id']
                event_id = request.form['event_id']
                batch_name = request.form['batch_name']
                action = request.form['action']
                if action == "save":
                    cursor.execute("UPDATE batches SET batch_name=? where batch_id=?",(batch_name,batch_id))
                    connection.commit()
                    return redirect(url_for("admin_calendar_edit_batches_list",event_id=event_id,update_alert="yes_saved",email_person="admin"))
                elif action == "delete":
                    cursor.execute("DELETE from batches where batch_id=?",(batch_id,))
                    connection.commit()
                    cursor.execute("DELETE from sessions where batch_id=?",(batch_id,))
                    connection.commit()
                    cursor.execute("select batch_id, batch_order from batches where event_id=?",(event_id,))
                    batch_details = cursor.fetchall()
                    for index,batch_loop in enumerate(batch_details):
                        batch_split = batch_loop[1].split(" ")
                        index_add = index + 1
                        batch_concat = batch_split[0] + " " + str(index_add)
                        cursor.execute("""UPDATE batches SET batch_order=? where batch_id=?
                                    """,(batch_concat,batch_loop[0]))
                        connection.commit()
                    return redirect(url_for("admin_calendar_edit_batches_list", event_id=event_id, update_alert="yes_deleted",email_person="admin"))
                elif action == "view_details":
                    return redirect(url_for("admin_calendar_edit_batch_details_view",event_id=event_id, batch_id=batch_id,email_person="admin"))
                elif action == "view_sessions":
                    return redirect(url_for("admin_calendar_sessions_list", event_id=event_id, batch_id=batch_id, update_alert="no", go_back="edit",email_person="admin"))
                elif action == "view_users":
                    return redirect(url_for("admin_individual_event_mapped_users",batch_id=batch_id,email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_edit_batch_update_error:
        logging.error("****An Error Occurred in admin_calendar_edit_batch_update method" + "\n" + "An error occurred in: %s",str(admin_calendar_edit_batch_update_error), exc_info=True)
        return redirect('/')

def admin_calendar_edit_add_batch():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                event_id = request.form['event_id']
                cursor.execute("select event_name from events where event_id=?",(event_id,))
                event_name = cursor.fetchone()
                cursor.execute("select batch_order from batches where event_id=?",(event_id,))
                batches_order = cursor.fetchall()
                string_value = batches_order[-1][0]
                last_string_number = ''.join(filter(str.isdigit, string_value))
                last_number = int(last_string_number) + 1
                return render_template("admin_calendar_edit_add_batch.html",event_id=event_id,event_name=event_name[0],last_number=last_number)
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_edit_add_batch_error:
        logging.error("****An Error Occurred in admin_calendar_edit_add_batch method" + "\n" + "An error occurred in: %s",str(admin_calendar_edit_add_batch_error), exc_info=True)
        return redirect('/')

def admin_calendar_edit_add_batch_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                event_id = request.form['event_id']
                batch_value1 = request.form['batch_value1']
                batch_name1 = request.form['batch_name1']
                batch_values = request.form.getlist('batch_value')
                batch_names = request.form.getlist('batch_name')
                # for batch new
                cursor.execute("""insert into batches (event_id,batch_order,batch_name) values (?,?,?)
                            """,(event_id,batch_value1,batch_name1))
                connection.commit()

                # for other batches
                for index, batch_names_loop in enumerate(batch_names):
                    cursor.execute("""insert into batches (event_id,batch_order,batch_name) values (?,?,?)
                                """,(event_id,batch_values[index],batch_names_loop))
                    connection.commit()
                return redirect(url_for("admin_calendar_batches_list",event_id = event_id,email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_edit_add_batch_update_error:
        logging.error("****An Error Occurred in admin_calendar_edit_add_batch_update method" + "\n" + "An error occurred in: %s",str(admin_calendar_edit_add_batch_update_error), exc_info=True)
        return redirect('/')

def admin_calendar_edit_event_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                event_id = request.form['event_id']
                event_enabling_status = request.form['event_enabling_status']
                action = request.form['action']
                if action == "save":
                    cursor.execute("""UPDATE events SET event_enabling_status=? where event_id=?
                                    """,(event_enabling_status,event_id))
                    connection.commit()
                    return redirect(url_for("admin_calendar_list_view",alert_message="yes_status_saved",email_person="admin"))
                elif action == "delete":
                    cursor.execute("select batch_id from batches where event_id=?",(event_id,))
                    batch_ids = cursor.fetchall()
                    for batch_ids_loop in batch_ids:   #related session delete
                        cursor.execute("DELETE from sessions where batch_id=?",(batch_ids_loop[0],))
                        connection.commit()
                    #related batches delete
                    cursor.execute("DELETE from batches where event_id=?",(event_id,))
                    connection.commit()
                    #related event delete
                    cursor.execute("DELETE from events where event_id=?",(event_id,))
                    connection.commit()
                    return redirect(url_for("admin_calendar_list_view",alert_message="yes_event_deleted",email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_edit_event_update_error:
        logging.error("****An Error Occurred in admin_calendar_edit_event_update method" + "\n" + "An error occurred in: %s",str(admin_calendar_edit_event_update_error), exc_info=True)
        return redirect('/')

def admin_calendar_edit_batch_details_view():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            event_id = request.args.get("event_id") or request.form.get('event_id')
            batch_id = request.args.get("batch_id") or request.form.get('batch_id')
            cursor.execute("select event_name from events where event_id=?",(event_id,))
            event_name = cursor.fetchone()
            cursor.execute("select * from batches where batch_id=?",(batch_id,))
            batch_details = cursor.fetchone()
            batch_name = batch_details[3]
            meeting = batch_details[11]
            cursor.execute("select shortform from timezone")
            timezone_shortform = cursor.fetchall()
            if batch_details[4] is not None:
                if meeting == "recurring":
                    cursor.execute("select session_start_time, session_duration from sessions where batch_id=?",(batch_id,))
                    all_time_details = cursor.fetchall()
                    time_details = all_time_details[0]
                    all_session_details = ['None','None']
                    if batch_details[12] == "Weekly":
                        selected_days = batch_details[15]
                        selected_days_list = selected_days.split('$')
                        return render_template("admin_calendar_edit_batch_details_view.html", event_id=event_id,batch_id=batch_id, event_name=event_name[0], batch_name=batch_name,batch_details=batch_details, time_details=time_details, time="yes", selected_days_list=selected_days_list,all_session_details=all_session_details,timezone_shortform=timezone_shortform)
                    else:
                        return render_template("admin_calendar_edit_batch_details_view.html", event_id=event_id, batch_id=batch_id,event_name=event_name[0], batch_name=batch_name, batch_details=batch_details,time_details=time_details, time="yes",all_session_details=all_session_details,timezone_shortform=timezone_shortform)
                elif meeting == "individual":
                    time_details = ['None','None']
                    cursor.execute("select session_date,session_start_time,session_duration from sessions where batch_id=?",(batch_id,))
                    all_session_details = cursor.fetchall()
                    return render_template("admin_calendar_edit_batch_details_view.html", event_id=event_id, batch_id=batch_id,event_name=event_name[0], batch_name=batch_name, batch_details=batch_details,time_details=time_details, time="yes",all_session_details=all_session_details,timezone_shortform=timezone_shortform)
            else:
                return redirect(url_for("admin_calendar_no_batch_details",event_id=event_id,batch_id=batch_id,email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_calendar_edit_batch_details_view_error:
        logging.error("****An Error Occurred in admin_calendar_edit_batch_details_view method" + "\n" + "An error occurred in: %s",str(admin_calendar_edit_batch_details_view_error), exc_info=True)
        return redirect('/')

def admin_calendar_no_batch_details():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            event_id = request.args.get('event_id')
            batch_id = request.args.get('batch_id')
            return render_template('admin_calendar_no_batch_details.html',event_id=event_id,batch_id=batch_id)
        else:
            return redirect("/")
    except Exception as admin_calendar_no_batch_details_error:
        logging.error("****An Error Occurred in admin_calendar_no_batch_details method" + "\n" + "An error occurred in: %s",str(admin_calendar_no_batch_details_error), exc_info=True)
        return redirect('/')

def admin_calendar_edit_event_name():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            event_id = request.form['event_id']
            event_name = request.form['event_name']
            cursor.execute("UPDATE events SET event_name=? where event_id=?",(event_name,event_id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for("admin_calendar_edit_batches_list",event_id=event_id,update_alert="yes_event_name_updated",email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_calendar_edit_event_name_error:
        logging.error("****An Error Occurred in admin_calendar_edit_event_name method" + "\n" + "An error occurred in: %s",str(admin_calendar_edit_event_name_error), exc_info=True)
        return redirect('/')

def admin_user_calendar_create():
    try:
        email_person = request.args.get('email_person') or request.form.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            from_event = request.args.get('from_event')
            from_event_batch_id = request.args.get('batch_id')
            cursor.execute("select event_id, event_name from events order by event_id DESC")
            event_details = cursor.fetchall()
            concat_list = []
            for event_loop in event_details:
                cursor.execute("select batch_id,batch_name from batches where event_id=?",(event_loop[0],))
                batch_details = cursor.fetchall()
                for batch_loop in batch_details:
                    concat_details = []
                    concat_name = event_loop[1] + " - " + batch_loop[1]
                    batch_id = batch_loop[0]
                    concat_details.extend([batch_id,concat_name])
                    concat_list.append(concat_details)
            cursor.execute("select user_id, email from users")
            user_details = cursor.fetchall()

            if request.method == "POST":
                batch_id = request.form['batch_id']
                user_email_name = request.form.getlist('user_emails')

                user_email_ids = []         #contains inserted email user_ids
                for user_loop in user_email_name:   #To get the user id of users using email
                    cursor.execute("select user_id from users where email=?",(user_loop,))
                    user_id = cursor.fetchone()
                    user_email_ids.append(str(user_id[0]))
                user_ids = ','.join(user_email_ids)
                cursor.execute("select batch_id,user_ids from event_registration")
                event_registration = cursor.fetchall()

                if event_registration:
                    batch_list=[]
                    user_ids_list = []
                    for event_loop in event_registration:
                        batch_list.append(int(event_loop[0]))    #only for batch ids from db
                        user_ids_list.append(event_loop[1])      #only for user ids from db
                    if int(batch_id) in batch_list:
                        batch_index = batch_list.index(int(batch_id))   #To get the index of batch_id
                        email_id_if_list = []
                        for id_loop in user_email_ids:      #used here to avoid duplication of user ids
                            if id_loop not in (user_ids_list[batch_index].split(",")):
                                email_id_if_list.append(str(id_loop))
                        if_user_ids = ",".join(email_id_if_list)
                        user_concat = user_ids_list[batch_index] + "," + if_user_ids
                        cursor.execute("""update event_registration set user_ids=? where batch_id=?
                                    """,(user_concat,batch_id))
                        connection.commit()
                    elif int(batch_id) not  in batch_list:
                        cursor.execute("""insert into event_registration (batch_id,user_ids) values
                                                    (?,?)""",(batch_id, user_ids))
                        connection.commit()
                else:
                    cursor.execute("""insert into event_registration (batch_id,user_ids) values
                                (?,?)""",(batch_id,user_ids))
                    connection.commit()
                return redirect(url_for('admin_panel',email_person="admin"))
            cursor.close()
            connection.close()
            return render_template("admin_user_calendar_create.html",concat_list=concat_list,user_details=user_details,from_event=from_event,from_event_batch_id=from_event_batch_id)
        else:
            return redirect("/")
    except Exception as admin_user_calendar_create_error:
        logging.error("****An Error Occurred in admin_user_calendar_create method" + "\n" + "An error occurred in: %s", str(admin_user_calendar_create_error),exc_info=True)
        return redirect('/')

def admin_user_display_list():
    try:
        email_person = request.args.get('email_person') or request.form.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select user_id,first_name,last_name,email from users")
            user_details = cursor.fetchall()
            update_alert = request.args.get('update_alert')

            if request.method == "POST":
                user_id = request.form['user_id']
                action = request.form['action']
                if action == "delete":
                    cursor.execute("select batch_id,user_ids from event_registration")
                    event_registration = cursor.fetchall()
                    for batch_loop in event_registration:
                        user_ids_list = batch_loop[1].split(",")
                        if user_id in user_ids_list:
                            user_ids_list.remove(user_id)
                            if user_ids_list == []:
                                cursor.execute("DELETE from event_registration where batch_id=?",(batch_loop[0],))
                                connection.commit()
                            else:
                                updated_user_ids_list = ",".join(user_ids_list)
                                cursor.execute("""UPDATE event_registration set user_ids=? where
                                                batch_id=?""",(updated_user_ids_list,batch_loop[0]))
                                connection.commit()
                    cursor.execute("DELETE from users WHERE user_id=?",(user_id,))
                    connection.commit()
                    cursor.execute("select user_id,first_name,last_name,email from users")
                    new_user_details = cursor.fetchall()        #why again mentioned here means after deleting the user when we pass the old user_details which contain old records including that deleted user.
                    return render_template("admin_user_display_list.html", user_details=new_user_details,alert_message="yes_user_deleted")
                elif action == "view_details":
                    return redirect(url_for("admin_user_details_view",user_id=user_id,email_person="admin"))
                elif action == "view_batches":
                    return redirect(url_for("admin_user_batches_view",user_id=user_id,email_person="admin"))
            cursor.close()
            connection.close()
            return render_template("admin_user_display_list.html",user_details=user_details,update_alert=update_alert)
        else:
            return redirect("/")
    except Exception as admin_user_display_list_error:
        logging.error("****An Error Occurred in admin_user_display_list method" + "\n" + "An error occurred in: %s",str(admin_user_display_list_error), exc_info=True)
        return redirect('/')

def admin_user_details_view():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            user_id = request.args.get('user_id') or request.form.get('user_id')
            cursor.execute("select * from users where user_id=?",(user_id,))
            user_details = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template("admin_user_details_view.html",user_id=user_id,user_details=user_details)
        else:
            return redirect("/")
    except Exception as admin_user_details_view_error:
        logging.error("****An Error Occurred in admin_user_details_view method" + "\n" + "An error occurred in: %s",str(admin_user_details_view_error), exc_info=True)
        return redirect('/')

def admin_user_details_view_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                user_id = request.form['user_id']
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                phone = request.form['phone']
                country = request.form['country']
                action = request.form['action']
                if action == "update":
                    cursor.execute("""UPDATE users SET first_name=?, last_name=?,phone_number=?,country=?
                                    WHERE user_id=?""",(first_name,last_name,phone,country,user_id))
                    connection.commit()
                    return redirect(url_for('admin_user_display_list',update_alert="yes_updated",email_person="admin"))
                elif action == "reset_password":
                    return redirect(url_for("new_user_password", email=email,flash_type="no", flash_msg="no",email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_user_details_view_update_error:
        logging.error("****An Error Occurred in admin_user_details_view_update method" + "\n" + "An error occurred in: %s",str(admin_user_details_view_update_error), exc_info=True)
        return redirect('/')

def admin_user_batches_view():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            user_id = request.args.get('user_id') or request.form.get('user_id')
            update_alert = request.args.get('update_alert')
            cursor.execute("select first_name, last_name, email from users where user_id=?",(user_id,))
            user_details = cursor.fetchone()

            cursor.execute("select * from event_registration")
            event_registration = cursor.fetchall()
            user_batch_list = []    #user allocated batch and details
            batch_ids = []
            for batch_loop in event_registration:
                if user_id in batch_loop[1].split(","):
                    batch_ids.append(batch_loop[0])

                    cursor.execute("select event_id, batch_name from batches where batch_id=?",(batch_loop[0],))
                    user_batch_details = cursor.fetchone()
                    cursor.execute("select event_name from events where event_id=?",(user_batch_details[0],))
                    event_name = cursor.fetchone()
                    name = event_name[0] + " - " + user_batch_details[1]
                    inner_list = [batch_loop[0],name]   #batch_id,event-batch name
                    user_batch_list.append(inner_list)

            cursor.execute("select event_id, event_name from events order by event_id DESC")
            event_details = cursor.fetchall()
            all_concat_list = []    #all batch details except already mapped batches
            for event_loop in event_details:
                cursor.execute("select batch_id,batch_name from batches where event_id=?",(event_loop[0],))
                batch_details = cursor.fetchall()
                for new_batch_loop in batch_details:
                    if new_batch_loop[0] not in batch_ids:
                        concat_name = event_loop[1] + " - " + new_batch_loop[1]
                        batch_id = new_batch_loop[0]
                        concat_details = [batch_id, concat_name]
                        all_concat_list.append(concat_details)
            cursor.close()
            connection.close()
            return render_template("admin_user_batches_view.html",user_id=user_id,user_details=user_details,user_batch_list=user_batch_list,all_concat_list=all_concat_list,update_alert=update_alert)
        else:
            return redirect("/")
    except Exception as admin_user_batches_view_error:
        logging.error("****An Error Occurred in admin_user_details_view_update method" + "\n" + "An error occurred in: %s",str(admin_user_batches_view_error), exc_info=True)
        return redirect('/')

def admin_user_batch_delete():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                batch_id = request.form['user_batch_id']
                user_id = request.form['user_id']
                action = request.form['action']
                if action == "delete":
                    cursor.execute("select user_ids from event_registration where batch_id=?",(batch_id,))
                    user_ids = cursor.fetchone()
                    user_ids_list = user_ids[0].split(",")
                    user_ids_list.remove(user_id)
                    if user_ids_list == []:
                        cursor.execute("DELETE from event_registration where batch_id=?",(batch_id,))
                        connection.commit()
                    else:
                        updated_user_ids = ",".join(user_ids_list)
                        cursor.execute("""UPDATE event_registration SET user_ids=? WHERE batch_id=?
                                        """,(updated_user_ids,batch_id))
                        connection.commit()
                    return redirect(url_for('admin_user_batches_view',user_id=user_id,update_alert="yes_deleted",email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_user_batch_delete_error:
        logging.error("****An Error Occurred in admin_user_batch_delete method" + "\n" + "An error occurred in: %s",str(admin_user_batch_delete_error), exc_info=True)
        return redirect('/')

def admin_user_batches_view_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                user_id = request.form['user_id']
                batch_ids = request.form.getlist('batch_ids')
                for batch_id_loop in batch_ids:
                    cursor.execute("select user_ids from event_registration where batch_id=?",(batch_id_loop,))
                    db_user_ids = cursor.fetchone()
                    if db_user_ids:
                        db_user_list = db_user_ids[0].split(",")
                        if user_id not in db_user_list:
                            db_user_list.append(user_id)
                            user_ids_join = ",".join(db_user_list)
                            cursor.execute("""update event_registration set user_ids=? where batch_id=?
                                           """,(user_ids_join,int(batch_id_loop)))
                            connection.commit()
                    else:
                        cursor.execute("""insert into event_registration(batch_id,user_ids) values
                                        (?,?)""",(int(batch_id_loop),str(user_id)))
                        connection.commit()
                return redirect(url_for('admin_user_batches_view',user_id=user_id,update_alert="yes_updated",email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_user_batches_view_update_error:
        logging.error("****An Error Occurred in admin_user_batches_view_update method" + "\n" + "An error occurred in: %s",str(admin_user_batches_view_update_error), exc_info=True)
        return redirect('/')

def admin_event_users_mapping():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("""select batches.batch_id,batches.batch_name,events.event_name 
                        from batches INNER JOIN events ON events.event_id = batches.event_id order by batches.batch_id desc""")
            event_batch_details = cursor.fetchall()
            event_batch_list = []
            for batch_loop in event_batch_details:
                cursor.execute("select user_ids from event_registration where batch_id=?",(batch_loop[0],))
                user_ids = cursor.fetchone()
                if user_ids is not None and user_ids[0] != "":
                    user_ids_len = len(user_ids[0].split(","))
                    total_persons = str(user_ids_len) + " persons"
                else:
                    total_persons = "0 persons"
                event_batch_name = batch_loop[2] + " - " + batch_loop[1]
                batch_list = [batch_loop[0],event_batch_name,total_persons]
                event_batch_list.append(batch_list)
            cursor.close()
            connection.close()
            return render_template("admin_event_users_mapping.html",event_batch_list=event_batch_list)
        else:
            return redirect("/")
    except Exception as admin_event_users_mapping_error:
        logging.error("****An Error Occurred in admin_event_users_mapping method" + "\n" + "An error occurred in: %s",str(admin_event_users_mapping_error), exc_info=True)
        return redirect('/')

def admin_individual_event_mapped_users():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            batch_id = request.args.get('batch_id') or request.form.get('batch_id')
            cursor.execute("select batch_name, event_id from batches where batch_id=?",(batch_id,))
            batch_details = cursor.fetchone()
            cursor.execute("select event_name from events where event_id=?",(batch_details[1],))
            event_name = cursor.fetchone()
            cursor.execute("select user_ids from event_registration where batch_id=?",(batch_id,))
            user_ids = cursor.fetchone()
            if user_ids is not None and user_ids[0] != "":
                user_ids_list = user_ids[0].split(",")
                users_list = []
                for user_loop in user_ids_list:
                    cursor.execute("""select first_name,last_name,email,phone_number,country,user_id from users
                                    where user_id=?""",(user_loop,))
                    user_details = cursor.fetchone()
                    users_list.append(list(user_details))
                cursor.close()
                connection.close()
                return render_template("admin_individual_event_mapped_users.html", users_list=users_list,event_name=event_name[0],batch_name=batch_details[0],batch_id=batch_id)
            else:
                return render_template("admin_individual_event_mapped_no_users.html", event_name=event_name[0], batch_name=batch_details[0], batch_id=batch_id)
        else:
            return redirect("/")
    except Exception as admin_individual_event_mapped_users_error:
        logging.error("****An Error Occurred in admin_individual_event_mapped_users method" + "\n" + "An error occurred in: %s",str(admin_individual_event_mapped_users_error), exc_info=True)
        return redirect('/')

def admin_individual_event_mapped_users_delete():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == "POST":
                user_id = request.form['user_id']
                batch_id = request.form['batch_id']
                action = request.form['action']
                if action == "delete":
                    cursor.execute("select user_ids from event_registration where batch_id=?",(batch_id,))
                    event_user_ids = cursor.fetchone()
                    event_user_ids_list = event_user_ids[0].split(",")
                    event_user_ids_list.remove(user_id)
                    updated_user_ids = ",".join(event_user_ids_list)
                    cursor.execute("""UPDATE event_registration SET user_ids=? WHERE batch_id=?""",(updated_user_ids, batch_id))
                    connection.commit()
                    return redirect(url_for("admin_individual_event_mapped_users",batch_id=batch_id,email_person="admin"))
            cursor.close()
            connection.close()
        else:
            return redirect("/")
    except Exception as admin_individual_event_mapped_users_delete_error:
        logging.error("****An Error Occurred in admin_individual_event_mapped_users_delete method" + "\n" + "An error occurred in: %s",str(admin_individual_event_mapped_users_delete_error), exc_info=True)
        return redirect('/')

def admin_individual_event_user_create():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == "POST":
                batch_id = request.form['batch_id']
                return redirect(url_for("admin_user_calendar_create",from_event="yes",batch_id=batch_id,email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_individual_event_user_create_error:
        logging.error("****An Error Occurred in admin_individual_event_user_create method" + "\n" + "An error occurred in: %s",str(admin_individual_event_user_create_error), exc_info=True)
        return redirect('/')

def admin_basic_calendar():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("""SELECT batches.start_date, courses.course_name FROM events INNER JOIN courses ON
            events.course_id = courses.course_id INNER JOIN batches ON events.event_id = batches.event_id""")
            event_calendar = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("admin-basic-calendar.html", event_calendar=event_calendar)
        else:
            return redirect("/")
    except Exception as admin_basic_calendar_error:
        logging.error("****An Error Occurred in admin_basic_calendar method" + "\n" + "An error occurred in: %s", str(admin_basic_calendar_error),exc_info=True)
        return redirect('/')

def admin_courses():
    return render_template("admin-courses.html")

def admin_mailbox():
    return render_template("admin-mailbox.html")

def admin_mailbox_compose():
    return render_template("admin-mailbox-compose.html")

def admin_mailbox_read():
    return render_template("admin-mailbox-read.html")

def admin_list_view_calendar():
    return render_template("admin-list-view-calendar.html")

def admin_bookmark():
    return render_template("admin-bookmark.html")

def admin_panel1():
    return redirect(url_for('admin_panel',email_person="admin"))

def admin_review():
    return render_template("admin-review.html")

def admin_add_listing():
    return render_template("admin-add-listing.html")

def admin_teacher_profile():
    return render_template("admin-teacher-profile.html")

def my_calendar():
    try:
        global seo_value
        if seo_value is None:
            seo()
        if request.method == 'POST' and 'email' in request.form:
            global event_details
            event_details = ""
            email = request.form['email']

            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select user_id from users where email=?",(email,))
            user_id = cursor.fetchone()
            cursor.execute("select batch_id,user_ids from event_registration")
            all_event_user_details = cursor.fetchall()
            batch_id_list = []      #contains user id's batch ids
            for all_event_user_details_loop in all_event_user_details:
                all_event_user_details_loop_split = all_event_user_details_loop[1].split(",")
                if str(user_id[0]) in all_event_user_details_loop_split:  #checks the logged email's user id in batch's event registraion row
                    batch_id_list.append(all_event_user_details_loop[0])
            Main_list = []
            for batch_id_loop in batch_id_list:
                cursor.execute("""select batch_id,event_id,batch_name,timezone from batches 
                                where batch_id=? and batch_enabling_status='Enable'""",(batch_id_loop,))
                batch_details =cursor.fetchone()
                cursor.execute("select event_name from events where event_id=?",(batch_details[1],))
                event_name = cursor.fetchone()
                cursor.execute("""select session_date, session_start_time, session_duration from sessions where
                                batch_id=?""",(batch_details[0],))
                sessions_details = cursor.fetchall()
                for session_loop in sessions_details:
                    start_time = datetime.datetime.strptime(session_loop[1], '%H:%M:%S')
                    duration_numbers = re.findall(r'\b\d+(?:\.\d+)?(?=(?:\s|$|[^\d.]))',session_loop[2])  # ['4.0'] or ['4.5']
                    int_duration = float(duration_numbers[0])
                    duration = datetime.timedelta(hours=int_duration)  # 4:00:00
                    end_time = start_time + duration
                    session_end_time = end_time.strftime('%H:%M:%S')
                    batch_end_time_obj = datetime.datetime.strptime(session_end_time, "%H:%M:%S")
                    formatted_start_time = start_time.strftime("%I:%M %p")  # Format the time object in "10:00 am" or "04:25 pm" format
                    formatted_end_time = batch_end_time_obj.strftime("%I:%M %p")
                    both_timing = formatted_start_time + " - " + formatted_end_time  # 06:20 PM - 10:20 PM

                    sub_list = [session_loop[0],event_name[0],session_loop[1],batch_details[2],batch_details[3],both_timing]
                    # sub_list contains session_date,event_name,session_time,batch_name,timezone,both_formatted_timing(06:20 PM - 10:20 PM)
                    Main_list.append(sub_list)
            cursor.close()
            connection.close()
            return render_template('my_calendar.html', event_details=Main_list,seo_value=seo_value)
        return render_template("my_calendar.html")
    except Exception as my_calendar_error:
        logging.error("****An Error Occurred in my_calendar method" + "\n" + "An error occurred in: %s", str(my_calendar_error),exc_info=True)
        return redirect('/')

def individual_category_page():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute(
                "select * from courses where course_status = 'Enable' and category_id=?",(category_loop[0],))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id=?",(category_loop[0],))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        if request.method == 'POST' and 'category_name' in request.form:
            category_name = request.form['category_name']
            cursor.execute("""select category_id from categories where category_name = ?
                                and category_status = 'Enable'""",(category_name,))
            category_id = cursor.fetchone()
            cursor.execute("select * from courses where category_id = ? and course_status = 'Enable'",(category_id[0],))
            course_details = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("individual_category_page.html",category_name=category_name,course_details=course_details,category=category,course=course, certification_courses=certification_courses,seo_value=seo_value)
        return render_template("individual_category_page.html",category=category,course=course, certification_courses=certification_courses,seo_value=seo_value)
    except Exception as individual_category_page_error:
        logging.error("****An Error Occurred in individual_category_page method" + "\n" + "An error occurred in: %s", str(individual_category_page_error),exc_info=True)
        return redirect('/')

def certification():
    try:
        global seo_value
        if seo_value is None:
            seo()
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("select category_id from categories where category_status = 'Enable'")
        category_ids = cursor.fetchall()

        cursor.execute("select * from courses where course_status = 'Enable'")
        course = cursor.fetchall()

        category = []
        for category_loop in category_ids:
            cursor.execute(
                "select * from courses where course_status = 'Enable' and category_id=?",(category_loop[0],))
            category_check = cursor.fetchall()
            if category_check:
                cursor.execute("select * from categories where category_status = 'Enable' and category_id=?",(category_loop[0],))
                category_details = cursor.fetchone()
                category.append(list(category_details))
        cursor.execute("select * from certification_courses where certification_status = 'Enable'")
        certification_courses = cursor.fetchall()

        global certification_value

        if request.method == "GET":
            certification_value = request.args.get('certification_value')
        if request.method == "POST":
            certification_value = request.form['certification_value']

        cursor.execute("SELECT * FROM certification_courses where certification_course_id = ? and certification_status = 'Enable'",(certification_value,))
        certification_course_details = cursor.fetchall()
        course_name = certification_course_details[0][1]
        sub_text = certification_course_details[0][2]
        who_is_this_program_for = certification_course_details[0][3]
        selected_courses = certification_course_details[0][4].split(",")
        program_topic_paragraphs = certification_course_details[0][5].split("$")

        program_courses_list = []
        for i in range(min(len(selected_courses), len(program_topic_paragraphs))):
            selected_courses_variable = selected_courses[i].strip()
            cursor.execute("SELECT course_id FROM courses WHERE course_name = ?", (selected_courses_variable,))
            course_id = cursor.fetchone()
            content = program_topic_paragraphs[i]
            if i in [0, 2, 4, 6, 8]:
                side = "left"
            else:
                side = "right"
            program_courses_list.append((selected_courses_variable, content, side, course_id[0]))

        key_takeaways = certification_course_details[0][6].split("$")
        last_day_to_enroll = certification_course_details[0][7]
        duration = certification_course_details[0][8]
        program_fee = certification_course_details[0][9]
        brochure_link = certification_course_details[0][11]
        banner_image_link = certification_course_details[0][14]
        about_topic = certification_course_details[0][15]
        about_description = certification_course_details[0][16]
        return render_template("certification1.html", course_name=course_name, sub_text=sub_text, who_is_this_program_for=who_is_this_program_for, program_courses_list=program_courses_list, key_takeaways=key_takeaways, last_day_to_enroll=last_day_to_enroll, duration=duration, program_fee=program_fee,banner_image_link=banner_image_link, course=course, category=category, certification_courses=certification_courses,about_topic=about_topic,about_description=about_description,seo_value=seo_value)
    except Exception as certification_error:
        logging.error("****An Error Occurred in certification method" + "\n" + "An error occurred in: %s", str(certification_error),exc_info=True)
        return redirect('/')


def admin_banner_creation():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("""SELECT certification_course_name FROM certification_courses 
                           where certification_status = 'Enable'""")
            certification_course_name = cursor.fetchall()
            cursor.execute("SELECT * FROM banner")
            banner_details = cursor.fetchall()
            banner_header = banner_details[0][1]
            banner_title = banner_details[0][2]
            short_description = banner_details[0][3]
            banner_link = banner_details[0][4]
            cursor.execute("""SELECT certification_course_name FROM certification_courses 
                            WHERE certification_course_id = ? and certification_status = 'Enable'""", (banner_link,))
            banner_link_final = cursor.fetchall()
            banner_status = banner_details[0][5]

            if request.method == 'POST':
                banner_header = request.form['banner_header']
                banner_title = request.form['banner_title']
                short_description = request.form['short_description']
                banner_link = request.form['banner_link']
                cursor.execute("""SELECT certification_course_id FROM certification_courses 
                            WHERE certification_course_name = ? and certification_status = 'Enable'""", (banner_link,))
                certification_course_id = cursor.fetchone()
                banner_status = request.form['banner_status']
                cursor.execute("UPDATE banner SET header = ?, title = ?, short_description = ?, link = ?, banner_status = ? WHERE banner_id = ?",(banner_header, banner_title, short_description, certification_course_id[0], banner_status, banner_details[0][0]))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('admin_panel',email_person="admin"))
            return render_template("admin_banner_creation.html", certification_course_name=certification_course_name, banner_header=banner_header, banner_title=banner_title, short_description=short_description, banner_link_final=banner_link_final, banner_status=banner_status)
        else:
            return redirect("/")
    except Exception as admin_banner_creation_error:
        logging.error("****An Error Occurred in admin_banner_creation method" + "\n" + "An error occurred in: %s", str(admin_banner_creation_error),exc_info=True)
        return redirect('/')

def download_file():
    file_path = 'static/company_profile.pdf'
    return send_file(file_path, as_attachment=True)

def download_cs1():
    file_path = 'static/cs1.pdf'
    return send_file(file_path, as_attachment=True)

def download_cs2():
    file_path = 'static/cs2.pdf'
    return send_file(file_path, as_attachment=True)

def download_cs3():
    file_path = 'static/cs3.pdf'
    return send_file(file_path, as_attachment=True)

def download_cs4():
    file_path = 'static/cs4.pdf'
    return send_file(file_path, as_attachment=True)

def admin_testimonial_creation():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == 'POST':
                student_name = request.form['student_name']
                course_name = request.form['course_name']
                comment = request.form['comment']
                testimonial_status = request.form['testimonial_status']
                insert_query = """INSERT INTO testimonials (student_name, course_name, comment,testimonial_status) 
                                VALUES (?, ?, ?, ?)"""
                cursor.execute(insert_query, (student_name, course_name, comment,testimonial_status))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('admin_panel',email_person="admin"))
            return render_template("admin_testimonial_creation.html")
        else:
            return redirect("/")
    except Exception as admin_testimonial_creation_error:
        logging.error("****An Error Occurred in admin_testimonial_creation method" + "\n" + "An error occurred in: %s", str(admin_testimonial_creation_error),exc_info=True)
        return redirect('/')

def admin_testimonial_view():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select * from testimonials order by testimonial_id desc")
            testimonials = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("admin_testimonial_view.html", testimonials=testimonials)
        else:
            return redirect("/")
    except Exception as admin_testimonial_view_error:
        logging.error("****An Error Occurred in admin_testimonial_view method" + "\n" + "An error occurred in: %s", str(admin_testimonial_view_error), exc_info=True)
        return redirect('/')

def admin_testimonial_edit():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST' and 'testimonial_id' in request.form:
                testimonial_id = request.form['testimonial_id']
                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute("select * from testimonials where testimonial_id =?",(testimonial_id,))
                testimonials = cursor.fetchall()
                return render_template("admin_testimonial_edit.html", testimonials=testimonials)
            return render_template("admin_testimonial_edit.html")
        else:
            return redirect("/")
    except Exception as admin_testimonial_edit_error:
        logging.error("****An Error Occurred in admin_testimonial_edit method" + "\n" + "An error occurred in: %s", str(admin_testimonial_edit_error),exc_info=True)
        return redirect('/')

def admin_testimonial_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST':
                testimonial_id = request.form['testimonial_id']
                student_name = request.form['student_name']
                course_name = request.form['course_name']
                comment = request.form['comment']
                testimonial_status = request.form['testimonial_status']
                connection = connect_to_database()
                cursor = connection.cursor()
                update_query = """UPDATE testimonials SET student_name = ?, course_name = ?, comment = ?, testimonial_status=? WHERE
                             testimonial_id = ?"""
                cursor.execute(update_query, (student_name, course_name, comment, testimonial_status, testimonial_id))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('admin_panel',email_person="admin"))
            return render_template("admin_testimonial_edit.html")
        else:
            return redirect("/")
    except Exception as admin_testimonial_update_error:
        logging.error("****An Error Occurred in admin_testimonial_update method" + "\n" + "An error occurred in: %s", str(admin_testimonial_update_error),exc_info=True)
        return redirect('/')

def admin_testimonial_edit_delete():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            testimonial_id = request.form['testimonial_id']
            cursor.execute(f"DELETE FROM testimonials WHERE testimonial_id=?",(testimonial_id,))
            connection.commit()
            connection.close()
            return redirect(url_for('admin_panel',email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_testimonial_edit_delete_error:
        logging.error("****An Error Occurred in admin_testimonial_edit method" + "\n" + "An error occurred in: %s", str(admin_testimonial_edit_delete_error),exc_info=True)
        return redirect('/')

def admin_testimonial_for_individual_course_creation():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select course_id, course_name from courses order by course_id desc")
            course_id_and_course_name = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("admin_testimonial_for_individual_course_creation.html", course_id_and_course_name=course_id_and_course_name)
        else:
            return redirect("/")
    except Exception as admin_testimonial_for_individual_course_creation_error:
        logging.error("****An Error Occurred in admin_testimonial_for_individual_course_creation method" + "\n" + "An error occurred in: %s", str(admin_testimonial_for_individual_course_creation_error), exc_info=True)
        return redirect('/')

def admin_testimonial_for_individual_course_creation_page():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            if request.method == 'POST':
                course_id = request.form["course_id"]
                return render_template("admin_testimonial_for_individual_course_creation_page.html", course_id=course_id)
            return render_template("admin_testimonial_for_individual_course_creation_page.html")
        else:
            return redirect("/")
    except Exception as admin_testimonial_for_individual_course_creation_page_error:
        logging.error("****An Error Occurred in admin_testimonial_for_individual_course_creation_page method" + "\n" + "An error occurred in: %s", str(admin_testimonial_for_individual_course_creation_page_error), exc_info=True)
        return redirect('/')

def admin_testimonial_for_individual_course_upload():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == 'POST':
                course_id = request.form['course_id']
                page_check = request.form['page_check']
                student_name1= request.form['student_name1']
                company_name1 = request.form['company_name1']
                feedback1 = request.form['feedback1']
                student_name = request.form.getlist('student_name')
                company_name = request.form.getlist('company_name')
                feedback = request.form.getlist('feedback')
                testimonial_date = request.form['testimonial_date']

                student_name_result = '$'.join([student_name1] + student_name)
                company_name_result = '$'.join([company_name1] + company_name)
                feedback_result = '$'.join([feedback1] + feedback)

                update_query = """UPDATE courses SET testimonial_student_name = ?, testimonial_company_name = ?,
                testimonial_feedback = ?, testimonial_date = ? WHERE course_id = ?"""
                cursor.execute(update_query, (student_name_result, company_name_result, feedback_result, testimonial_date, course_id))
                connection.commit()
                connection.close()
                if page_check == "creation_page":
                    return redirect(url_for("admin_testimonial_for_individual_course_creation",email_person="admin"))
                elif page_check == "edition_page":
                    return redirect(url_for("admin_testimonial_for_individual_course_edition",email_person="admin"))
            return render_template("admin_testimonial_for_individual_course_creation_page.html")
        else:
            return redirect("/")
    except Exception as admin_testimonial_for_individual_course_upload_error:
        logging.error("****An Error Occurred in admin_testimonial_for_individual_course_upload method" + "\n" + "An error occurred in: %s", str(admin_testimonial_for_individual_course_upload_error), exc_info=True)
        return redirect('/')

def admin_testimonial_for_individual_course_edition():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()

            cursor.execute("select course_id, course_name from courses order by course_id desc")
            course_id_and_course_name = cursor.fetchall()

            cursor.close()
            connection.close()
            return render_template("admin_testimonial_for_individual_course_edition.html", course_id_and_course_name=course_id_and_course_name)
        else:
            return redirect("/")
    except Exception as admin_testimonial_for_individual_course_edition_error:
        logging.error("****An Error Occurred in admin_testimonial_for_individual_course_edition method" + "\n" + "An error occurred in: %s", str(admin_testimonial_for_individual_course_edition_error), exc_info=True)
        return redirect('/')

def admin_testimonial_for_individual_course_edition_page():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            if request.method == 'POST':
                course_id = request.form["course_id"]
                cursor.execute("""select testimonial_student_name,testimonial_company_name,
                                testimonial_feedback,testimonial_date from courses WHERE course_id = ?""",(course_id,))
                details = cursor.fetchone()
                testimonial_date = details[3]
                if testimonial_date is not None:
                    testimonial_student_name = details[0].split("$")
                    testimonial_company_name = details[1].split("$")
                    testimonial_feedback = details[2].split("$")
                    return render_template("admin_testimonial_for_individual_course_edition_page.html", course_id=course_id, testimonial_date=testimonial_date, testimonial_student_name=testimonial_student_name, testimonial_company_name=testimonial_company_name, testimonial_feedback=testimonial_feedback)
                else:
                    return render_template("admin_testimonial_for_individual_course_edition_page.html", course_id=course_id, testimonial_date=testimonial_date, testimonial_student_name="", testimonial_company_name="", testimonial_feedback="")
            cursor.close()
            connection.close()
            return render_template("admin_testimonial_for_individual_course_edition_page.html")
        else:
            return redirect("/")
    except Exception as admin_testimonial_for_individual_course_edition_page_error:
        logging.error("****An Error Occurred in admin_testimonial_for_individual_course_edition_page method" + "\n" + "An error occurred in: %s", str(admin_testimonial_for_individual_course_edition_page_error), exc_info=True)
        return redirect('/')

def admin_seo():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("select seo_value from seo")
            seo_fetched_value = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template("admin_seo.html",seo_fetched_value=seo_fetched_value)
        else:
            return redirect("/")
    except Exception as admin_seo_error:
        logging.error("****An Error Occurred in admin_seo method" + "\n" + "An error occurred in: %s", str(admin_seo_error), exc_info=True)
        return redirect('/')

def admin_seo_update():
    try:
        email_person = request.args.get('email_person')
        if email_person == "admin":
            connection = connect_to_database()
            cursor = connection.cursor()
            seo_name=request.form['seo_name']
            update_query = "update seo set seo_value=? where seo_id=1"
            cursor.execute(update_query,(seo_name,))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('admin_panel',email_person="admin"))
        else:
            return redirect("/")
    except Exception as admin_seo_error:
        logging.error("****An Error Occurred in admin_seo method" + "\n" + "An error occurred in: %s", str(admin_seo_error), exc_info=True)
        return redirect('/')