from flask import request, jsonify
from flask_restful import Resource
from flaskr.modelos import Rol
from flaskr.modelos import db, Usuario, Rol
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from ..modelos import (
    db, Rol, Usuario, Carrito, CarritoProducto, Producto, Categoria, Talla,
    Pedido, MetodoPago, Factura, Reseña, DetalleFactura,
    UsuarioSchema, ProductoSchema, PedidoSchema, FacturaSchema, ReseñaSchema,
    MetodoPagoSchema, CarritoSchema, CarritoProductoSchema, CategoriaSchema,
    TallaSchema, DetalleFacturaSchema, RolSchema
)

# Serializadores
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)
factura_schema = FacturaSchema()
reseña_schema = ReseñaSchema()
reseñas_schema = ReseñaSchema(many=True)
metodo_pago_schema = MetodoPagoSchema()
metodos_pago_schema = MetodoPagoSchema(many=True)
carrito_schema = CarritoSchema()
carritos_schema = CarritoSchema(many=True)
categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)
talla_schema = TallaSchema()
tallas_schema = TallaSchema(many=True)
carrito_producto_schema = CarritoProductoSchema()
carritos_productos_schema = CarritoProductoSchema(many=True)
detalle_factura_schema = DetalleFacturaSchema()
detalles_factura_schema = DetalleFacturaSchema(many=True)

# ==================== Vistas para Usuarios ==================== #

class VistaCrearUsuario(Resource):
    def post(self):
        data = request.json
        if not data:
            return {"mensaje": "El cuerpo de la solicitud está vacío o mal formado"}, 400

        nombre = data.get("nombre")
        email = data.get("email")
        contrasena = data.get("password")
        num_cel = data.get("num_cel")  # Asegúrate de obtener este campo
        direccion = data.get("direccion")
        id_rol = data.get("id_rol", 2)  # Default rol_id es 2 (usuario)
        estado = "Activo"

        # Verificar campos obligatorios
        if not nombre or not email or not contrasena or not num_cel:
            return {"mensaje": "Nombre, email, contraseña y número de celular son obligatorios."}, 400

        # Validar que el email no esté registrado
        if Usuario.query.filter_by(email=email).first():
            return {"mensaje": "El email ya está registrado."}, 409

        # Validar que el rol exista
        rol = Rol.query.filter_by(id=id_rol).first()
        if not rol:
            return {"mensaje": f"El rol con ID {id_rol} no existe."}, 404

        # Crear el usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            num_cel=num_cel,  # Asegúrate de asignar este valor
            contrasena_hash=generate_password_hash(contrasena),
            direccion=direccion,
            id_rol=id_rol,
            estado=estado
        )

        # Guardar en la base de datos
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "Usuario registrado exitosamente."}, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error al registrar el usuario. Intenta nuevamente."}, 500



class VistaEliminarUsuario(Resource):
    @jwt_required()
    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaVerUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return usuario_schema.dump(usuario), 200

class VistaEditarUsuario(Resource):
    @jwt_required()
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.nombre = request.json.get("nombre", usuario.nombre)
        usuario.email = request.json.get("email", usuario.email)
        usuario.direccion = request.json.get("direccion", usuario.direccion)
        usuario.estado = request.json.get("estado", usuario.estado)
        db.session.commit()
        return usuario_schema.dump(usuario), 200

class VistaSeleccionRoles(Resource):
    @jwt_required()
    def get(self):
        roles = Rol.query.all()
        return [{"id": rol.id, "nombre": rol.nombre} for rol in roles], 200

class VistaRegistroUsuarios(Resource):
    def post(self):
        data = request.json
        if not data:
            return {"mensaje": "El cuerpo de la solicitud está vacío o mal formado"}, 400

        return VistaCrearUsuario().post()

class VistaInicioSesion(Resource):
    def post(self):
        email = request.json["email"]
        contrasena = request.json["password"]
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.verificar_contrasena(contrasena):
            token = create_access_token(identity={"id": usuario.id, "rol": usuario.id_rol})
            return {"mensaje": "Inicio de sesión exitoso", "token": token}, 200
        return {"mensaje": "Email o contraseña incorrectos"}, 401

class VistaCerrarSesion(Resource):
    @jwt_required()
    def post(self):
        return {"mensaje": "Sesión cerrada correctamente"}, 200

class VistaRecuperarContrasena(Resource):
    def post(self):
        email = request.json["email"]
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            # Aquí iría la lógica de envío de correo
            return {"mensaje": "Correo de recuperación enviado."}, 200
        return {"mensaje": "Email no encontrado"}, 404

# ==================== Vistas para Productos ==================== #

