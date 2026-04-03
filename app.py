
from flask import Flask, render_template, request, session, redirect, jsonify
from flask_socketio import SocketIO
from flask import request, jsonify
from models import db, SensorData, User
from ai import calculate_ai
import requests, math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.json

        temp = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
        gas = float(data.get('gas'))
        battery = float(data.get('battery'))
        crop = data.get('crop')

        if temp == 0:
            return {"status": "ignored"}

        ai = calculate_ai(temp, humidity, gas, crop)

        sensor = SensorData(
            temperature=temp,
            humidity=humidity,
            gas=gas,
            battery=battery,
            crop=crop,
            health_score=ai['health_score'],
            days_remaining=ai['days_remaining'],
            risk=ai['risk']
        )

        db.session.add(sensor)
        db.session.commit()

        # 🔥 REALTIME UPDATE
        socketio.emit("sensor_update", {
            "temperature": temp,
            "humidity": humidity,
            "gas": gas,
            "battery": battery,
            **ai
        })

        return {"status": "success"}

    except Exception as e:
        return {"error": str(e)}


@app.route('/api/predict')
def predict():
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(10).all()

    if not data:
        return {"data": []}

    last = data[0]

    predictions = []
    temp = last.temperature
    humidity = last.humidity
    gas = last.gas

    for i in range(1, 6):
        temp += 0.4
        humidity += 1
        gas += 10

        risk = min(100, int(temp + humidity/2 + gas/20))

        predictions.append({
            "time": f"+{i}h",
            "risk": risk
        })

    return {"data": predictions}


@socketio.on('sensor_data')
def handle_sensor_data(data):
    try:
        temp = float(data.get('temperature'))
        if temp == 0 or math.isnan(temp):
            return

        humidity = float(data.get('humidity'))
        gas = float(data.get('gas'))
        battery = float(data.get('battery'))
        crop = data.get('crop')

        ai = calculate_ai(temp, humidity, gas, crop)

        d = SensorData(temperature=temp, humidity=humidity, gas=gas,
                       battery=battery, crop=crop,
                       health_score=ai['health_score'],
                       days_remaining=ai['days_remaining'],
                       risk=ai['risk'])

        db.session.add(d)
        db.session.commit()

        socketio.emit("sensor_update", {
            "temperature": temp, "humidity": humidity,
            "gas": gas, "battery": battery,
            **ai
        })

    except Exception as e:
        print(e)

@app.route('/api/history')
def history():
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(20).all()
    return jsonify([{"t":d.temperature} for d in data])

@app.route('/api/weather')
def weather():
    r = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=YOUR_API_KEY&units=metric").json()
    return {"temp": r["main"]["temp"], "humidity": r["main"]["humidity"]}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app)
