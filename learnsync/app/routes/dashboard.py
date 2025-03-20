from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.group import Group, GroupMember
from app.models.schedule import StudySession
from app.models.material import Material
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def index():
    # Get user's groups
    user_groups = Group.query.join(GroupMember).filter(GroupMember.user_id == current_user.id).all()
    
    # Get upcoming sessions
    today = datetime.utcnow()
    upcoming_sessions = StudySession.query.join(GroupMember, StudySession.group_id == GroupMember.group_id)\
        .filter(GroupMember.user_id == current_user.id, StudySession.start_time >= today)\
        .order_by(StudySession.start_time).limit(3).all()
    
    # Get recent materials
    recent_materials = Material.query.join(GroupMember, Material.group_id == GroupMember.group_id)\
        .filter(GroupMember.user_id == current_user.id)\
        .order_by(Material.uploaded_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          user_groups=user_groups,
                          upcoming_sessions=upcoming_sessions,
                          recent_materials=recent_materials)
