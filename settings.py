API_SERVER = f"http://127.0.0.1:5002"
APP_NAME = "Throne Hospital"

'''Under __init__.py'''


# @app.route('/insert')
# def insert_page():
#     # Commit data into table here
#     username = 'admin'
#     password = 'throne2024'
#     admin = Admin(username, password)
#     db.session.add(admin)
#     db.session.commit()
#     return '<h1>Data Successfully Inserted</h1>'

# @app.route('/view_admin')
# def view_admin():
#     from flask import jsonify
#     admin_list = []
#     admin = Admin.query.all()
#     for item in admin:
#         dic = {'Username': item.username,
#                'Password': item.password,
#                }
#         admin_list.append(dic)
#     return jsonify(admin_list)


# @app.route('/delete')
# def insert_page():
#     # Commit data into table here
#     username = 'admin'
#     user = Admin.query.filter_by(username=username).first()
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         return '<h1>User Successfully deleted</h1>'
