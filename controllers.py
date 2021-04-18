from pydal.validators import *
import uuid
from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner
from yatl.helpers import A
from .common import db, session, T, cache, auth, signed_url
from py4web.utils.auth import Auth
import datetime
from .textFunc import rivers_func
from .weatherScrapper import weatherInfo

url_signer = URLSigner(session)
def get_time():
    return datetime.datetime.utcnow()

def get_user_id():
    user_id = db(db.user_profile.email == auth.current_user.get('email')).select()
    return user_id[0].id

#def logged_in_check():
#    if auth.get_user() is None:
#        return False
#    else:
#        return True

@action('index', method=['GET', 'POST'])
@action.uses('index.html', auth.user, db, session)
def home_page():
    #if (db(db.user_profile.email == auth.current_user.get('email')).select() == None):
    #    print("user has not created their profile yet")
    #    db.user_profile.insert(email=auth.current_user.get('email'))
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()
    current_user_row = db(db.user_profile.id == current_user_id).select()
    return dict(
        fetch_tags=URL('fetch_tags', signer=url_signer),
        map_page=URL('map_page', signer=url_signer),
        fetch_substance_table=URL('fetch_substance_table', signer=url_signer),
        update_report=URL('update_report', signer=url_signer),
        delete_report=URL('delete_report', signer=url_signer),
        fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),
        user_email=auth.current_user.get('email'),
        submit_trip_report_url=URL('submit_trip_report', signer=url_signer),
        current_user_row=current_user_row,
        fetch_profile_fields=URL('fetch_profile_fields', signer=url_signer),
        create_profile=URL('create_profile', signer=url_signer),
        create_profile_page=URL('create_profile_page', signer=url_signer),
        need_help=URL('need_help', signer=url_signer)
    )

@action('fetch_substance_table', method=['GET', 'POST'])
@action.uses('submit_trip_report_form.html', db, auth.user, session)
def fetch_substance_table():
    substance_table = db().select(db.substance_table.ALL)
    return dict(substance_array=substance_table)

@action('fetch_profile_fields', method=['GET', 'POST'])
@action.uses(auth.user, session, db)
def fetch_profile_fields():
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()
    almost_profile_fields = db(db.user_profile.id == current_user_id).select().as_list()
    profile_fields = almost_profile_fields
    tripsitter_array = db(db.user_profile.tripsitter == True).select().first()
    return dict(profile_fields=profile_fields, tripsitter_array=tripsitter_array)

@action('fetch_trip_reports', method=['GET', 'POST'])
@action.uses(auth.user, session, db)
def fetch_trip_reports():
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()
    trip_reports_home_page = db(db.trip_reports.user_id == current_user_id.id)\
        .select(orderby=~db.trip_reports.date).as_list()
    for report in trip_reports_home_page:
        substance = db.substance_table[report["substance_id"]].as_dict()
        report["substance_name"] = substance["substance_name"]
    return dict(trip_reports=trip_reports_home_page,
               fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),)

@action('fetch_tags', method=['GET', 'POST'])
@action.uses(auth.user, session, db)
def fetch_tags():
    user_report_tags = db(db.text_analysis.user_profile_id == get_user_id()).select().as_list()
    return dict(user_report_tags=user_report_tags)

@action('submit_trip_report_page', method=['GET'])
@action.uses('submit_trip_report_form.html', auth.user, session, db)
def submit_trip_report_page():
    substance_array = db(db.substance_table).select()
    return dict(substance_array=substance_array,
                fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),
                fetch_profile_fields=URL('fetch_profile_fields', signer=url_signer),
                fetch_substance_table=URL('fetch_substance_table', signer=url_signer),
                fetch_tags=URL('fetch_tags', signer=url_signer),
                )

@action('submit_trip_report', method='POST')
@action.uses('submit_trip_report_form.html', auth.user, session, db)
def submit_trip_report():
    substance_array = db(db.substance_table).select()
    substance_name = request.params.get('substance_name')
    substance_row = db(db.substance_table.substance_name ==
                      substance_name).select()
    substance_id = substance_row[0].id
    title = request.params.get('title')
    report_content = request.params.get('report_content')
    dif_headspace = request.params.get('dif_headspace')
    anti_depress = request.params.get('anti_depress')
    at_festival = request.params.get('at_festival')
    new_trip_report_id = db.trip_reports.insert(title=title,
                           substance_id=substance_id,
                           user_id=get_user_id(),
                           report_content=report_content,
                           difficult_headspace=dif_headspace,
                           anti_depressants=anti_depress,
                           at_festival=at_festival,
                           )
    newest_trip_report = db.trip_reports[new_trip_report_id]
    analyze_this_content = newest_trip_report.report_content
    tags_list = rivers_func(analyze_this_content)
    new_id = db.text_analysis.insert(id=new_trip_report_id,
                                     user_profile_id=get_user_id(),
                                     tags=tags_list)
    redirect('submit_trip_report_page')
    return dict(trip_reports=newest_trip_report.as_dict(),
                fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),
                fetch_profile_fields=URL('fetch_profile_fields', signer=url_signer),
                fetch_substance_table=URL('fetch_substance_table', signer=url_signer),
                substance_array=substance_array)

