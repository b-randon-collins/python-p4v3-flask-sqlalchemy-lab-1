# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    with db.session() as session: 
        earthquake = session.get(Earthquake, id) 

    if earthquake:
        return make_response(jsonify(earthquake.to_dict()), 200)
    else:
        return make_response(jsonify({'message': f'Earthquake {id} not found.'}), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    with db.session() as session: 
        earthquakes = session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()

        quake_list = [quake.to_dict() for quake in earthquakes]
        body = {
            "count": len(quake_list),
            "quakes": quake_list
        }

    return make_response(jsonify(body), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)