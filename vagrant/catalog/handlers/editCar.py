import os
from flask import (Flask, render_template, request, redirect,
                   url_for, jsonify, flash)
from project import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Dealers, Cars
from werkzeug.utils import secure_filename
from flask import session as login_session

engine = create_engine('sqlite:///cars4sale.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = '/vagrant/catalog/static/uploaded'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'bububu'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/car_<int:carID>/edit', methods=['GET', 'POST'])
def editCar(carID):
    if 'username' not in login_session:
        return redirect('/login')
    user = login_session['username']
    editedCar = session.query(Cars).filter_by(id=carID).one()
    # orderedInputs are used to show inputs in order that we want
    orderedInputs = ["make",
                     "model",
                     "trim",
                     "type",
                     "year",
                     "price",
                     "mileage"]
    if request.method == 'POST':
        # remove "uploaded" from "uploaded/filename"
        pictureFile = editedCar.picture[9:]
        # check if the post request has the file part
        if 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['picture']
        # save update dealer`s picture
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pictureFile))
        # update all changes after editing, picture was updated before
        editedCar.newCar = request.form['newCar'] == "True"
        editedCar.type = request.form['type']
        editedCar.make = request.form['make']
        editedCar.model = request.form['model']
        editedCar.trim = request.form['trim']
        editedCar.year = request.form['year']
        editedCar.mileage = request.form['mileage']
        editedCar.price = request.form['price']
        editedCar.description = request.form['description']
        session.commit()
        return redirect('/')
    else:
        inputs = {'newCarRadio': "",
                  'pre-ownedCarRadio': "",
                  'type': editedCar.type,
                  'make': editedCar.make,
                  'model': editedCar.model,
                  'trim': editedCar.trim,
                  'year': editedCar.year,
                  'mileage': editedCar.mileage,
                  'price': editedCar.price,
                  'description': editedCar.description,
                  'ID': editedCar.id}
        if editedCar.newCar:
            inputs['newCarRadio'] = 'checked'
        else:
            inputs['pre-ownedCarRadio'] = 'checked'
        return render_template('addCar.html',
                               user=user,
                               inputs=inputs,
                               orderedInputs=orderedInputs,
                               title="Edit car",
                               carPicture=editedCar.picture)
