# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body ={'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)


@app.route('/demo_json')
def demo_json():
    pets = Pet.query.all()
    
    pet_list = []
    
    for pet in pets:
        pet_dict = {
            'id': pet.id, 
            'name' : pet.name, 
            'species' : pet.species
        }
        pet_list.append(pet_dict)
        
    return make_response(pet_list, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.get(id)
    
    if pet:
        body = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        status = 200
    else:
        body = {
            'message': f'Pet {id} not found.'
        }
        status = 404
        
    return make_response(body, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pet_list = []
    
    pets = Pet.query.filter_by(species=species).all()
    
    for pet in pets:
        pet_dict = {
            'id': pet.id,
            'name': pet.name,
        }
        pet_list.append(pet_dict)
    
    body = {
        'count': len(pet_list),
        'pets': pet_list
    }
        
    response = make_response(body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
