import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from app import create_app, db
from app.models.user import User
from app.models.group import Group, GroupMember
from app.models.material import Material, AISummary
from app.models.chat import Message
from app.models.schedule import StudySession, SessionParticipant

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Group': Group,
        'GroupMember': GroupMember,
        'Material': Material,
        'AISummary': AISummary,
        'Message': Message,
        'StudySession': StudySession,
        'SessionParticipant': SessionParticipant
    }

if __name__ == '__main__':
    app.run(debug=True)
# Compare this snippet from learnsync/app/routes/auth.py:
# from flask import Blueprint, render_template, redirect, url_for, flash, request
# from flask_login import login_user, logout_user, current_user, login_required
# from app.models.user import User
# from app import db
# from werkzeug.urls import url_parse
#
# auth = Blueprint('auth', __name__)
#
# @auth.route('/login', methods=['GET', 'POST'])
