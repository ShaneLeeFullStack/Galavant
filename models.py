#ssh -i "awesome_galavant.pem" ubuntu@ec2-18-188-117-20.us-east-2.compute.amazonaws.com
import datetime

from .common import db, Field, auth
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email')

def get_first_name():
    return auth.current_user.get('first_name')

def get_time():
    return datetime.datetime.utcnow()

def get_user_id():
    user_id = db(db.user_profile.email == auth.current_user.get('email')).select()
    return user_id[0].id

# User Profile Table
db.define_table('user_profile',
                Field('name', 'text'),
                Field('gender_identity'),
                Field('phone_number', 'text', required=True),
                Field('email', default=get_user_email),
                Field('city', 'text'),
                Field('tripsitter', 'boolean'),
                Field('safety_contact_name', 'text'),
                Field('safety_contact_phone_number', 'text')
                )

# Substance Table
db.define_table('substance_table',
                Field('substance_name', 'text'),
                Field('category', 'text'),
                )

# Trip Reports Table
db.define_table('trip_reports',
                Field('date', 'text', default=get_time),
                Field('user_id', 'reference user_profile'),
                Field('title', 'text'),
                Field('substance_id', 'reference substance_table', required=True),
                Field('report_content', 'text'),
                Field('difficult_headspace', 'boolean'),
                Field('anti_depressants', 'boolean'),
                Field('at_festival', 'boolean'),
                Field('is_showing', 'reference trip_reports')
                )

# Text Analysis Table
db.define_table('text_analysis',
                Field('id', 'reference trip_reports'),
                Field('user_profile_id', 'reference user_profile'),
                Field('tags', 'list:string'),
                migrate=True)

db.trip_reports.date.readable = False
db.trip_reports.user_id.readable = False
db.user_profile.id.readable = False
db.user_profile.email.readable = False
db.commit()
