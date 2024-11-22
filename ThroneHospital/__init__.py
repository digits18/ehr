from flask import Flask
from .routes import bp
from .models import db, Admin, Patient, Nurse, Doctor
from .models import migrate
from .models import login_manager
from flask import jsonify


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'hjghfgjdfnzxbvfhgijhjsdvgsdhfejfs'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///throne_db.sqlite"
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # Register blueprints here
    app.register_blueprint(bp)

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

    @app.route('/nurse_accounts')
    def nurse_accounts():
        nurse_list = []
        nurse_login_account = Nurse.query.all()
        for item in nurse_login_account:
            dic = {
                'First Name': item.first_name,
                'Last Name': item.last_name,
                'Mobile': item.mobile,
                'Email': item.email,
                'Username': item.username,
                'Profile Pic Filename' : item.profile_pic,
                'status': item.status
            }
            nurse_list.append(dic)
        return jsonify(nurse_list)

    @app.route('/doctor_accounts')
    def doctor_accounts():
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

    @app.route('/delete')
    def insert_page():
        # Commit data into table here
        username = 'judyman'
        user = Nurse.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return '<h1>User Successfully deleted</h1>'

    @app.route('/delete')
    def delete():
        # Commit data into table here
        username = 'Sholatyr'
        user = Nurse.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return '<h1>User Successfully deleted</h1>'

    return app
