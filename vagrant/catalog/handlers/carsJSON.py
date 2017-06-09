import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from project import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Dealers, Cars
from werkzeug.utils import secure_filename

engine = create_engine('sqlite:///cars4sale.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON APIs to view car information
@app.route('/JSON')
def allCarsJSON():
    cars = session.query(Cars).all()
    return jsonify(cars=[r.serialize for r in cars])


@app.route('/car_<int:car_id>/JSON')
def carJSON(car_id):
    car = session.query(Cars).filter_by(id=car_id).one()
    return jsonify(car.serialize)
