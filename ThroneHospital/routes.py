from flask import Blueprint, Flask, jsonify
from flask import render_template, request, flash, jsonify, redirect, url_for
from .models import login_manager
from .models import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Admin, Patient, Nurse, Doctor
from .models import current_user, logout_user, login_required, login_user
from settings import *

bp = Blueprint('bp', __name__)

app = Flask(__name__)

# Define the upload folder path
static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')  # Get the absolute path to 'static'
upload_folder = os.path.join(static_folder, 'AppUploads')  # Create 'AppUploads' inside 'static'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(upload_folder, exist_ok=True)

app.config['UPLOAD'] = upload_folder


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def loader_user(username):
    if username is not None:
        return Admin.query.get(username)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view this page.", "error")
    return redirect(url_for("bp.index"))


@bp.route('/logout_admin', methods=['GET', 'POST'])
def logout_admin():
    logout_user()
    return redirect(url_for('bp.admin_login'))


def verify_patient_num(num):
    all_patient_records = Patient.query.all()
    patient_num_list = []

    for item in all_patient_records:
        check_patient_num = item.patient_num
        patient_num_list.append(check_patient_num)

    if num in patient_num_list:
        return "Patient record already exist"


def assign_patient_id(card_numbers_list, patient_num_list):
    # Loop through card_numbers_list
    for card_number in card_numbers_list:
        if card_number not in patient_num_list:
            # Assign this ID to the patient
            return card_number
    # If no available ID is found, return None or raise an error
    return None


def total_number_of_patient():
    # ======== Length of Patients
    all_patient_records = Patient.query.all()
    all_patients = len(all_patient_records)
    return all_patients


def total_number_of_nurse():
    # ======== Length of Patients
    all_nurses_records = Nurse.query.all()
    all_nurses = len(all_nurses_records)
    return all_nurses


def total_number_of_doctor():
    # ======== Length of Patients
    all_doctors_records = Doctor.query.all()
    all_doctors = len(all_doctors_records)
    return all_doctors


def patients_info():
    # ====== Lists Of Patients
    patient_list = []
    patient_records = Patient.query.all()
    for item in patient_records:
        dic = {'patient_num': item.patient_num,
               'first_name': item.first_name,
               'last_name': item.last_name,
               'dob': item.dob,
               'age': item.age,
               'gender': item.gender,
               'address': item.address,
               'mobile': item.mobile,
               'marital_status': item.marital_status,
               'nhis': item.nhis,
               'reg_date': item.reg_date
               }
        patient_list.append(dic)
    return patient_list


def nurse_info():
    # ====== Lists Of Nurses
    nurse_list = []
    nurse_records = Nurse.query.all()
    for item in nurse_records:
        dic = {
            'first_name': item.first_name,
            'last_name': item.last_name,
            'mobile': item.mobile,
            'email': item.email,
            'username': item.username,
            'filename': item.profile_pic,
            'status': item.status
        }
        nurse_list.append(dic)
    return nurse_list


def doctor_info():
    # ====== Lists Of Nurses
    doctor_list = []
    doctor_records = Doctor.query.all()
    for item in doctor_records:
        dic = {
            'first_name': item.first_name,
            'last_name': item.last_name,
            'mobile': item.mobile,
            'email': item.email,
            'username': item.username,
            'image_file': item.profile_pic,
            'status': item.status
        }
        doctor_list.append(dic)
    return doctor_list


def verify_patient_name(first_name, last_name):
    all_patient_records = Patient.query.all()
    first_name_list = []

    for item in all_patient_records:
        check_first_name = item.first_name
        first_name_list.append(check_first_name)

    last_name_list = []

    for item in all_patient_records:
        check_last_name = item.last_name
        last_name_list.append(check_last_name)

    if first_name in first_name_list and last_name in last_name_list:
        return "Patient record already exist"


def verify_nurse_username(username):
    all_nurses_records = Nurse.query.all()
    username_list = []

    for item in all_nurses_records:
        check_username = item.username
        username_list.append(check_username)

    if username in username_list:
        return "Username already exist"


