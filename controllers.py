from pydal.validators import *
import uuid
from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner
from yatl.helpers import A
from .common import db, session, T, cache, auth, signed_url
from py4web.utils.auth import Auth
import datetime

url_signer = URLSigner(session)
def get_time():
    return datetime.datetime.utcnow()

def get_user_id():
    user_id = db(db.user_profile.email == auth.current_user.get('email')).select()
    return user_id[0].id

@action('index', method=['GET', 'POST'])
@action.uses('index.html', auth.user, db, session)
def home_page():
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()
    if current_user_id == None:
        redirect(URL('create_profile'))
    return dict(
        fetch_substance_table=URL('fetch_substance_table', signer=url_signer),
        update_report=URL('update_report', signer=url_signer),
        delete_report=URL('delete_report', signer=url_signer),
        fetch_trip_reports=URL('fetch_trip_reports', signer=url_signer),
        user_email=auth.current_user.get('email'),
        submit_trip_report_url=URL('submit_trip_report', signer=url_signer),
    )

@action('fetch_substance_table', method=['GET', 'POST'])
@action.uses('submit_trip_report_form.html', db, auth.user, session)
def fetch_substance_table():
    substance_table = db().select(db.substance_table.ALL)
    return dict(substance_array=substance_table)

@action('fetch_trip_reports', method='GET')
@action.uses(auth.user, session, db)
def fetch_trip_reports():
    current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
        .select().first()

    trip_reports_home_page = db(db.trip_reports.user_id == current_user_id.id)\
        .select(orderby=~db.trip_reports.date).as_list()
    for report in trip_reports_home_page:
        substance = db.substance_table[report["substance_id"]].as_dict()
        report["substance_name"] = substance["substance_name"]
    return dict(trip_reports=trip_reports_home_page)

@action('fetch_trip_reports', method='POST')
@action.uses(db, auth.user, session)
def save_trip_reports():
    is_showing = request.json.get('is_showing')
    report_content = request.json.get('report_content')
    new_trip_report_id = db.trip_reports.update_or_insert(
        report_content=report_content,
        is_showing=is_showing,
    )
    return dict(report_content=report_content)

@action('define_substance', method='POST')
@action.uses('define_substance_form.html', auth.user, session, db)
def define_substance():
    substance = request.params.get('substance_name')
    lethal = request.params.get('lethal')
    category = request.params.get('category')
    new_substance_id = db.substance_table.insert(
        substance_name=substance,
        lethal=lethal,
        category=category
    )
    newest_substance = db.substance_table[new_substance_id]
    return dict(substance_table=newest_substance.as_dict())

@action('define_substance_page', method='GET')
@action.uses('define_substance_form.html', auth.user, session, db)
def define_substance_page():
    return dict()

@action('create_profile_page', method=['GET', 'POST'])
@action.uses('create_profile_form.html', auth.user, session, db)
def create_profile_page():
    return dict()

@action('submit_trip_report_page', method=['GET'])
@action.uses('submit_trip_report_form.html', auth.user, session, db)
def submit_trip_report_page():
    substance_array = db(db.substance_table).select()
    #current_user_id = db(db.user_profile.email == auth.current_user.get('email')) \
    #    .select().first()
    #if current_user_id == None:
    current_user_first_name = db(db.user_profile.email == auth.current_user.get('email')).select()
    if current_user_first_name[0].name == None:
        redirect(URL('create_profile'))
    return dict(substance_array=substance_array)

@action('submit_trip_report', method='POST')
@action.uses('submit_trip_report_form.html', auth.user, session, db)
def submit_trip_report():
    substance_array = db(db.substance_table).select()
    substance_name = request.params.get('substance_name')
    substance_row = db(db.substance_table.substance_name ==
                      substance_name).select()
    substance_id = substance_row[0].id
    if db.substance_table[substance_id] is None:
        redirect(URL('define_substance'))
    report_content = request.params.get('report_content')
    dif_headspace = request.params.get('dif_headspace')
    anti_depress = request.params.get('anti_depress')
    title = request.params.get('title')
    print(dif_headspace)
    print(anti_depress)
    new_trip_report_id = db.trip_reports.insert(title=title,
                           substance_id=substance_id,
                           user_id=get_user_id(),
                           report_content=report_content,
                           difficult_headspace=dif_headspace,
                           anti_depressants=anti_depress,
                           )
    newest_trip_report = db.trip_reports[new_trip_report_id]
    return dict(trip_reports=newest_trip_report.as_dict(),
                substance_array=substance_array)


@action('create_profile', method=['GET', 'POST'])
@action.uses('create_profile_form.html', auth.user, session, db)
def create_profile():
    name = request.params.get('name')
    phone_number = request.params.get('phone_number')
    new_user_id = db.user_profile.insert(
        name=name,
        phone_number=phone_number,
        email=auth.current_user.get('email')
    )
    newest_user = db.user_profile[new_user_id]
    return dict(user_profile=newest_user.as_dict())

@action('update_report', method='POST')
@action.uses(db, auth.user, session)
def update_report():
    id = request.json.get('id')
    report_content = request.json.get('report_content')
    db(db.trip_reports.id == id).update(report_content=report_content)

@action('delete_report', method=['GET', 'POST'])
@action.uses(session, db, auth.user)
def delete_report():
    id = request.json.get('id')
    db(db.trip_reports.id == id).delete()
    return "ok"