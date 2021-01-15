###################
#### imports ######
###################

from project import app, db
from project.models import BlogPost
from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from functools import wraps

####################
#### config ########
####################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

#########################
### helper functions ####
#########################

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

######################
#### routes ##########
######################

# use decorators to link the function to the url
@home_blueprint.route('/')
@login_required
def home():
    # return 'Hello universe!' # return a string
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts) # render a template

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html') # render a template


