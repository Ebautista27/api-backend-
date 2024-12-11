from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .modelos import db
from .vistas import (
    VistaUsuarios, VistaUsuario, VistaProductos, VistaProducto, VistaPedidos, VistaPedido, VistaReseñas, VistaReseña,
    VistaCrearUsuario, VistaRegistroUsuarios, VistaInicioSesion
)


def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/stayprueba'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de la base de datos y migraciones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configuración de JWT
    app.config['JWT_SECRET_KEY'] = 'supersecretkey'
    jwt = JWTManager(app)

    # Habilitar CORS
    CORS(app)

    # Configuración de la API RESTful
    api = Api(app)

    # ==================== Configuración de Rutas ==================== #

    # Rutas para usuarios
    api.add_resource(VistaUsuarios, '/usuarios')
    api.add_resource(VistaUsuario, '/usuarios/<int:id_usuario>')

    # Rutas para productos
    api.add_resource(VistaProductos, '/productos')
    api.add_resource(VistaProducto, '/productos/<int:id_producto>')

    # Rutas para pedidos
    api.add_resource(VistaPedidos, '/pedidos')
    api.add_resource(VistaPedido, '/pedidos/<int:id_pedido>')

    # Rutas para reseñas
    api.add_resource(VistaReseñas, '/reseñas')
    api.add_resource(VistaReseña, '/reseñas/<int:id_resena>')

    # Rutas para autenticación
    api.add_resource(VistaCrearUsuario, '/registrar_usuario')
    api.add_resource(VistaRegistroUsuarios, '/registro')
    api.add_resource(VistaInicioSesion, '/login')

    return app
