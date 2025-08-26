"""
WTForms for ECOTECH SERVICES application
Defines forms for login, internship applications, and admin operations
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    """Admin login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class InternshipApplicationForm(FlaskForm):
    """Internship application form"""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    college = StringField('College/University', validators=[DataRequired(), Length(min=2, max=200)])
    course = StringField('Course/Degree', validators=[DataRequired(), Length(min=2, max=100)])
    year_of_study = SelectField('Year of Study', 
                               choices=[('1st Year', '1st Year'), 
                                       ('2nd Year', '2nd Year'),
                                       ('3rd Year', '3rd Year'),
                                       ('4th Year', '4th Year'),
                                       ('Final Year', 'Final Year'),
                                       ('Graduate', 'Graduate')],
                               validators=[DataRequired()])
    
    internship_type = SelectField('Internship Domain',
                                 choices=[('IT Solutions', 'IT Solutions'),
                                         ('IoT Development', 'IoT Development'),
                                         ('AI & Machine Learning', 'AI & Machine Learning'),
                                         ('Full Stack Development', 'Full Stack Development'),
                                         ('Data Science', 'Data Science')],
                                 validators=[DataRequired()])
    
    resume = FileField('Resume (PDF only)', 
                      validators=[FileRequired(), 
                                FileAllowed(['pdf'], 'Only PDF files are allowed!')])
    
    cover_letter = TextAreaField('Cover Letter', 
                                validators=[Optional(), Length(max=1000)],
                                render_kw={"rows": 5, "placeholder": "Tell us why you're interested in this internship..."})
    
    skills = TextAreaField('Technical Skills', 
                          validators=[Optional(), Length(max=500)],
                          render_kw={"rows": 3, "placeholder": "List your technical skills (e.g., Python, JavaScript, React, etc.)"})
    
    github_profile = StringField('GitHub Profile (Optional)', 
                                validators=[Optional(), URL()])
    
    linkedin_profile = StringField('LinkedIn Profile (Optional)', 
                                  validators=[Optional(), URL()])
    
    submit = SubmitField('Submit Application')

class ApplicationStatusForm(FlaskForm):
    """Form for updating application status"""
    status = SelectField('Status',
                        choices=[('pending', 'Pending'),
                                ('reviewed', 'Reviewed'),
                                ('accepted', 'Accepted'),
                                ('rejected', 'Rejected')],
                        validators=[DataRequired()])
    
    notes = TextAreaField('Admin Notes', 
                         validators=[Optional(), Length(max=1000)],
                         render_kw={"rows": 4})
    
    submit = SubmitField('Update Status')
