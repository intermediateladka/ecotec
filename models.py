"""
Database models for ECOTECH SERVICES application
Defines User, Admin, and Internship application models
"""

from flask_login import UserMixin
from datetime import datetime
from app import db

class Admin(UserMixin, db.Model):
    """Admin user model for authentication"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class InternshipApplication(db.Model):
    """Model for internship applications"""
    __tablename__ = 'internship_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    college = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.String(20), nullable=False)
    internship_type = db.Column(db.String(50), nullable=False)  # IT, IoT, AI
    resume_filename = db.Column(db.String(255), nullable=True)
    cover_letter = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    github_profile = db.Column(db.String(255), nullable=True)
    linkedin_profile = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, accepted, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)  # Admin notes
    
    def __repr__(self):
        return f'<InternshipApplication {self.name} - {self.internship_type}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'college': self.college,
            'course': self.course,
            'year_of_study': self.year_of_study,
            'internship_type': self.internship_type,
            'resume_filename': self.resume_filename,
            'cover_letter': self.cover_letter,
            'skills': self.skills,
            'github_profile': self.github_profile,
            'linkedin_profile': self.linkedin_profile,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'notes': self.notes
        }


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    service = db.Column(db.String(50), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage {self.first_name} {self.last_name}>"