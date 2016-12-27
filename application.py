#
# application.py
# Nicholas Boucher 2017
#
# Contains the main application code for NOVA. This code maps
# all URL endpoints to FLASK functions
#

from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from database_models import *
from helpers import *

# create Flask server
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

#set cryptographic key for Sessions
app.secret_key = "some really good encryption string"

# setup database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

        
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_grant')
def new_grant():
    """ Inserts new grant applications into database from query strings passed by qualtrics survey """
    
    # get arguments from query string
    args = get_grant_args(request.query_string)
    
    # Verify security key
    sec_key = Config.query.filter_by(key='security_key').first().value
    if not args.get('k') or sec_key != args.get('k')[0]:
        return "Invalid Security Key. You do not have access to this system."
    
    # Get Next Grant ID
    council_semester = Config.query.filter_by(key='council_semester').first()
    current_week = Config.query.filter_by(key='grant_week').first()
    grant_prefix = council_semester.value + '-' + current_week.value
    grant_number = Grant_Count.query.filter_by(grant_week=grant_prefix).first()
    # This is not atomic, which seems like a potential problem...
    grant_number.num_grants += 1
    db.session.commit()
    grant_id = grant_prefix + "-" + str(grant_number.num_grants)
    
    # Create New Grant
    grant = Grant(grant_id)
    
    # Add Grant Values from Parsed Query String
    if args.get('amount_requested'): grant.amount_requested = float(args.get('amount_requested')[0])
    if args.get('is_collaboration'): grant.is_collaboration = (True if args.get('is_collaboration')[0] == "Yes" else False)
    if args.get('collaborators'): grant.collaborators = args.get('collaborators')[0]
    if args.get('collaboration_explanation'): grant.collaboration_explanation = args.get('collaboration_explanation')[0]
    if args.get('contact_first_name'): grant.contact_first_name = args.get('contact_first_name')[0]
    if args.get('contact_last_name'): grant.contact_last_name = args.get('contact_last_name')[0]
    if args.get('contact_email'): grant.contact_email = args.get('contact_email')[0]
    if args.get('contact_phone'): grant.contact_phone = args.get('contact_phone')[0]
    if args.get('contact_role'): grant.contact_role = args.get('contact_role')[0]
    if args.get('is_upfront'): grant.is_upfront = (True if args.get('is_upfront')[0] == "1" else False)
    if args.get('organization'): grant.organization = args.get('organization')[0]
    if args.get('tax_id'): grant.tax_id = args.get('tax_id')[0]
    if args.get('project'): grant.project = args.get('project')[0]
    if args.get('project_description'): grant.project_description = args.get('project_description')[0]
    if args.get('is_event'): grant.is_event = (True if args.get('is_event')[0] == "Event" else False)
    if args.get('project_location'): grant.project_location = args.get('project_location')[0]
    if args.get('project_start'): grant.project_start = datetime.strptime(args.get('project_start')[0], '%m/%d/%Y')
    if args.get('project_end'): grant.project_end = datetime.strptime(args.get('project_end')[0], '%m/%d/%Y')
    if args.get('college_attendees'): grant.college_attendees = int(args.get('college_attendees')[0])
    if args.get('facebook_link'): grant.facebook_link = args.get('facebook_link')[0]
    if args.get('revenue1_type'): grant.revenue1_type = args.get('revenue1_type')[0]
    if args.get('revenue1_description'): grant.revenue1_description = args.get('revenue1_description')[0]
    if args.get('revenue1_amount'): grant.revenue1_amount = float(args.get('revenue1_amount')[0])
    if args.get('revenue2_type'): grant.revenue2_type = args.get('revenue2_type')[0]
    if args.get('revenue2_description'): grant.revenue2_description = args.get('revenue2_description')[0]
    if args.get('revenue2_amount'): grant.revenue2_amount = float(args.get('revenue2_amount')[0])
    if args.get('revenue3_type'): grant.revenue3_type = args.get('revenue3_type')[0]
    if args.get('revenue3_description'): grant.revenue3_description = args.get('revenue3_description')[0]
    if args.get('revenue3_amount'): grant.revenue3_amount = float(args.get('revenue3_amount')[0])
    if args.get('revenue4_type'): grant.revenue4_type = args.get('revenue4_type')[0]
    if args.get('revenue4_description'): grant.revenue4_description = args.get('revenue4_description')[0]
    if args.get('revenue4_amount'): grant.revenue4_amount = float(args.get('revenue4_amount')[0])
    if args.get('revenue5_type'): grant.revenue5_type = args.get('revenue5_type')[0]
    if args.get('revenue5_description'): grant.revenue5_description = args.get('revenue5_description')[0]
    if args.get('revenue5_amount'): grant.revenue5_amount = float(args.get('revenue5_amount')[0])
    if args.get('revenue6_type'): grant.revenue6_type = args.get('revenue6_type')[0]
    if args.get('revenue6_description'): grant.revenue6_description = args.get('revenue6_description')[0]
    if args.get('revenue6_amount'): grant.revenue6_amount = float(args.get('revenue6_amount')[0])
    if args.get('revenue7_type'): grant.revenue7_type = args.get('revenue7_type')[0]
    if args.get('revenue7_description'): grant.revenue7_description = args.get('revenue7_description')[0]
    if args.get('revenue7_amount'): grant.revenue7_amount = float(args.get('revenue7_amount')[0])
    if args.get('revenue8_type'): grant.revenue8_type = args.get('revenue8_type')[0]
    if args.get('revenue8_description'): grant.revenue8_description = args.get('revenue8_description')[0]
    if args.get('revenue8_amount'): grant.revenue8_amount = float(args.get('revenue8_amount')[0])
    if args.get('revenue9_type'): grant.revenue9_type = args.get('revenue9_type')[0]
    if args.get('revenue9_amount'): grant.revenue9_amount = float(args.get('revenue9_amount')[0])
    if args.get('revenue10_type'): grant.revenue10_type = args.get('revenue10_type')[0]
    if args.get('revenue10_description'): grant.revenue10_description = args.get('revenue10_description')[0]
    if args.get('revenue10_amount'): grant.revenue10_amount = float(args.get('revenue10_amount')[0])
    if args.get('app_expense1_type'): grant.app_expense1_type = args.get('app_expense1_type')[0]
    if args.get('app_expense1_description'): grant.app_expense1_description = args.get('app_expense1_description')[0]
    if args.get('app_expense1_amount'): grant.app_expense1_amount = float(args.get('app_expense1_amount')[0])
    if args.get('app_expense2_type'): grant.app_expense2_type = args.get('app_expense2_type')[0]
    if args.get('app_expense2_description'): grant.app_expense2_description = args.get('app_expense2_description')[0]
    if args.get('app_expense2_amount'): grant.app_expense2_amount = float(args.get('app_expense2_amount')[0])
    if args.get('app_expense3_type'): grant.app_expense3_type = args.get('app_expense3_type')[0]
    if args.get('app_expense3_description'): grant.app_expense3_description = args.get('app_expense3_description')[0]
    if args.get('app_expense3_amount'): grant.app_expense3_amount = float(args.get('app_expense3_amount')[0])
    if args.get('app_expense4_type'): grant.app_expense4_type = args.get('app_expense4_type')[0]
    if args.get('app_expense4_description'): grant.app_expense4_description = args.get('app_expense4_description')[0]
    if args.get('app_expense4_amount'): grant.app_expense4_amount = float(args.get('app_expense4_amount')[0])
    if args.get('app_expense5_type'): grant.app_expense5_type = args.get('app_expense5_type')[0]
    if args.get('app_expense5_description'): grant.app_expense5_description = args.get('app_expense5_description')[0]
    if args.get('app_expense5_amount'): grant.app_expense5_amount = float(args.get('app_expense5_amount')[0])
    if args.get('app_expense6_type'): grant.app_expense6_type = args.get('app_expense6_type')[0]
    if args.get('app_expense6_description'): grant.app_expense6_description = args.get('app_expense6_description')[0]
    if args.get('app_expense6_amount'): grant.app_expense6_amount = float(args.get('app_expense6_amount')[0])
    if args.get('app_expense7_type'): grant.app_expense7_type = args.get('app_expense7_type')[0]
    if args.get('app_expense7_description'): grant.app_expense7_description = args.get('app_expense7_description')[0]
    if args.get('app_expense7_amount'): grant.app_expense7_amount = float(args.get('app_expense7_amount')[0])
    if args.get('app_expense8_type'): grant.app_expense8_type = args.get('app_expense8_type')[0]
    if args.get('app_expense8_description'): grant.app_expense8_description = args.get('app_expense8_description')[0]
    if args.get('app_expense8_amount'): grant.app_expense8_amount = float(args.get('app_expense8_amount')[0])
    if args.get('app_expense9_type'): grant.app_expense9_type = args.get('app_expense9_type')[0]
    if args.get('app_expense9_description'): grant.app_expense9_description = args.get('app_expense9_description')[0]
    if args.get('app_expense9_amount'): grant.app_expense9_amount = float(args.get('app_expense9_amount')[0])
    if args.get('app_expense10_type'): grant.app_expense10_type = args.get('app_expense10_type')[0]
    if args.get('app_expense10_description'): grant.app_expense10_description = args.get('app_expense10_description')[0]
    if args.get('app_expense10_amount'): grant.app_expense10_amount = float(args.get('app_expense10_amount')[0])
    if args.get('app_expense11_type'): grant.app_expense11_type = args.get('app_expense11_type')[0]
    if args.get('app_expense11_description'): grant.app_expense11_description = args.get('app_expense11_description')[0]
    if args.get('app_expense11_amount'): grant.app_expense11_amount = float(args.get('app_expense11_amount')[0])
    if args.get('app_expense12_type'): grant.app_expense12_type = args.get('app_expense12_type')[0]
    if args.get('app_expense12_description'): grant.app_expense12_description = args.get('app_expense12_description')[0]
    if args.get('app_expense12_amount'): grant.app_expense12_amount = float(args.get('app_expense12_amount')[0])
    if args.get('application_comments'): grant.application_comments = args.get('application_comments')[0]
    
    try:
        db.session.add(grant)
        db.session.commit()
    except IntegrityError:
        return "Error: Grant already exists"
    
    return "Inserted"
    
@app.route('/receipts')
def receipts():
    """ Adds completed project info (including receipts) to existing grant record """
    
    # get arguments from query string
    args = get_grant_args(request.query_string)

@app.route('/grant/<grant>')
def grant(grant):
    """ Retrieves grant info for applicants to track grant progress """
    return grant.upper()