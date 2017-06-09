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


# Page with more car info.
@app.route('/car_<int:carID>/', methods=['GET'])
def car(carID):
    if 'username' not in login_session:
        user = "guest"
    else:
        user = login_session['username']
    car = session.query(Cars).filter_by(id=carID).one()
    dealer = session.query(Dealers).filter_by(id=car.dealer_id).one()
    return render_template('car.html',
                           car=car,
                           user=user,
                           dealerName=dealer.name)