def verify_doctor_username(username):
    all_doctors_records = Doctor.query.all()
    username_list = []

    for item in all_doctors_records:
        check_username = item.username
        username_list.append(check_username)

    if username in username_list:
        return "Username already exist"


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', APP_NAME=APP_NAME)


@bp.route('/admin_login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get("password")
        current_user = Admin.query.filter_by(username=username).first()
        if current_user and current_user.password == password:
            login_user(current_user, remember=True)
            return redirect(url_for('bp.admin_dashboard', user=current_user.username))
        else:
            flash("Incorrect Login Credentials", "danger")

    return render_template('admin_login.html', APP_NAME=APP_NAME)


@bp.route('/nurse_login/', methods=['GET', 'POST'])
def nurse_login():
    return render_template('nurse_login.html', APP_NAME=APP_NAME)


@bp.route('/doctor_login/', methods=['GET', 'POST'])
def doctor_login():
    return render_template('doctor_login.html', APP_NAME=APP_NAME)


@bp.route('/lab_login/', methods=['GET', 'POST'])
def lab_login():
    return render_template('lab_login.html', APP_NAME=APP_NAME)


@bp.route('/pharmacy_login/', methods=['GET', 'POST'])
def pharmacy_login():
    return render_template('pharmacy_login.html', APP_NAME=APP_NAME)


@bp.route('/admin_dashboard/', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    all_patients = total_number_of_patient()
    patient_list = patients_info()

    all_nurses = total_number_of_nurse()
    nurse_list = nurse_info()

    all_doctors = total_number_of_doctor()
    doctor_list = doctor_info()

    # ================= NURSES
    # Get all image names from nurse_list
    all_image_name = [item['filename'] for item in nurse_list]

    # Generate the full image paths and URLs
    images = []  # To store the URLs of all images
    for image_name in all_image_name:
        # Construct the full file path
        img_path = os.path.join(app.config['UPLOAD'], image_name)

        # Extract just the filename
        filename = os.path.basename(img_path)

        # Generate the URL for the image
        img_url = url_for('static', filename=f'AppUploads/{filename}')

        # Append the URL to the images list
        images.append(img_url)


    # =============== DOCTORS

    # Get all image names from doctor_list
    all_image = [pcs['image_file'] for pcs in doctor_list]

    # Generate the full image paths and URLs
    pictures = []  # To store the URLs of all images
    for img_name in all_image:
        # Construct the full file path
        image_path = os.path.join(app.config['UPLOAD'], img_name)

        # Extract just the filename
        fileName = os.path.basename(image_path)

        # Generate the URL for the image
        image_url = url_for('static', filename=f'AppUploads/{fileName}')

        # Append the URL to the images list
        pictures.append(image_url)

    return render_template('admin_dashboard.html', APP_NAME=APP_NAME, all_patients=all_patients,
                           patient_list=patient_list, all_nurses=all_nurses, nurse_list=nurse_list, images=images,
                           all_doctors=all_doctors, doctor_list=doctor_list, pictures=pictures, zip=zip)


@bp.route('/add_patient/', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        num = request.form.get('patient_num')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d')
        formatted_dob = dob.strftime('%d-%m-%Y')
        age = request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('address')
        mobile = request.form.get('mobile')
        marital_status = request.form.get('marital_status')
        nhis = request.form.get('nhis')
        reg_date = datetime.strptime(request.form.get('reg_date'), '%Y-%m-%d')
        formatted_reg_date = reg_date.strftime('%d-%m-%Y')

        res = verify_patient_num(num)
        resp = verify_patient_name(first_name, last_name)

        if res:
            flash(f'{res}', 'error')
        elif resp:
            flash(f'{resp}', 'error')
        else:
            new_patient = Patient(num, first_name, last_name, formatted_dob, age, gender, address, mobile,
                                  marital_status,
                                  nhis, formatted_reg_date)
            db.session.add(new_patient)
            db.session.commit()
            flash('Patient record successfully entered', 'success')
            return redirect(url_for('bp.admin_dashboard', APP_NAME=APP_NAME))

    # Create an empty list of patient's number
    card_numbers_list = []
    # Generate the 5-digit number serially starting from 0 for 50000 patients
    card_numbers = [f"{i:05}" for i in range(1, 50000 + 1)]
    for card_number in card_numbers:
        card_numbers_list.append(card_number)

    # ========== Checking Patient Table and populating a list to check for existing patient number
    all_patient_records = Patient.query.all()
    patient_num_list = []

    for item in all_patient_records:
        check_patient_num = item.patient_num
        patient_num_list.append(check_patient_num)

    # Assign a new ID to the patient
    new_patient_id = assign_patient_id(card_numbers_list, patient_num_list)
    id_no = new_patient_id

    return render_template('add_patient.html', APP_NAME=APP_NAME, patient_id=id_no)


@bp.route('/add_nurse/', methods=['GET', 'POST'])
@login_required
def add_nurse():
    prefix_list = ['070', '080', '081', '090', '091']
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        image = request.files.get('profile_pic')

        response = verify_nurse_username(username)
        # Check if the password contains at least 2 numbers
        password_has_number = sum(1 for char in password if char.isdigit())

        prefix = mobile[0:3]
        if len(first_name) < 3:
            flash('Pls enter your first name', 'error')
        elif len(username) < 6:
            flash('Username too short', 'error')
        elif response:
            flash(f'{response}', 'error')
        elif prefix not in prefix_list:
            flash('Invalid mobile number prefix', 'error')
        elif len(mobile) < 11:
            flash('Invalid mobile number', 'error')
        elif len(password) < 8:
            flash('Weak password ', 'error')
        elif password_has_number < 2:
            flash('Password must contain at least 2 numbers.', 'error')
        else:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD'], filename))

                nurse_account = Nurse(first_name, last_name, mobile, email, username, password, filename, 'ACTIVE')
                db.session.add(nurse_account)
                db.session.commit()
                flash('Nurse Account successfully created', 'success')
                return redirect(url_for('bp.admin_dashboard', APP_NAME=APP_NAME))
            else:
                flash('Invalid file format!', 'error')
    return render_template('add_nurse.html', APP_NAME=APP_NAME)


@bp.route('/add_doctor/', methods=['GET', 'POST'])
@login_required
def add_doctor():
    prefix_list = ['070', '080', '081', '090', '091']
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        image = request.files.get('profile_pic')

        response = verify_doctor_username(username)
        # Check if the password contains at least 2 numbers
        password_has_number = sum(1 for char in password if char.isdigit())

        prefix = mobile[0:3]
        if len(first_name) < 3:
            flash('Pls enter your first name', 'error')
        elif len(username) < 6:
            flash('Username too short', 'error')
        elif response:
            flash(f'{response}', 'error')
        elif prefix not in prefix_list:
            flash('Invalid mobile number prefix', 'error')
        elif len(mobile) < 11:
            flash('Invalid mobile number', 'error')
        elif len(password) < 8:
            flash('Weak password ', 'error')
        elif password_has_number < 2:
            flash('Password must contain at least 2 numbers.', 'error')
        else:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD'], filename))

                doctor_account = Doctor(first_name, last_name, mobile, email, username, password, filename, 'ACTIVE')
                db.session.add(doctor_account)
                db.session.commit()
                flash('Doctor Account successfully created', 'success')
                return redirect(url_for('bp.admin_dashboard', APP_NAME=APP_NAME))
            else:
                flash('Invalid file format!', 'error')
    return render_template('add_doctor.html', APP_NAME=APP_NAME)


@bp.route('/patients_list/', methods=['GET', 'POST'])
@login_required
def patients_list():
    patient_list = patients_info()
    return render_template('patients_list.html', APP_NAME=APP_NAME, patient_list=patient_list)