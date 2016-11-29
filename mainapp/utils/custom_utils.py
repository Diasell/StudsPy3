# -*- coding: utf-8 -*-
import datetime, random, string
from PIL import Image
from datetime import timedelta

from ..models.helpermodels import StartSemester


def group_year(date_started):
    """
    :param date_started: date when group was created
    :return: str that represents the course for the group
    """
    today = datetime.date.today()
    course = int(((today - date_started).days / 365) + 1)
    return str(course) + u"-й курс"


def for_ios_format(response):
    """
    Method created specially to sort data in the way that
    swift json parser would be able to handle.
    Used in get_faculties structure method
    """
    updated_response = dict()
    for key in response:
        group_t = dict()
        for group in response[key]:
            if group[0] not in group_t:
                course = dict()
                course[group[2]] = group[1]
                group_t[group[0]] = course
            else:
                courses = group_t[group[0]]
                courses[group[2]] = group[1]
                group_t[group[0]] = courses
        updated_response[key] = group_t
    return updated_response


def ifweekiseven(todaysdata, datastart):
    """
    Helper function that tracks what week is now from the certain
    day. For us it important when we calculate schedule as we  have to
    know whether it is even week or odd
    :param todaysdata: type datetime
    :param datastart: data when semester starts
    """

    weekday1e = datastart.weekday()
    mondaydelta = timedelta(weekday1e)
    monday = datastart - mondaydelta
    delta = ((todaysdata - monday) / 7).days + 1

    if delta % 2 == 0:
        return True
    else:
        return False


def get_weektype(date):
    """
    Checks what is the weektype
    :param date: datetime.date type value
    :return: True/False/None
    """
    semesters = StartSemester.objects.all()
    for semester in semesters:
        if (semester.semesterstart <= date) \
                and (semester.semesterend >= date):
            return ifweekiseven(date, semester.semesterstart)
    return None


def is_valid_image(photo):
    """uses Pillow to check whether file is an image"""

    image = Image.open(photo)
    valid_formats = ['jpeg', 'jpg', 'png']
    if image.format.lower() in valid_formats:
        return True
    return False


def format_time(strng):
    x = strng.replace(" ", '')
    y = x.replace('.', '_')
    result = y.replace(':', '_')
    return result


def custom_logger(data, user):
    """
    :param data: request.data  that comes from the clients request
    :param user: username
    creates and saves new file with request data
    """
    path = "../media/logs/"
    time = format_time(str(datetime.datetime.now()))
    filename = path + time + '.log'
    with open(filename, "w+") as f:
        f.write(str(user) + ':' + str(data))



def generate_new_password():
    """
    :return: String that can be used as password for User object
    """
    new_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(8))
    return new_password


def create_response_scelet(status, message, data):
    response = dict()
    response['status'] = status
    response['message'] = message
    response['data']= data
    return response


def prettify_phone(phonenumber):
    """
    make phone number more readable
    :param phonenumber: 380988257176
    :return: 38(098)-825-71-76
    """
    number = str(phonenumber)
    return number[0:2] + '(' + number[2:5] + ')-' + number[5:8] + '-' + number[8:10] + '-' + number[10:]

