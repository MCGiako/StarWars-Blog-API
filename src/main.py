"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Favoritos, Personajes, Planetas, Vehiculos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/usuario', methods=['GET'])
def handle_hello():
    all_usuarios = Usuario.query.all()
    all_usuarios = list(map(lambda x: x.serialize(), all_usuarios))
    return jsonify(all_usuarios), 200

#Acá se mostrarán todos mis Favoritos
@app.route('/favoritos', methods=['GET'])
def allFavoritos():
    all_favoritos = Favoritos.query.all()
    all_favoritos = list(map(lambda x: x.serialize(), all_favoritos))
    return jsonify(all_favoritos) 

@app.route('/usuario/favoritos', methods=['GET'])
def allUsuarioFavoritos():
    all_usuario_favoritos = Favoritos.query.all()
    all_usuario_favoritos = list(map(lambda x: x.serialize(), all_usuario_favoritos))
    return jsonify(all_usuario_favoritos)

@app.route('/usuario/favoritos<int:position>', methods=['POST'])
def PostFavoritos():
    all_usuario_favoritos = Favoritos.query.all()
    all_usuario_favoritos = list(map(lambda x: x.serialize(), all_usuario_favoritos))
    return jsonify(all_usuario_favoritos)

@app.route('/usuario/favoritos<int:position>', methods=['DELETE'])
def DeleteFavoritos():
    delete_usuario_favoritos = Favoritos.query.all()
    delete_usuario_favoritos = list(map(lambda x: x.serialize(), delete_usuario_favoritos))
    return jsonify(delete_usuario_favoritos)


#Acá se mostrarán todos mis Personajes
@app.route('/personajes', methods=['GET'])
def allPersonajes():
    all_personajes = Personajes.query.all()
    all_personajes = list(map(lambda x: x.serialize(), all_personajes))
    return jsonify(all_personajes)   


#Acá se mostrarán todos mis Planetas
@app.route('/planetas', methods=['GET'])
def allPlanetas():
    all_planetas = Planetas.query.all()
    all_planetas = list(map(lambda x: x.serialize(), all_planetas))
    return jsonify(all_planetas)   



#Acá se mostrarán todos mis Vehículos
@app.route('/vehiculos', methods=['GET'])
def allVehiculos():
    all_vehiculos = Vehiculos.query.all()
    all_vehiculos = list(map(lambda x: x.serialize(), all_vehiculos))
    return jsonify(all_vehiculos) 



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
