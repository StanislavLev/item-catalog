import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from project import app
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Dealers, Cars
from flask import session as login_session

engine = create_engine('sqlite:///cars4sale.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

REMOVE_FOLDER = '/vagrant/catalog/static/'


# Page for delete car confirmation.
@app.route('/car_<int:carID>/delete', methods=['GET', 'POST'])
def deleteRestaurant(carID):
    if 'username' not in login_session:
        return redirect('/login')
    user = login_session['username']
    deleteCar = session.query(Cars).filter_by(id=carID).one()
    if request.method == 'POST':
        os.remove(REMOVE_FOLDER + deleteCar.picture)
        session.delete(deleteCar)
        session.commit()
        return redirect('/')
    else:
        return render_template('deleteCar.html',
                               deleteCar=deleteCar,
                               user=user)
