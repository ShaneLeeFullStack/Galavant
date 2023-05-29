"""
This file defines the database models
"""
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

db.define_table('user_profile',
                Field('name', ),
                Field('phone_number', 'text', required=True),
                Field('email', default=get_user_email),
                )

db.define_table('substance_table',
                Field('substance_name', 'text'),
                Field('lethal', 'boolean'),
                Field('category', 'text')
                )

db.define_table('trip_reports',
                Field('date', 'text', default=get_time),
                Field('user_id', 'reference user_profile'),
                Field('title', 'text'),
                Field('substance_id', 'reference substance_table', required=True),
                Field('report_content', 'text'),
                Field('difficult_headspace', 'boolean'),
                Field('anti_depressants', 'boolean'),
                Field('is_showing', 'reference trip_reports')
                )

db.trip_reports.date.readable = False
db.trip_reports.user_id.readable = False
db.user_profile.id.readable = False
db.user_profile.email.readable = False
db.commit()
