from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50))
    precio: Mapped[float]
    stock: Mapped[int]

    detalle_pedidos: Mapped[list["Detalle_Pedido"]] = relationship(back_populates="producto")

class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    monto_total: Mapped[float]
    fecha: Mapped[str]

    detalle_pedidos: Mapped[list["Detalle_Pedido"]] = relationship(back_populates="pedido")


class Detalle_Pedido(Base):
    __tablename__ = "detalle_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cantidad: Mapped[int]
    monto: Mapped[float]
    descuento: Mapped[float]
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))

    producto: Mapped["Producto"] = relationship(back_populates="detalle_pedidos")
    pedido: Mapped["Pedido"] = relationship(back_populates="detalle_pedidos")