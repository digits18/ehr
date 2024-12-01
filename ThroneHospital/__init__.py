from flask import Flask
from .routes import bp
from .models import db, login_manager, Admin, Patient, Nurse, Doctor
from .models import migrate
from flask import jsonify
from config import Config
import logging


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'hjghfgjdfnzxbvfhgijhjsdvgsdhfejfs'
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///throne_db.sqlite"
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # Register blueprints here
    app.register_blueprint(bp)

    # Setup console logging
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('EHR Startup')

    @app.route('/patients_records')
    def patients_records():
        patient_list = []
        patient_records = Patient.query.all()
        for item in patient_records:
            dic = {'Patient Number': item.patient_num,
                   'First Name': item.first_name,
                   'Last Name': item.last_name,
                   'DOB': item.dob,
                   'Age': item.age,
                   'Gender': item.gender,
                   'Add': item.address,
                   'Mobile': item.mobile,
                   'Marital Status': item.marital_status,
                   'NHIS': item.nhis,
                   'Reg Date': item.reg_date
                   }
            patient_list.append(dic)
        return jsonify(patient_list)

    @app.route('/nurses_account')
    def nurses_account():
        nurse_list = []
        nurse_login_account = Nurse.query.all()
        for item in nurse_login_account:
            dic = {
                'First Name': item.first_name,
                'Last Name': item.last_name,
                'Mobile': item.mobile,
                'Email': item.email,
                'Username': item.username,
                'Profile Pic Filename': item.profile_pic,
                'status': item.status
            }
            nurse_list.append(dic)
        return jsonify(nurse_list)

    @app.route('/doctors_account')
    def doctors_account():
        doctor_list = []
        doctor_login_account = Doctor.query.all()
        for item in doctor_login_account:
            dic = {
                'First Name': item.first_name,
                'Last Name': item.last_name,
                'Mobile': item.mobile,
                'Email': item.email,
                'Username': item.username,
                'Profile Pic Filename': item.profile_pic,
                'status': item.status
            }
            doctor_list.append(dic)
        return jsonify(doctor_list)

    return app
