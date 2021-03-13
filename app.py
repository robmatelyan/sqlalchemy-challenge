import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Databse Setup
engine = create_engine("sqlite:///Resources_copy/hawaii.sqlite")

# Reflect existing database into new model
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement

station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date</br>"
    )

# Flask Routes
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session link
    session = Session(engine)

    #query all precipitation data
    precipitation = session.query(measurement.date, measurement.prcp).all()
    session.close()

    # create a dictionary from the row data and append to list
    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict['Date'] = date
        prcp_dict['Precipitation'] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # create session link
    session = Session(engine)

    # query all station data
    stations = session.query(station.id, station.name).all()
    session.close()

    # create dictionary
    station_list = []
    for id, name in stations:
        station_dict = {}
        station_dict['Station ID'] = id
        station_dict['Station Name'] = name
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link
    session = Session(engine)

    # query tobs
    date_one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    most_active = session.query(measurement.date, measurement.tobs).filter(measurement.date >= date_one_year).filter(measurement.station == 'USC00519281').all()
    session.close()

    #create dictionary
    tobs_list = []
    for date, tobs in most_active:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Temperature'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>")
def start_only(start_date):
    #create session
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date).all()
    session.close()
    
    start_date_list = []
    for min, max, avg in results:
        start_date_dict = {}
        start_date_dict['min_temp'] = min
        start_date_dict['max_temp'] = max
        start_date_dict['avg_temp'] = avg
        start_date_list.append(start_date_dict)
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date,end_date):
    #create session
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    start_end_list = []
    for min, max, avg in results:
        start_end_dict = {}
        start_end_dict['min_temp'] = min
        start_end_dict['max_temp'] = max
        start_end_dict['avg_temp'] = avg
        start_end_list.append(start_end_dict)
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)