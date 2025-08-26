"""
Main routes for ECOTECH SERVICES application
Handles homepage, services, internships, and public pages
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from forms import InternshipApplicationForm
from models import InternshipApplication
from extensions import db  # Import from extensions instead of app
import os
from datetime import datetime

from models import ContactMessage


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage with company introduction"""
    return render_template('index.html')

@main_bp.route('/services')
def services():
    """Services page displaying IT, IoT, and AI solutions"""
    services_data = {
        'it_solutions': [
            {
                'title': 'Web Development',
                'description': 'Custom web applications using modern frameworks like Flask, Django, React, and Vue.js',
                'icon': 'fas fa-globe'
            },
            {
                'title': 'Mobile App Development',
                'description': 'Native and cross-platform mobile applications for iOS and Android',
                'icon': 'fas fa-mobile-alt'
            },
            {
                'title': 'Cloud Solutions',
                'description': 'AWS, Azure, and Google Cloud infrastructure setup and management',
                'icon': 'fas fa-cloud'
            },
            {
                'title': 'Database Management',
                'description': 'Database design, optimization, and management for scalable applications',
                'icon': 'fas fa-database'
            }
        ],
        'iot_solutions': [
            {
                'title': 'Smart Home Systems',
                'description': 'Automated home solutions with sensor integration and mobile control',
                'icon': 'fas fa-home'
            },
            {
                'title': 'Industrial IoT',
                'description': 'Manufacturing and industrial automation with real-time monitoring',
                'icon': 'fas fa-industry'
            },
            {
                'title': 'Environmental Monitoring',
                'description': 'Air quality, weather, and environmental data collection systems',
                'icon': 'fas fa-leaf'
            },
            {
                'title': 'Asset Tracking',
                'description': 'GPS and RFID-based tracking solutions for inventory and logistics',
                'icon': 'fas fa-map-marker-alt'
            }
        ],
        'ai_solutions': [
            {
                'title': 'Machine Learning Models',
                'description': 'Custom ML models for prediction, classification, and recommendation systems',
                'icon': 'fas fa-brain'
            },
            {
                'title': 'Computer Vision',
                'description': 'Image recognition, object detection, and video analysis solutions',
                'icon': 'fas fa-eye'
            },
            {
                'title': 'Natural Language Processing',
                'description': 'Text analysis, chatbots, and language understanding applications',
                'icon': 'fas fa-comments'
            },
            {
                'title': 'Data Analytics',
                'description': 'Business intelligence and data visualization for informed decision making',
                'icon': 'fas fa-chart-line'
            }
        ]
    }
    return render_template('services.html', services=services_data)

@main_bp.route('/internships')
def internships():
    """Internships page with available positions"""
    internship_positions = [
        {
            'title': 'Full Stack Development Intern',
            'domain': 'IT Solutions',
            'duration': '3-6 months',
            'description': 'Work on web applications using Python Flask, React, and modern databases',
            'requirements': ['Python/JavaScript knowledge', 'Basic web development skills', 'Git version control']
        },
        {
            'title': 'IoT Development Intern',
            'domain': 'IoT Development',
            'duration': '4-6 months',
            'description': 'Develop IoT solutions using Arduino, Raspberry Pi, and cloud platforms',
            'requirements': ['Electronics basics', 'Programming skills (Python/C++)', 'Interest in hardware']
        },
        {
            'title': 'AI/ML Research Intern',
            'domain': 'AI & Machine Learning',
            'duration': '3-6 months',
            'description': 'Work on machine learning projects and AI model development',
            'requirements': ['Python programming', 'Mathematics/Statistics background', 'ML frameworks knowledge']
        },
        {
            'title': 'Data Science Intern',
            'domain': 'Data Science',
            'duration': '3-4 months',
            'description': 'Analyze data, create visualizations, and build predictive models',
            'requirements': ['Python/R programming', 'Statistics knowledge', 'Data visualization skills']
        }
    ]
    return render_template('internships.html', positions=internship_positions)

@main_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    """Internship application form"""
    form = InternshipApplicationForm()
    
    if form.validate_on_submit():
        try:
            # Handle file upload
            resume_filename = None
            if form.resume.data:
                resume_file = form.resume.data
                filename = secure_filename(resume_file.filename)
                # Add timestamp to avoid filename conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                resume_filename = timestamp + filename
                
                upload_path = os.path.join(current_app.static_folder, 'uploads', resume_filename)
                resume_file.save(upload_path)
            
            # Create new application
            application = InternshipApplication(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                college=form.college.data,
                course=form.course.data,
                year_of_study=form.year_of_study.data,
                internship_type=form.internship_type.data,
                resume_filename=resume_filename,
                cover_letter=form.cover_letter.data,
                skills=form.skills.data,
                github_profile=form.github_profile.data,
                linkedin_profile=form.linkedin_profile.data
            )
            
            db.session.add(application)
            db.session.commit()
            
            flash('Your application has been submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('main.apply'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your application. Please try again.', 'error')
            current_app.logger.error(f'Application submission error: {str(e)}')
    
    return render_template('apply.html', form=form)

@main_bp.route('/about')
def about():
    """About page with company information"""
    return render_template('about.html')

# @main_bp.route('/contact', methods=['GET', 'POST'])
# def contact():
#     """Contact page with company details"""
#     if request.method == 'POST':
#         # Process form data here
#         flash('Your message has been sent successfully!', 'success')
#         return redirect(url_for('main.contact'))
#     return render_template('contact.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Form se data uthao
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')

        # Data database me save karo
        new_message = ContactMessage(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            service=service,
            message=message
        )
        db.session.add(new_message)
        db.session.commit()

        flash("Your message has been sent successfully! ✅", "success")
        return redirect(url_for('main.contact'))  # Wapas contact page par

    return render_template("contact.html")
