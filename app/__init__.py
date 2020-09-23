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
            if name:
                pizzas = Pizza(name=name)
                pizzas.save()
                response = jsonify({
                    'id': pizzas.id,
                    'name': pizzas.name,
                    'order_time': pizzas.order_time,
                    'date_modified': pizzas.date_modified,
                    'size':pizzas.size,
                    'price':pizzas.price,
                    'crust':pizzas.crust,
                })
                response.status_code = 201
                return response
        else:
            # GET
            pizzas = Pizza.get_all()
            results = []

            for items in pizzas:
                obj = {
                     'id': pizzas.id,
                    'name': pizzas.name,
                    'order_time': pizzas.order_time,
                    'date_modified': pizzas.date_modified,
                    'size':pizzas.size,
                    'price':pizzas.price,
                    'crust':pizzas.crust,
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response


    return app