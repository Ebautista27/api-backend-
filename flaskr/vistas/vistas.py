from flask import request, jsonify
from flask_restful import Resource
from flaskr.modelos import Rol
from flaskr.modelos import db, Usuario, Rol
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from ..modelos import (
    db, Rol, Usuario, Carrito, CarritoProducto, Producto, Categoria, Talla,
    Pedido, MetodoPago, Factura, Reseña, DetalleFactura,
    UsuarioSchema, ProductoSchema, PedidoSchema, FacturaSchema, ReseñaSchema,
    MetodoPagoSchema, CarritoSchema, CarritoProductoSchema, CategoriaSchema,
    TallaSchema, DetalleFacturaSchema, RolSchema
)

import logging


# Serializadores
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)
reseña_schema = ReseñaSchema()
reseñas_schema = ReseñaSchema(many=True)

# ==================== Vistas Generales ==================== #

"""
class VistaUsuarios(Resource):
    @jwt_required()
    def get(self):
        try:
            logging.info("Recibida solicitud GET en /usuarios")
            usuarios = Usuario.query.all()
            logging.info(f"Usuarios encontrados: {len(usuarios)}")
            return usuarios_schema.dump(usuarios), 200
        except Exception as e:
            logging.error(f"Error en VistaUsuarios.get: {str(e)}")
            return {"mensaje": "Error interno del servidor."}, 500

    @jwt_required()
    def post(self):
        try:
            nuevo_usuario = Usuario(
                nombre=request.json['nombre'],
                email=request.json['email'],
                num_cel=request.json.get('num_cel', ''),
                direccion=request.json.get('direccion', ''),
                contrasena_hash=generate_password_hash(request.json['contrasena']),
                id_rol=request.json['id_rol'],
                estado=request.json.get('estado', 'Activo')
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return usuario_schema.dump(nuevo_usuario), 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error de integridad: {str(e)}")
            return {"mensaje": "Error al crear el usuario. Verifique los datos ingresados."}, 409
        except KeyError as e:
            logging.error(f"Falta el campo: {str(e)}")
            return {"mensaje": f"Falta el campo obligatorio: {str(e)}."}, 400
        except Exception as e:
            logging.error(f"Error en VistaUsuarios.post: {str(e)}")
            return {"mensaje": "Error interno del servidor."}, 500
"""
class VistaUsuarios(Resource):
    @jwt_required()
    def get(self):
        try:
            # Obtener el ID del usuario actual desde el token
            usuario_actual_id = get_jwt_identity()
            if not isinstance(usuario_actual_id, (str, int)):
                raise ValueError("El ID del usuario no es un formato válido.")

            logging.info(f"Usuario autenticado con ID: {usuario_actual_id}")

            # Consultar todos los usuarios en la base de datos
            usuarios = Usuario.query.all()

            if not usuarios:
                logging.info("No hay usuarios registrados en la base de datos.")
                return {"mensaje": "No hay usuarios registrados."}, 200

            logging.info(f"Usuarios encontrados: {len(usuarios)}")
            return usuarios_schema.dump(usuarios), 200
        except ValueError as ve:
            logging.error(f"Error en validación del token: {str(ve)}")
            return {"mensaje": str(ve)}, 422
        except Exception as e:
            logging.error(f"Error en VistaUsuarios.get: {str(e)}")
            return {"mensaje": "Error interno del servidor."}, 500

    @jwt_required()
    def post(self):
        try:
            # Crear un nuevo usuario con los datos proporcionados
            nuevo_usuario = Usuario(
                nombre=request.json['nombre'],
                email=request.json['email'],
                num_cel=request.json.get('num_cel', ''),
                direccion=request.json.get('direccion', ''),
                contrasena_hash=generate_password_hash(request.json['contrasena']),
                id_rol=request.json['id_rol'],
                estado=request.json.get('estado', 'Activo')
            )

            # Guardar el usuario en la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()

            logging.info(f"Usuario creado exitosamente: {nuevo_usuario.nombre}")
            return usuario_schema.dump(nuevo_usuario), 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error de integridad: {str(e)}")
            return {"mensaje": "Error al crear el usuario. Verifique los datos ingresados."}, 409
        except KeyError as e:
            logging.error(f"Falta el campo obligatorio: {str(e)}")
            return {"mensaje": f"Falta el campo obligatorio: {str(e)}."}, 400
        except Exception as e:
            logging.error(f"Error en VistaUsuarios.post: {str(e)}")
            return {"mensaje": "Error interno del servidor."}, 500





