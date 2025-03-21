from app import db
from datetime import datetime

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))
    is_online = db.Column(db.Boolean, default=False)
    meeting_link = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='sessions')
    participants = db.relationship('SessionParticipant', back_populates='session')

class SessionParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('study_session.id'))
    status = db.Column(db.String(20))  # confirmed, pending, declined
    
    # Relationships
    session = db.relationship('StudySession', back_populates='participants')
