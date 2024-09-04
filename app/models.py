from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cv_file = db.Column(db.String(120)) 
    profile_photo = db.Column(db.String(120)) 

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary = db.Column(db.String(50), nullable=False)  
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')

    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))

    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='unique_user_job_application'),)
