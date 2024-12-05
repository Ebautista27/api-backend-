"""Mensaje de la migración

Revision ID: 69d004bda864
Revises: 
Create Date: 2024-12-05 08:24:51.952630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69d004bda864'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categorias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metodos_pago',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.String(length=50), nullable=False),
    sa.Column('detalle', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('tallas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=False),
    sa.Column('categoria_talla', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('precio', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('estado', sa.String(length=10), nullable=True),
    sa.Column('id_categoria', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_categoria'], ['categorias.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('num_cel', sa.String(length=15), nullable=True),
    sa.Column('direccion', sa.String(length=100), nullable=True),
    sa.Column('contrasena_hash', sa.String(length=255), nullable=False),
    sa.Column('id_rol', sa.Integer(), nullable=False),
    sa.Column('estado', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['id_rol'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('carritos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('estado', sa.String(length=20), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pedidos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha_pedido', sa.Date(), nullable=True),
    sa.Column('estado_pedido', sa.String(length=50), nullable=True),
    sa.Column('total_pedido', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('direccion_envio', sa.String(length=100), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('id_metodo_pago', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_metodo_pago'], ['metodos_pago.id'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reseñas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comentario', sa.String(length=150), nullable=False),
    sa.Column('calificacion', sa.Integer(), nullable=False),
    sa.Column('id_producto', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_producto'], ['productos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carrito_productos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_carrito', sa.Integer(), nullable=True),
    sa.Column('id_producto', sa.Integer(), nullable=True),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.Column('subtotal', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['id_carrito'], ['carritos.id'], ),
    sa.ForeignKeyConstraint(['id_producto'], ['productos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('facturas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_pedido', sa.Integer(), nullable=True),
    sa.Column('monto_total', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('fecha_emision', sa.DateTime(), nullable=True),
    sa.Column('estado', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['id_pedido'], ['pedidos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('detalle_facturas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_factura', sa.Integer(), nullable=True),
    sa.Column('id_producto', sa.Integer(), nullable=True),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_factura'], ['facturas.id'], ),
    sa.ForeignKeyConstraint(['id_producto'], ['productos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detalle_facturas')
    op.drop_table('facturas')
    op.drop_table('carrito_productos')
    op.drop_table('reseñas')
    op.drop_table('pedidos')
    op.drop_table('carritos')
    op.drop_table('usuarios')
    op.drop_table('productos')
    op.drop_table('tallas')
    op.drop_table('roles')
    op.drop_table('metodos_pago')
    op.drop_table('categorias')
    # ### end Alembic commands ###
