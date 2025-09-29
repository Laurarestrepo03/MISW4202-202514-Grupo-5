from datetime import datetime
from .db import db
from sqlalchemy import ForeignKey, Integer, String, Float, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Usuario(db.Model):

    __tablename__ = 'usuarios'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    def __init__(self, username: str):
        self.username = username

    def __repr__(self):
        return f'<Usuario id {self.id}, username {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }
    


class PedidoItem(db.Model):

    __tablename__ = 'pedido_items'
    pedido_id: Mapped[int] = mapped_column(ForeignKey('pedidos.id'), primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey('productos.id'), primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    pedido = relationship("Pedido", back_populates='pedido_items')
    producto = relationship("Producto", back_populates='pedido_items')

    def to_dict(self):
        return {
            'pedido_id': self.pedido_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'producto': self.producto.to_dict() if self.producto else None
        }


class Cliente(db.Model):

    __tablename__ = 'clientes'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    
    pedidos_asociados = relationship("Pedido", back_populates="cliente")

    def __init__(self, nombre: str):
        self.nombre = nombre

    def __repr__(self):
        return f'<Cliente {self.nombre}, id={self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }

class Producto(db.Model):

    __tablename__ = 'productos'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)

    pedido_items = relationship("PedidoItem", back_populates='producto')

    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

    def __repr__(self):
        return f'<Producto {self.nombre}, id={self.id}, precio={self.precio}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio
        }

class Pedido(db.Model):

    __tablename__ = 'pedidos'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    total_pedido: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    comision: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    usuario_creacion: Mapped[str] = mapped_column(nullable=True)
    usuario_modificacion: Mapped[str] = mapped_column(nullable=True)

    fecha_creacion: Mapped[datetime] = mapped_column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    fecha_modificacion: Mapped[datetime] = mapped_column(db.DateTime, onupdate=db.func.current_timestamp(), nullable=True)

    cliente_id: Mapped[int] = mapped_column(ForeignKey('clientes.id'), nullable=False)

    pedido_items = relationship("PedidoItem", back_populates='pedido')
    cliente = relationship("Cliente", back_populates='pedidos_asociados')

    def __repr__(self):
        return f'<Pedido id={self.id}, cliente_id={self.cliente_id}, fecha_creacion={self.fecha_creacion}, fecha_modificacion={self.fecha_modificacion}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion,
            'total_pedido': self.total_pedido,
            'comision': self.comision,
            'usuario_creacion': self.usuario_creacion,
            'usuario_modificacion': self.usuario_modificacion,
            'items': self.pedido_items.to_dict() if self.pedido_items else None
        }