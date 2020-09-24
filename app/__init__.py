from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    
    from app.models import Pizza
    
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    @app.route('/pizzas/', methods=['POST', 'GET'])
    def pizzas():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            size = str(request.data.get('size', ''))
            price = str(request.data.get('price', ''))
            crust = str(request.data.get('crust', ''))
            if name:
                piza = Pizza(name=name,size=size,price=price,crust=crust)
                piza.save()
                response = jsonify({
                    'id':piza.id,
                    'name':piza.name,
                    'size':piza.size,
                    'price':piza.price,
                    'crust':piza.crust,
                })
                response.status_code = 201
                return response
        else:
            # GET
            piza = Pizza.get_all()
            results = []

            for items in piza:
                obj = {
                     'id':items.id,
                    'name':items.name,
                    'size':items.size,
                    'price':items.price,
                    'crust':items.crust,
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    
    @app.route('/pizzas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def pizzas_manipulation(id, **kwargs):
     # retrieve a pizza using it's ID
        piza = Pizza.query.filter_by(id=id).first()
        if not piza:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            piza.delete()
            return {
            "message": "pizza {} deleted successfully".format(piza.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            piza.name = name
            piza.save()
            response = jsonify({
                'id':piza.id,
                'name':piza.name,
                'size':piza.size,
                'price':piza.price,
                'crust':piza.crust,
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id':piza.id,
                'name':piza.name,
                'size':piza.size,
                'price':piza.price,
                'crust':piza.crust,
            })
            response.status_code = 200
            return response



    return app