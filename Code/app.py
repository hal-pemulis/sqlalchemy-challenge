import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine('sqlite:///../Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    print('A request for the home page…')
    return (
        f'Welcome to my Hawaii climate app!<br/><br/>'
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start (YYYY-MM-DD)<br/>'
        f'/api/v1.0/start/end (YYYY-MM-DD)'
    )

@app.route('/api/v1.0/precipitation')
def precip():
    print('A request for the precipitation page…')
    results = session.query(Measurement.date, Measurement.prcp).all()
    return jsonify(results)

@app.route('/api/v1.0/stations')
def stations():
    print('A request for the stations page…')
    results = session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    return jsonify(results)


@app.route('/api/v1.0/tobs')
def tobs():
    print('A request for the temperature page…')
    
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').all()
    return jsonify(results)

@app.route('/api/v1.0/<start>')
def start_date(start):
    print('A request for the temperature page with start date…')

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    results = {
    "Minimum temperature" : session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date>=start_date).all()[0][0],
    "Maximum temperature" : round(session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start_date).all()[0][0],2), 
    "Average temperature" : session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date>=start_date).all()[0][0]
    }
    
    return jsonify(results)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):

    print('A request for the temperature page with start and end date…')

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    results = {
    "Minimum temperature" : session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()[0][0],
    "Maximum temperature" : round(session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()[0][0],2), 
    "Average temperature" : session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()[0][0],
    }
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)