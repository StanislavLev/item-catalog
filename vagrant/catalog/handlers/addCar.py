import os
import datetime
from shutil import copyfile
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


@app.route('/new/', methods=['GET', 'POST'])
def addCar():
    if 'username' not in login_session:
        return redirect('/login')
    user = login_session['username']
    # orderedInputs are used to show inputs in order that we want
    orderedInputs = ["make",
                     "model",
                     "trim",
                     "type",
                     "year",
                     "price",
                     "mileage"]
    if request.method == 'POST':
        # This file has to be in "static/uploaded" folder
        # and used as default file if dealer doesn`t provide car picture
        pictureFile = 'default.jpg'
        # Car entity is created in database with "pictureFile".
        # It`s ID will be used later for uniq name of picture file
        addCar2db = Cars(newCar=(request.form['newCar'] == "True"),
                         created=datetime.datetime.utcnow(),
                         type=request.form['type'].lower(),
                         make=request.form['make'].lower(),
                         model=request.form['model'].lower(),
                         trim=request.form['trim'].lower(),
                         year=request.form['year'],
                         mileage=request.form['mileage'],
                         price=request.form['price'],
                         description=request.form['description'],
                         picture='uploaded/' + pictureFile,
                         dealer_id=login_session['dealer_id'])
        session.add(addCar2db)
        session.commit()
        # check if the post request has the file part
        if 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['picture']
        # if user does not select file, browser also
        # submit a empty part without filename
        # copy of default picture is created
        if file.filename == '':
            IDfilename = str(addCar2db.id) + '.jpg'
            srcPic = UPLOAD_FOLDER + '/' + pictureFile
            dstPic = UPLOAD_FOLDER + '/' + IDfilename
            copyfile(srcPic, dstPic)
        # save dealer`s picture
        else:
            IDfilename = str(addCar2db.id) + '.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], IDfilename))
        # update picture fileneme in DB
        addCar2db.picture = 'uploaded/' + IDfilename
        session.commit()
        return redirect('/')
    else:
        inputs = {'type': "Type:",
                  'make': "Make:",
                  'model': "Model:",
                  'trim': "Trim:",
                  'year': "2003",
                  'mileage': "12345",
                  'price': "12345",
                  'description': ""}
        return render_template('addCar.html',
                               user=user,
                               inputs=inputs,
                               orderedInputs=orderedInputs,
                               title="Add new car",
                               carPicture="uploaded/default.jpg")