class VistaCrearProducto(Resource):
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

class VistaVerProducto(Resource):
    def get(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        return producto_schema.dump(producto), 200

class VistaEditarProducto(Resource):
    @jwt_required()
    def put(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        producto.nombre = request.json.get("nombre", producto.nombre)
        producto.descripcion = request.json.get("descripcion", producto.descripcion)
        producto.precio = request.json.get("precio", producto.precio)
        producto.estado = request.json.get("estado", producto.estado)
        db.session.commit()
        return producto_schema.dump(producto), 200

class VistaEliminarProducto(Resource):
    @jwt_required()
    def delete(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        db.session.delete(producto)
        db.session.commit()
        return '', 204

class VistaSeleccionTallaCantidad(Resource):
    def get(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        return {"id_producto": producto.id, "tallas": [{"id": talla.id, "nombre": talla.nombre} for talla in producto.tallas]}, 200

class VistaBuscarProducto(Resource):
    def get(self):
        nombre = request.args.get("nombre", "").lower()
        categoria = request.args.get("categoria", type=int)
        precio_min = request.args.get("precio_min", type=float)
        precio_max = request.args.get("precio_max", type=float)

        productos = Producto.query
        if nombre:
            productos = productos.filter(Producto.nombre.ilike(f"%{nombre}%"))
        if categoria:
            productos = productos.filter_by(id_categoria=categoria)
        if precio_min is not None:
            productos = productos.filter(Producto.precio >= precio_min)
        if precio_max is not None:
            productos = productos.filter(Producto.precio <= precio_max)

        return productos_schema.dump(productos.all()), 200

# ==================== Vistas para Reseñas ==================== #

class VistaCrearResena(Resource):
    @jwt_required()
    def post(self):
        nueva_resena = Reseña(
            comentario=request.json["comentario"],
            calificacion=request.json["calificacion"],
            id_producto=request.json["id_producto"]
        )
        db.session.add(nueva_resena)
        db.session.commit()
        return reseña_schema.dump(nueva_resena), 201

class VistaVerResena(Resource):
    def get(self, id_resena):
        reseña = Reseña.query.get_or_404(id_resena)
        return reseña_schema.dump(reseña), 200

class VistaEditarResena(Resource):
    @jwt_required()
    def put(self, id_resena):
        reseña = Reseña.query.get_or_404(id_resena)
        reseña.comentario = request.json.get("comentario", reseña.comentario)
        reseña.calificacion = request.json.get("calificacion", reseña.calificacion)
        db.session.commit()
        return reseña_schema.dump(reseña), 200

class VistaEliminarResena(Resource):
    @jwt_required()
    def delete(self, id_resena):
        reseña = Reseña.query.get_or_404(id_resena)
        db.session.delete(reseña)
        db.session.commit()
        return '', 204

# ==================== Vistas para Pedidos ==================== #

class VistaVerPedido(Resource):
    def get(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        return pedido_schema.dump(pedido), 200

class VistaCrearPedido(Resource):
    @jwt_required()
    def post(self):
        nuevo_pedido = Pedido(
            id_usuario=get_jwt_identity()["id"],
            total_pedido=request.json["total_pedido"],
            direccion_envio=request.json["direccion_envio"],
            id_metodo_pago=request.json["id_metodo_pago"]
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        return pedido_schema.dump(nuevo_pedido), 201

class VistaEditarPedido(Resource):
    @jwt_required()
    def put(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        pedido.total_pedido = request.json.get("total_pedido", pedido.total_pedido)
        pedido.direccion_envio = request.json.get("direccion_envio", pedido.direccion_envio)
        pedido.estado_pedido = request.json.get("estado_pedido", pedido.estado_pedido)
        db.session.commit()
        return pedido_schema.dump(pedido), 200

class VistaEliminarPedido(Resource):
    @jwt_required()
    def delete(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        db.session.delete(pedido)
        db.session.commit()
        return '', 204

class VistaRealizarPedido(Resource):
    @jwt_required()
    def post(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        pedido.estado_pedido = "Realizado"
        db.session.commit()
        return pedido_schema.dump(pedido), 200

# ==================== Vistas para Facturas ==================== #

class VistaSeleccionMetodoPago(Resource):
    def get(self):
        metodos = MetodoPago.query.all()
        return metodos_pago_schema.dump(metodos), 200

class VistaGenerarFactura(Resource):
    @jwt_required()
    def post(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        nueva_factura = Factura(
            id_usuario=pedido.id_usuario,
            monto_total=pedido.total_pedido
        )
        db.session.add(nueva_factura)
        db.session.commit()
        return factura_schema.dump(nueva_factura), 201