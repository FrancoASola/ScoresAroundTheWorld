from flask import Blueprint, render_template

mod = Blueprint('site', __name__)
current_matches = {}

@mod.route('/')
def live():
    '''Main Page'''
    return render_template('index.html')
