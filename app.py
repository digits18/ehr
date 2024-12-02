from ThroneHospital import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)





# Create the Migration folder first by running the code below
# flask db init
#To initially migrate the db, run the code below
# flask db migrate -m "Initial migration."



# Finally
#To upgrade the db and effect changes in the db
#flask db upgrade