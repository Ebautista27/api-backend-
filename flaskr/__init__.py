from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .modelos import db
from .vistas import (
    VistaCrearUsuario, VistaEliminarUsuario, VistaVerUsuario, VistaEditarUsuario,
    VistaSeleccionRoles, VistaRegistroUsuarios, VistaInicioSesion, VistaCerrarSesion, VistaRecuperarContrasena,
    VistaCrearProducto, VistaVerProducto, VistaEditarProducto, VistaEliminarProducto, VistaSeleccionTallaCantidad,
    VistaBuscarProducto, VistaCrearResena, VistaVerResena, VistaEditarResena, VistaEliminarResena,
    VistaVerPedido, VistaCrearPedido, VistaEditarPedido, VistaEliminarPedido,
    VistaRealizarPedido, VistaSeleccionMetodoPago, VistaGenerarFactura
)

def create_app():
    app = Flask(__name__)  # Corregido el nombre del parámetro

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/stayprueba'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de la base de datos y migración
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configuración de JWT
    app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Cambia esto por una clave más segura
    jwt = JWTManager(app)

    # Habilita CORS para permitir solicitudes de otros dominios
    CORS(app)

    # Configuración de la API RESTful
    api = Api(app)

    # ==================== Configuración de Rutas ==================== #

    # Rutas para usuarios
    api.add_resource(VistaCrearUsuario, '/usuarios')
    api.add_resource(VistaEliminarUsuario, '/usuarios/<int:id_usuario>')
    api.add_resource(VistaVerUsuario, '/usuarios/<int:id_usuario>')
    api.add_resource(VistaEditarUsuario, '/usuarios/<int:id_usuario>/editar')

    # Rutas relacionadas con roles y autenticación
    api.add_resource(VistaSeleccionRoles, '/roles')
    api.add_resource(VistaRegistroUsuarios, '/registro')
    api.add_resource(VistaInicioSesion, '/login')
    api.add_resource(VistaCerrarSesion, '/logout')
    api.add_resource(VistaRecuperarContrasena, '/recuperar-contrasena')

    # Rutas para productos
    api.add_resource(VistaCrearProducto, '/productos')
    api.add_resource(VistaVerProducto, '/productos/<int:id_producto>')
    api.add_resource(VistaEditarProducto, '/productos/<int:id_producto>/editar')
    api.add_resource(VistaEliminarProducto, '/productos/<int:id_producto>/eliminar')
    api.add_resource(VistaSeleccionTallaCantidad, '/productos/<int:id_producto>/tallas')
    api.add_resource(VistaBuscarProducto, '/productos/buscar')

    # Rutas para reseñas
    api.add_resource(VistaCrearResena, '/reseñas')
    api.add_resource(VistaVerResena, '/reseñas/<int:id_resena>')
    api.add_resource(VistaEditarResena, '/reseñas/<int:id_resena>/editar')
    api.add_resource(VistaEliminarResena, '/reseñas/<int:id_resena>/eliminar')

    # Rutas para pedidos
    api.add_resource(VistaCrearPedido, '/pedidos')
    api.add_resource(VistaVerPedido, '/pedidos/<int:id_pedido>')
    api.add_resource(VistaEditarPedido, '/pedidos/<int:id_pedido>/editar')
    api.add_resource(VistaEliminarPedido, '/pedidos/<int:id_pedido>/eliminar')

    # Rutas relacionadas con la gestión de pedidos y facturación
    api.add_resource(VistaRealizarPedido, '/pedidos/<int:id_pedido>/realizar')
    api.add_resource(VistaSeleccionMetodoPago, '/metodos-pago')
    api.add_resource(VistaGenerarFactura, '/facturas/pedidos/<int:id_pedido>')

    return app
