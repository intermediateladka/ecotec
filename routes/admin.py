"""
Admin routes for ECOTECH SERVICES application
Handles admin dashboard and application management
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_from_directory, current_app
from flask_login import login_required, current_user
from models import InternshipApplication
from forms import ApplicationStatusForm
from app import db
from datetime import datetime
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard with application statistics"""
    # Get application statistics
    total_applications = InternshipApplication.query.count()
    pending_applications = InternshipApplication.query.filter_by(status='pending').count()
    reviewed_applications = InternshipApplication.query.filter_by(status='reviewed').count()
    accepted_applications = InternshipApplication.query.filter_by(status='accepted').count()
    rejected_applications = InternshipApplication.query.filter_by(status='rejected').count()
    
    # Get recent applications (last 10)
    recent_applications = InternshipApplication.query.order_by(
        InternshipApplication.applied_at.desc()
    ).limit(10).all()
    
    # Get applications by internship type
    it_applications = InternshipApplication.query.filter_by(internship_type='IT Solutions').count()
    iot_applications = InternshipApplication.query.filter_by(internship_type='IoT Development').count()
    ai_applications = InternshipApplication.query.filter_by(internship_type='AI & Machine Learning').count()
    
    stats = {
        'total': total_applications,
        'pending': pending_applications,
        'reviewed': reviewed_applications,
        'accepted': accepted_applications,
        'rejected': rejected_applications,
        'it': it_applications,
        'iot': iot_applications,
        'ai': ai_applications
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_applications=recent_applications)

@admin_bp.route('/applications')
@login_required
def applications():
    """View all internship applications with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    type_filter = request.args.get('type', 'all')
    search = request.args.get('search', '')
    
    # Build query with filters
    query = InternshipApplication.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if type_filter != 'all':
        query = query.filter_by(internship_type=type_filter)
    
    if search:
        query = query.filter(
            InternshipApplication.name.contains(search) |
            InternshipApplication.email.contains(search) |
            InternshipApplication.college.contains(search)
        )
    
    # Order by application date (newest first) and paginate
    applications = query.order_by(
        InternshipApplication.applied_at.desc()
    ).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/applications.html', 
                         applications=applications,
                         status_filter=status_filter,
                         type_filter=type_filter,
                         search=search)

@admin_bp.route('/application/<int:id>')
@login_required
def view_application(id):
    """View detailed application information"""
    application = InternshipApplication.query.get_or_404(id)
    form = ApplicationStatusForm(obj=application)
    return render_template('admin/view_application.html', application=application, form=form)

@admin_bp.route('/application/<int:id>/update', methods=['POST'])
@login_required
def update_application(id):
    """Update application status and notes"""
    application = InternshipApplication.query.get_or_404(id)
    form = ApplicationStatusForm()
    
    if form.validate_on_submit():
        application.status = form.status.data
        application.notes = form.notes.data
        application.reviewed_at = datetime.utcnow()
        
        db.session.commit()
        flash(f'Application status updated to {form.status.data}', 'success')
    else:
        flash('Error updating application status', 'error')
    
    return redirect(url_for('admin.view_application', id=id))

@admin_bp.route('/download-resume/<int:id>')
@login_required
def download_resume(id):
    """Download applicant's resume"""
    application = InternshipApplication.query.get_or_404(id)
    
    if not application.resume_filename:
        flash('No resume found for this application', 'error')
        return redirect(url_for('admin.view_application', id=id))
    
    try:
        upload_dir = os.path.join(current_app.static_folder, 'uploads')
        return send_from_directory(upload_dir, application.resume_filename, as_attachment=True)
    except FileNotFoundError:
        flash('Resume file not found', 'error')
        return redirect(url_for('admin.view_application', id=id))

@admin_bp.route('/api/applications-chart')
@login_required
def applications_chart_data():
    """API endpoint for dashboard charts"""
    # Applications by month (last 6 months)
    from sqlalchemy import func, extract
    
    monthly_data = db.session.query(
        extract('month', InternshipApplication.applied_at).label('month'),
        func.count(InternshipApplication.id).label('count')
    ).group_by(extract('month', InternshipApplication.applied_at)).all()
    
    # Applications by status
    status_data = db.session.query(
        InternshipApplication.status,
        func.count(InternshipApplication.id).label('count')
    ).group_by(InternshipApplication.status).all()
    
    return jsonify({
        'monthly': [{'month': row.month, 'count': row.count} for row in monthly_data],
        'status': [{'status': row.status, 'count': row.count} for row in status_data]
    })
