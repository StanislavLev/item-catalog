from flask import Flask, render_template, request, redirect, url_for, jsonify
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Restaurant, MenuItem

# imports for login
#from flask import session as login_session
#import random
#import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

#engine = create_engine('sqlite:///restaurantmenu.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()

from handlers.welcome import *
from handlers.login import *
from handlers.car import *
from handlers.addCar import *
from handlers.editCar import *
from handlers.deleteCar import *
from handlers.carsJSON import *

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)