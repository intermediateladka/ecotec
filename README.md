# ECOTECH SERVICES - Flask Web Application

A modern, responsive web application built with Flask for ECOTECH SERVICES, featuring internship management, admin dashboard, and company portfolio.

## 🚀 Features

### Public Features
- **Modern Homepage** - Company introduction with services overview
- **Services Page** - Detailed IT, IoT, and AI solutions
- **Internship Portal** - Available positions and application system
- **About & Contact** - Company information and contact details
- **Responsive Design** - Bootstrap 5 with dark theme

### Admin Features
- **Secure Authentication** - Flask-Login with session management
- **Admin Dashboard** - Statistics and analytics with charts
- **Application Management** - View, filter, and update internship applications
- **Resume Downloads** - Secure file handling for applicant resumes
- **Status Tracking** - Application workflow management

### Technical Features
- **Modular Architecture** - Flask Blueprints for organized code
- **Database Integration** - SQLAlchemy with SQLite (production-ready)
- **File Upload System** - Secure resume upload with validation
- **Form Validation** - WTForms with client-side validation
- **Error Handling** - Custom 404/500 pages with logging
- **Security** - CSRF protection, secure file uploads, input validation

## 📋 Requirements

- Python 3.8+
- Flask 2.3+
- SQLAlchemy 2.0+
- Bootstrap 5.3+

## 🛠️ Installation & Setup

### 1. Clone or Download
\`\`\`bash
# If using git
git clone <repository-url>
cd ecotech-flask-app

# Or extract the downloaded ZIP file
unzip ecotech-flask-app.zip
cd ecotech-flask-app
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install flask flask-sqlalchemy flask-login flask-migrate flask-wtf wtforms email-validator werkzeug
\`\`\`

### 4. Environment Setup
Create a `.env` file in the root directory:
\`\`\`env
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///ecotech.db
FLASK_ENV=development
FLASK_DEBUG=True
\`\`\`

### 5. Initialize Database
\`\`\`bash
# Initialize the database
python app.py
\`\`\`

### 6. Run Application
\`\`\`bash
python app.py
\`\`\`

The application will be available at `http://localhost:5000`

## 🔐 Default Admin Credentials

- **Username:** `admin`
- **Password:** `admin123`

**⚠️ Important:** Change these credentials in production!

## 📁 Project Structure

\`\`\`
ecotech-flask-app/
├── app.py                 # Main application file
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── routes/                # Blueprint routes
│   ├── __init__.py
│   ├── main.py           # Public routes
│   ├── auth.py           # Authentication routes
│   └── admin.py          # Admin routes
├── templates/             # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── services.html     # Services page
│   ├── internships.html  # Internships page
│   ├── apply.html        # Application form
│   ├── about.html        # About page
│   ├── contact.html      # Contact page
│   ├── auth/             # Authentication templates
│   │   └── login.html
│   ├── admin/            # Admin templates
│   │   ├── dashboard.html
│   │   ├── applications.html
│   │   └── view_application.html
│   └── errors/           # Error pages
│       ├── 404.html
│       └── 500.html
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   └── uploads/          # Resume uploads (created automatically)
├── requirements.txt      # Python dependencies
└── README.md            # This file
\`\`\`

## 🎨 Customization

### Branding
- Update company name in `templates/base.html`
- Modify colors in `static/css/style.css`
- Replace logo/favicon in `static/` directory

### Services
- Edit service content in `routes/main.py` (services route)
- Update service descriptions in `templates/services.html`

### Internship Positions
- Modify available positions in `routes/main.py` (internships route)
- Update internship types in `forms.py` (InternshipApplicationForm)

## 🔧 Configuration

### Database Configuration
\`\`\`python
# For PostgreSQL (production)
DATABASE_URL = 'postgresql://user:password@localhost/ecotech'

# For MySQL
DATABASE_URL = 'mysql://user:password@localhost/ecotech'

# For SQLite (default)
DATABASE_URL = 'sqlite:///ecotech.db'
\`\`\`

### Email Configuration (Optional)
Add to your environment variables:
\`\`\`env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
\`\`\`

### File Upload Configuration
\`\`\`python
# Maximum file size (16MB default)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
\`\`\`

## 🚀 Production Deployment

### 1. Environment Variables
Set production environment variables:
\`\`\`env
SECRET_KEY=your-strong-secret-key
DATABASE_URL=your-production-database-url
FLASK_ENV=production
FLASK_DEBUG=False
\`\`\`

### 2. Database Migration
\`\`\`bash
# Initialize migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
\`\`\`

### 3. Web Server (Gunicorn)
\`\`\`bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
\`\`\`

### 4. Nginx Configuration (Optional)
\`\`\`nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/your/app/static;
    }
}
\`\`\`

## 📊 Database Schema

### Admin Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`
- `is_active`

### InternshipApplication Table
- `id` (Primary Key)
- `name`
- `email`
- `phone`
- `college`
- `course`
- `year_of_study`
- `internship_type`
- `resume_filename`
- `cover_letter`
- `skills`
- `github_profile`
- `linkedin_profile`
- `status` (pending/reviewed/accepted/rejected)
- `applied_at`
- `reviewed_at`
- `notes` (Admin notes)

## 🔒 Security Features

- **CSRF Protection** - All forms protected against CSRF attacks
- **File Upload Security** - Type validation and secure filename handling
- **Input Validation** - Server-side validation for all user inputs
- **Session Management** - Secure session handling with Flask-Login
- **Password Hashing** - Werkzeug password hashing
- **SQL Injection Prevention** - SQLAlchemy ORM protection

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   \`\`\`bash
   # Delete existing database and recreate
   rm ecotech.db
   python app.py
   \`\`\`

2. **File Upload Issues**
   \`\`\`bash
   # Check upload directory permissions
   mkdir -p static/uploads
   chmod 755 static/uploads
   \`\`\`

3. **Template Not Found**
   - Ensure templates are in the correct directory structure
   - Check template names match route render_template calls

4. **Static Files Not Loading**
   - Verify static files are in `static/` directory
   - Check Flask static_folder configuration

### Debug Mode
Enable debug mode for development:
\`\`\`python
app.run(debug=True)
\`\`\`

## 📈 Performance Optimization

### Database Optimization
- Add database indexes for frequently queried fields
- Use database connection pooling for production
- Implement query optimization for large datasets

### Caching
\`\`\`python
# Add Flask-Caching for better performance
from flask_caching import Cache
cache = Cache(app)
\`\`\`

### Static File Optimization
- Use CDN for Bootstrap and Font Awesome
- Minify CSS and JavaScript files
- Implement browser caching headers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Email: support@ecotechservices.com
- Documentation: [Project Wiki]
- Issues: [GitHub Issues]

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added admin dashboard and analytics
- **v1.2.0** - Enhanced security and file upload features

---

**ECOTECH SERVICES** - Innovative Technology Solutions for a Sustainable Future
#   e c o t e c h  
 