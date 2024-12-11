from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .modelo import (
    Rol, Usuario, Carrito, CarritoProducto, Producto, Categoria, Talla,
    Pedido, MetodoPago, Factura, Reseña, DetalleFactura
)

from marshmallow import fields

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"name": value.name, "value": value.value}  # Convierte el Enum a un diccionario


class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    # Si tienes un Enum para 'rol', usa la misma lógica de conversión
    rol = EnumADiccionario(attribute="rol")
    
    class Meta:
        model = Usuario
        include_relationships = True  # Incluir relaciones como 'rol'
        load_instance = True  # Habilitar carga de instancias SQLAlchemy
        exclude = ("contrasena_hash",)  # Excluir campos sensibles como contraseñas


class CarritoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Carrito
        include_relationships = True
        load_instance = True

class CarritoProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CarritoProducto
        include_relationships = True
        load_instance = True

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationships = True
        load_instance = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class TallaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Talla
        include_relationships = True
        load_instance = True

class PedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        include_relationships = True
        load_instance = True

class MetodoPagoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MetodoPago
        include_relationships = True
        load_instance = True

class FacturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Factura
        include_relationships = True
        load_instance = True

class ReseñaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reseña
        include_relationships = True
        load_instance = True

class DetalleFacturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DetalleFactura
        include_relationships = True
        load_instance = True
