# WebDoctor (EHR) System

## 📋 Project Overview

The **WebDoctor** is a comprehensive web-based healthcare management platform designed to streamline patient care, medical record management, and telemedicine services. This system bridges the gap between patients and healthcare providers through a secure, scalable, and user-friendly digital platform.

The EHR system facilitates seamless communication between patients and doctors, enabling efficient appointment scheduling, medical record management, prescription tracking, and real-time video consultations. Built with modern web technologies, it ensures data security, regulatory compliance, and enhanced healthcare delivery.

## 💻 Programming Languages

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## 🛠️ Tech Stack

**Backend:**
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37B24D?style=for-the-badge&logo=celery&logoColor=white)

**Frontend & Integration:**
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![100ms](https://img.shields.io/badge/100ms-Video_API-FF6B6B?style=for-the-badge&logo=webrtc&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-SMTP-D14836?style=for-the-badge&logo=gmail&logoColor=white)

**Development Tools:**
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

## �🚀 Key Features

### Patient Management
- **Patient Registration & Profiles**: Comprehensive patient onboarding with detailed medical history
- **Medical Records**: Secure storage and management of patient health records
- **Vital Signs Tracking**: Monitor body temperature, heart rate, respiratory rate, blood pressure
- **Report Management**: Upload, view, and manage medical reports (Blood tests, X-rays, MRI, CT scans, etc.)
- **Chronic Conditions Tracking**: JSON-based storage of patient's chronic medical conditions
- **Emergency Contact Management**: Quick access to emergency contact information

### Doctor Management
- **Doctor Profiles**: Detailed professional profiles with specializations and credentials
- **Multi-Specialty Support**: 12+ medical specializations including Cardiology, Neurology, Oncology, etc.
- **License Verification**: Secure storage of medical license numbers and credentials
- **Patient Lists**: Organized patient management with connection tracking
- **Consultation Fee Management**: Flexible pricing structure for different services

### Appointment System
- **Smart Scheduling**: Intelligent appointment booking with conflict resolution
- **Status Management**: Track appointments (scheduled, completed, cancelled)
- **Automated Notifications**: Email notifications for appointment reminders and updates
- **Background Task Processing**: Celery-based asynchronous task management

### Telemedicine Integration
- **100ms Integration**: Professional-grade video conferencing for online consultations
- **Role-based Meeting Access**: Separate meeting links for doctors and patients
- **Room Management**: Automatic creation and management of consultation rooms
- **Session Recording**: Optional consultation recording capabilities

### User Authentication & Security
- **Custom User Model**: Email-based authentication system
- **Role-based Access Control**: Separate interfaces for patients, doctors, and administrators
- **Secure Password Management**: Django's built-in password validation
- **Session Management**: Secure user session handling

### Communication System
- **Email Integration**: SMTP-based email system for notifications
- **Appointment Reminders**: Automated email reminders for upcoming appointments
- **Status Updates**: Real-time updates on appointment and request status

## 🛠️ Technology Stack

### Backend Framework
- **Django 5.1**: High-level Python web framework
- **Python 3.12**: Core programming language
- **Django REST Framework**: API development (implied from structure)

### Database
- **PostgreSQL**: Primary relational database
- **Redis**: Caching and message broker for Celery

### Asynchronous Processing
- **Celery**: Distributed task queue for background processing
- **Celery Beat**: Periodic task scheduler
- **Redis Broker**: Message broker for task distribution

### Frontend Technologies
- **HTML5 Templates**: Server-side rendered templates
- **CSS3**: Styling and responsive design
- **JavaScript**: Client-side interactivity
- **Bootstrap** (implied): Responsive UI components

### Third-Party Integrations
- **100ms Video API**: Professional video conferencing solution
- **SMTP Gmail Integration**: Email notification system
- **UUID**: Unique identifier generation for records

### Development Tools
- **python-dotenv**: Environment variable management
- **psycopg2-binary**: PostgreSQL adapter for Python
- **PyJWT**: JSON Web Token implementation
- **requests**: HTTP library for API integrations

### Security & Authentication
- **Django Authentication**: Built-in user authentication system
- **Custom User Manager**: Extended user management capabilities
- **CSRF Protection**: Cross-site request forgery protection
- **Session Security**: Secure session management

## 🏗️ System Architecture

### Model-View-Template (MVT) Architecture
The application follows Django's MVT pattern with clear separation of concerns:

```
EHR System Architecture
├── Models (Data Layer)
│   ├── CustomUser (Authentication)
│   ├── DoctorProfile (Doctor Management)
│   ├── PatientRecord (Patient Management)
│   ├── Appointment (Scheduling)
│   ├── Report (Medical Records)
│   └── Medication (Prescription Management)
├── Views (Business Logic)
│   ├── Authentication Views
│   ├── Patient Management Views
│   ├── Doctor Management Views
│   └── Appointment Management Views
└── Templates (Presentation Layer)
    ├── Authentication Templates
    ├── Patient Dashboard Templates
    └── Doctor Dashboard Templates
```

### Database Schema Design

#### Core Entities
1. **CustomUser**: Central user management with email-based authentication
2. **DoctorProfile**: Extended doctor information with specializations
3. **PatientRecord**: Comprehensive patient health records
4. **Appointment**: Appointment scheduling with video integration
5. **PatientsList**: Many-to-many relationship between patients and doctors
6. **Report**: Medical report management with file storage

#### Relationship Structure
- **One-to-One**: User ↔ DoctorProfile, User ↔ PatientRecord
- **Many-to-Many**: Patients ↔ Doctors (through PatientsList)
- **One-to-Many**: Doctor → Appointments, Patient → Reports

### Asynchronous Task Architecture
```
Celery Task System
├── Task Queue (Redis)
├── Background Workers
│   ├── Appointment Management
│   ├── Email Notifications
│   └── Room Management
└── Scheduled Tasks (Celery Beat)
    ├── Appointment Reminders
    └── System Maintenance
```

### Video Integration Architecture
```
100ms Integration
├── Room Creation
├── Role-based Access (Doctor/Patient)
├── Meeting Link Generation
└── Automatic Room Cleanup
```

## 📁 Project Structure

```
EHR/
├── EHR/                    # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   ├── celery.py          # Celery configuration
│   └── wsgi.py            # WSGI application
├── user/                   # User management app
│   ├── models.py          # Custom user model
│   ├── views.py           # Authentication views
│   ├── manager.py         # Custom user manager
│   └── emailAuth.py       # Email authentication
├── doctor/                 # Doctor management app
│   ├── models.py          # Doctor-related models
│   ├── views.py           # Doctor dashboard views
│   ├── forms.py           # Doctor forms
│   └── tasks.py           # Doctor-related Celery tasks
├── patients/               # Patient management app
│   ├── models.py          # Patient-related models
│   ├── views.py           # Patient dashboard views
│   ├── forms.py           # Patient forms
│   └── registrationForm.py # Patient registration
├── templates/              # HTML templates
│   ├── auth/              # Authentication templates
│   ├── doc/               # Doctor templates
│   └── pat/               # Patient templates
├── patient_reports/        # File storage for reports
├── hms.py                 # 100ms API integration
├── manage.py              # Django management script
└── requirements.txt       # Project dependencies
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.12+
- PostgreSQL 12+
- Redis Server
- Git

### Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
HMS_ACCESS_KEY=your_100ms_access_key
HMS_SECRET=your_100ms_secret
HMS_TOKEN=your_100ms_token
HMS_TEMPLATE_ID=your_100ms_template_id
```

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd EHR
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Redis Server**
   ```bash
   redis-server
   ```

7. **Start Celery Worker** (in separate terminal)
   ```bash
   celery -A EHR worker --loglevel=info
   ```

8. **Start Celery Beat** (in separate terminal)
   ```bash
   celery -A EHR beat --loglevel=info
   ```

9. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## 🔒 Security Features

- **Email-based Authentication**: Secure user identification
- **Role-based Access Control**: Separate permissions for patients and doctors
- **CSRF Protection**: Built-in Django security
- **Password Validation**: Strong password requirements
- **Session Security**: Secure session management
- **Database Security**: PostgreSQL with encrypted connections
- **File Upload Security**: Secure medical report storage

## 📊 Performance Optimizations

- **Asynchronous Processing**: Celery for background tasks
- **Database Indexing**: Optimized database queries
- **File Management**: Efficient medical report storage

## 🎯 Use Cases

1. **Patient Onboarding**: Complete registration with medical history
2. **Doctor-Patient Connection**: Secure connection establishment
3. **Appointment Scheduling**: Intelligent booking system
4. **Telemedicine Consultations**: Video-based medical consultations
5. **Medical Record Management**: Comprehensive health record tracking
6. **Report Analysis**: Medical report upload and management
7. **Prescription Management**: Digital prescription tracking

## 🚀 Future Enhancements

- **AI Integration**: Medical diagnosis assistance
- **Blockchain**: Secure medical record storage
- **IoT Integration**: Wearable device data integration
- **Advanced Analytics**: Health trend analysis
- **Multi-language Support**: Internationalization
- **FHIR Compliance**: Healthcare interoperability standards

**Built with ❤️ using Django, PostgreSQL, and modern web technologies for better healthcare delivery.**