"""
class VistaUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return usuario_schema.dump(usuario), 200

    @jwt_required()
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.nombre = request.json.get("nombre", usuario.nombre)
        usuario.email = request.json.get("email", usuario.email)
        usuario.direccion = request.json.get("direccion", usuario.direccion)
        usuario.estado = request.json.get("estado", usuario.estado)
        db.session.commit()
        return usuario_schema.dump(usuario), 200

    @jwt_required()
    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
"""
class VistaUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        try:
            usuario_actual_id = get_jwt_identity()
            if not usuario_actual_id:
                return {"mensaje": "Token inválido o no proporcionado."}, 401

            usuario = Usuario.query.get_or_404(id_usuario)
            return usuario_schema.dump(usuario), 200
        except Exception as e:
            logging.error(f"Error en VistaUsuario.get: {str(e)}")
            return {"mensaje": "Error interno del servidor."}, 500

    @jwt_required()
    def put(self, id_usuario):
        try:
            usuario_actual_id = get_jwt_identity()
            if not usuario_actual_id:
                return {"mensaje": "Token inválido o no proporcionado."}, 401

            usuario = Usuario.query.get_or_404(id_usuario)
            usuario.nombre = request.json.get("nombre", usuario.nombre)
            usuario.email = request.json.get("email", usuario.email)
            usuario.direccion = request.json.get("direccion", usuario.direccion)
            usuario.estado = request.json.get("estado", usuario.estado)
            db.session.commit()
            return usuario_schema.dump(usuario), 200
        except Exception as e:
            logging.error(f"Error en VistaUsuario.put: {str(e)}")
            return {"mensaje": "Error interno del servidor."}, 500

    @jwt_required()
    def delete(self, id_usuario):
        try:
            usuario_actual_id = get_jwt_identity()
            if not usuario_actual_id:
                return {"mensaje": "Token inválido o no proporcionado."}, 401

            usuario = Usuario.query.get_or_404(id_usuario)
            db.session.delete(usuario)
            db.session.commit()
            return '', 204
        except Exception as e:
            logging.error(f"Error en VistaUsuario.delete: {str(e)}")
            return {"mensaje": "Error interno del servidor."}, 500
        


class VistaProductos(Resource):
    def get(self):
        productos = Producto.query.all()
        return productos_schema.dump(productos), 200

