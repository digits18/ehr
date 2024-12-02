from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user, logout_user

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


class Admin(db.Model, UserMixin):
    tablename = 'admin'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username


class Patient(db.Model):
    tablename = 'patient'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    patient_num = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, unique=False, nullable=False)
    last_name = db.Column(db.String, unique=False, nullable=False)
    dob = db.Column(db.String, unique=False, nullable=True)
    age = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String, unique=False, nullable=True)
    address = db.Column(db.String, unique=False, nullable=False)
    mobile = db.Column(db.String, unique=False, nullable=False)
    marital_status = db.Column(db.String, unique=False, nullable=True)
    nhis = db.Column(db.String, unique=False, nullable=True)
    reg_date = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, patient_num, first_name, last_name, dob, age, gender, address, mobile, marital_status, nhis,
                 reg_date):
        self.patient_num = patient_num
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.age = age
        self.gender = gender
        self.address = address
        self.mobile = mobile
        self.marital_status = marital_status
        self.nhis = nhis
        self.reg_date = reg_date

    def __repr__(self):
        return self.patient_num


class Nurse(db.Model):
    tablename = 'nurse'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String, unique=False, nullable=False)
    last_name = db.Column(db.String, unique=False, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Name of the image file
    content_type = db.Column(db.String(50), nullable=False)  # MIME type (e.g., 'image/png', 'image/jpeg')
    data = db.Column(db.Text, nullable=False)  # Base64-encoded image data
    status = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, first_name, last_name, mobile, email, username, password, filename, content_type, data, status):
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.email = email
        self.username = username
        self.password = password
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.status = status

    def __repr__(self):
        return self.username


class Doctor(db.Model):
    tablename = 'doctor'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String, unique=False, nullable=False)
    last_name = db.Column(db.String, unique=False, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Name of the image file
    content_type = db.Column(db.String(50), nullable=False)  # MIME type (e.g., 'image/png', 'image/jpeg')
    data = db.Column(db.Text, nullable=False)  # Base64-encoded image data
    status = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, first_name, last_name, mobile, email, username, password, filename, content_type, data, status):
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.email = email
        self.username = username
        self.password = password
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.status = status

    def __repr__(self):
        return self.username





