
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    gas = db.Column(db.Float)
    battery = db.Column(db.Float)
    crop = db.Column(db.String(50))
    health_score = db.Column(db.Integer)
    days_remaining = db.Column(db.Integer)
    risk = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    role = db.Column(db.String(10))
    approved = db.Column(db.Boolean, default=False)