class VistaProducto(Resource):
    @jwt_required()
    def get(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        return producto_schema.dump(producto), 200

    @jwt_required()
    def post(self):
        nuevo_producto = Producto(
            nombre=request.json["nombre"],
            descripcion=request.json.get("descripcion"),
            precio=request.json["precio"],
            estado=request.json.get("estado", "Disponible"),
            id_categoria=request.json["id_categoria"]
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return producto_schema.dump(nuevo_producto), 201

    @jwt_required()
    def put(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        producto.nombre = request.json.get("nombre", producto.nombre)
        producto.descripcion = request.json.get("descripcion", producto.descripcion)
        producto.precio = request.json.get("precio", producto.precio)
        producto.estado = request.json.get("estado", producto.estado)
        db.session.commit()
        return producto_schema.dump(producto), 200

    @jwt_required()
    def delete(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        db.session.delete(producto)
        db.session.commit()
        return '', 204

class VistaPedidos(Resource):
    @jwt_required()
    def get(self):
        pedidos = Pedido.query.all()
        return pedidos_schema.dump(pedidos), 200

class VistaPedido(Resource):
    @jwt_required()
    def get(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        return pedido_schema.dump(pedido), 200

    @jwt_required()
    def post(self):
        nuevo_pedido = Pedido(
            id_usuario=request.json["id_usuario"],
            total_pedido=request.json["total_pedido"],
            direccion_envio=request.json["direccion_envio"],
            id_metodo_pago=request.json["id_metodo_pago"]
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        return pedido_schema.dump(nuevo_pedido), 201

    @jwt_required()
    def put(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        pedido.total_pedido = request.json.get("total_pedido", pedido.total_pedido)
        pedido.direccion_envio = request.json.get("direccion_envio", pedido.direccion_envio)
        pedido.estado_pedido = request.json.get("estado_pedido", pedido.estado_pedido)
        db.session.commit()
        return pedido_schema.dump(pedido), 200

    @jwt_required()
    def delete(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        db.session.delete(pedido)
        db.session.commit()
        return '', 204

class VistaReseñas(Resource):
    def get(self):
        reseñas = Reseña.query.all()
        return reseñas_schema.dump(reseñas), 200

class VistaReseña(Resource):
    @jwt_required()
    def get(self, id_resena):
        reseña = Reseña.query.get_or_404(id_resena)
        return reseña_schema.dump(reseña), 200

    @jwt_required()
    def post(self):
        nueva_reseña = Reseña(
            comentario=request.json["comentario"],
            calificacion=request.json["calificacion"],
            id_producto=request.json["id_producto"]
        )
        db.session.add(nueva_reseña)
        db.session.commit()
        return reseña_schema.dump(nueva_reseña), 201

    @jwt_required()
    def put(self, id_resena):
        reseña = Reseña.query.get_or_404(id_resena)
        reseña.comentario = request.json.get("comentario", reseña.comentario)
        reseña.calificacion = request.json.get("calificacion", reseña.calificacion)
        db.session.commit()
        return reseña_schema.dump(reseña), 200

    @jwt_required()
    def delete(self, id_resena):
        reseña = Reseña.query.get_or_404(id_resena)
        db.session.delete(reseña)
        db.session.commit()
        return '', 204

# ==================== Vistas de Autenticación ==================== #
"""
class VistaCrearUsuario(Resource):
    def post(self):
        data = request.json
        if not data:
            return {"mensaje": "El cuerpo de la solicitud está vacío o mal formado"}, 400

        nombre = data.get("nombre")
        email = data.get("email")
        contrasena = data.get("password")
        num_cel = data.get("num_cel")
        direccion = data.get("direccion")
        id_rol = data.get("id_rol", 2)
        estado = "Activo"

        if not nombre or not email or not contrasena or not num_cel:
            return {"mensaje": "Nombre, email, contraseña y número de celular son obligatorios."}, 400

        if Usuario.query.filter_by(email=email).first():
            return {"mensaje": "El email ya está registrado."}, 409

        rol = Rol.query.filter_by(id=id_rol).first()
        if not rol:
            return {"mensaje": f"El rol con ID {id_rol} no existe."}, 404

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            num_cel=num_cel,
            contrasena_hash=generate_password_hash(contrasena),
            direccion=direccion,
            id_rol=id_rol,
            estado=estado
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "Usuario registrado exitosamente."}, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error al registrar el usuario. Intenta nuevamente."}, 500
 """       
class VistaCrearUsuario(Resource):
    def post(self):
        data = request.json
        if not data:
            return {"mensaje": "El cuerpo de la solicitud está vacío o mal formado"}, 400

        nombre = data.get("nombre")
        email = data.get("email")
        contrasena = data.get("password")
        num_cel = data.get("num_cel")
        direccion = data.get("direccion")
        id_rol = data.get("id_rol", 2)
        estado = "Activo"

        if not nombre or not email or not contrasena or not num_cel:
            return {"mensaje": "Nombre, email, contraseña y número de celular son obligatorios."}, 400

        if Usuario.query.filter_by(email=email).first():
            return {"mensaje": "El email ya está registrado."}, 409

        rol = Rol.query.filter_by(id=id_rol).first()
        if not rol:
            return {"mensaje": f"El rol con ID {id_rol} no existe."}, 404

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            num_cel=num_cel,
            contrasena_hash=generate_password_hash(contrasena),
            direccion=direccion,
            id_rol=id_rol,
            estado=estado
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "Usuario registrado exitosamente."}, 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error de integridad: {str(e)}")
            return {"mensaje": "Error al registrar el usuario. Intenta nuevamente."}, 500







"""
class VistaRegistroUsuarios(Resource):
    def post(self):
        data = request.json
        if not data:
            return {"mensaje": "El cuerpo de la solicitud está vacío o mal formado"}, 400

        return VistaCrearUsuario().post()

from flask_jwt_extended import create_access_token
"""
class VistaRegistroUsuarios(Resource):
    def post(self):
        data = request.json
        if not data:
            return {"mensaje": "El cuerpo de la solicitud está vacío o mal formado"}, 400

        return VistaCrearUsuario().post()






"""
class VistaInicioSesion(Resource):
    def post(self):
        email = request.json.get("email")
        contrasena = request.json.get("password")

        # Buscar usuario por email
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_contrasena(contrasena):
            # Generar el token con el ID y el rol del usuario
            #token = create_access_token(identity={"id": usuario.id, "rol": usuario.id_rol})
            token = create_access_token(identity=str(usuario.id))
            mensaje = "Inicio de sesión exitoso"
            if usuario.id_rol == 1:
                mensaje += " como administrador"
            return {"mensaje": mensaje, "token": token}, 200

        return {"mensaje": "Email o contraseña incorrectos"}, 401

"""
class VistaInicioSesion(Resource):
    def post(self):
        email = request.json.get("email")
        contrasena = request.json.get("password")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_contrasena(contrasena):
            token = create_access_token(identity=str(usuario.id))
            mensaje = "Inicio de sesión exitoso"
            if usuario.id_rol == 1:
                mensaje += " como administrador"
            return {"mensaje": mensaje, "token": token}, 200

        return {"mensaje": "Email o contraseña incorrectos"}, 401