@action('create_profile_page', method=['GET'])
@action.uses('super_create_profile_form.html', auth.user, session, db)
def create_profile_page():
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()
    current_user_row = db(db.user_profile.id == current_user_id).select()
    return dict(
        fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),
        fetch_profile_fields=URL('fetch_profile_fields', signer=url_signer),
        current_user_row=current_user_row,
        fetch_tags=URL('fetch_tags', signer=url_signer),
    )


@action('create_profile', method=['GET', 'POST'])
@action.uses('super_create_profile_form.html', auth.user, session, db)
def create_profile():
    name = request.params.get('name')
    gender_identity = request.params.get('gender_identity')
    phone_number = request.params.get('phone_number')
    city = request.params.get('city')
    tripsitter = request.params.get('tripsitter')
    safety_contact_name = request.params.get('safety_contact_name')
    safety_contact_phone_number = request.params.get('safety_contact_phone_number')
    db.user_profile.update_or_insert(
        db.user_profile.email == auth.current_user.get('email'),
        name=name,
        phone_number=phone_number,
        gender_identity=gender_identity,
        email=auth.current_user.get('email'),
        city=city,
        tripsitter=tripsitter,
        safety_contact_name=safety_contact_name,
        safety_contact_phone_number=safety_contact_phone_number,
    )
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()
    current_user_row = db(db.user_profile.id == current_user_id).select()
    redirect('create_profile_page')
    return dict(current_user_row=current_user_row,
                fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),
                fetch_profile_fields=URL('fetch_profile_fields', signer=url_signer)
                )

@action('update_report', method='POST')
@action.uses(db, auth.user, session)
def update_report():
    id = request.json.get('id')
    report_content = request.json.get('report_content')
    db(db.trip_reports.id == id).update(report_content=report_content)
    tags_list = rivers_func(report_content)
    print(report_content)
    print(tags_list)
    db(db.text_analysis.id == id).update(
        tags=tags_list,
    )

@action('delete_report', method=['GET', 'POST'])
@action.uses(session, db, auth.user)
def delete_report():
    id = request.json.get('id')
    db(db.trip_reports.id == id).delete()
    return "ok"

@action('map_page', method=['GET', 'POST'])
@action.uses('map_form.html', session, db, auth.user)
def map_page():
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()
    user_city_location = db(db.user_profile.id == current_user_id).select(db.user_profile.city)
    weather_string = weatherInfo()
    return dict(
        user_city=user_city_location,
        fetch_profile_fields=URL('fetch_profile_fields', signer=url_signer),
        weather_string=weather_string
    )

@action('books_movies', method=['GET', 'POST'])
@action.uses('books_movies_form.html', db, session, auth.user)
def books_movies():
    weather_string = weatherInfo()
    return dict(
        books_movies=URL('books_movies', signer=url_signer),
        weather_string=weather_string
    )

@action('journey_safe', method=['GET', 'POST'])
@action.uses('journey_safe_form.html', db, auth.user, session)
def journey_safe():
    journey_substance_name = request.params.get('journey_substance_name')
    dose = request.params.get('dosage_amount')
    units = request.params.get('dosage_units')
    dif_headspace = request.params.get('dif_headspace')
    anti_depress = request.params.get('anti_depress')
    at_a_festival = request.params.get('at_a_festival')
    substance_table = db(db.substance_table.substance_name == journey_substance_name).select()
    current_user_row = db(db.user_profile.id == get_user_id()).select()
    return dict(substance_table=substance_table, current_user_row=current_user_row,
                fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),
                fetch_profile_fields=URL('fetch_profile_fields', signer=url_signer),
                fetch_tags=URL('fetch_tags', signer=url_signer),
                )

@action('need_help', method=['GET','POST'])
@action.uses('need_help.html', db, session, auth.user)
def need_help():
    current_user_row = db(db.user_profile.id == get_user_id()).select()
    return dict(current_user_row=current_user_row)

@action('map_cont', method=['GET', 'POST'])
@action.uses('map.html', db, session, auth.user)
def map_cont():
    return dict(map_cont=URL('map_cont', signer=url_signer))


