from datetime import datetime, timezone, date
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session
import typer
from rich import print
from rich.table import Table

from models import Producto, Pedido, Detalle_Pedido
from models import Base
from database import engine

app = typer.Typer()

Base.metadata.create_all(engine)

session = Session(engine)

@app.command()
def main():
    while True:
        print("\n\t*------Sistema de Pedidos------*\n")
        print("1. Crear Pedido")
        print("2. Ver Resumen de Ventas")
        print("3. Crear Producto")
        print("4. Agregar Stock a Producto")
        print("5. Salir")
        print()
        opcion_principal = typer.prompt("Ingrese una opción ", type=int)
        match opcion_principal:
            case 1:
                pedido_agregar = Pedido(monto_total=0, fecha=str(date.today()))

                session.add(pedido_agregar)
                session.commit()
                session.refresh(pedido_agregar)

                while True:
                    print("\nCrear Pedido\n")
                    print("1. Agregar Producto")
                    print("2. Finalizar Pedido")
                    print("3. Cancelar Pedido")
                    opcion_secundaria = typer.prompt("\nIngrese una opción ", type=int)
                    match opcion_secundaria:
                        case 1:
                            productos = session.scalars(select(Producto)).all()
                            if len(productos) == 0:
                                print("\nNo hay productos disponibles\n")
                                continue

                            print("\nAgregar Producto\n")
                            tabla_productos = Table(title="Productos Disponibles")
                            tabla_productos.add_column("ID")
                            tabla_productos.add_column("Nombre")
                            tabla_productos.add_column("Precio")
                            tabla_productos.add_column("Stock")

                            for producto in productos:
                                tabla_productos.add_row(
                                    str(producto.id),
                                    producto.nombre,
                                    str(producto.precio),
                                    str(producto.stock),
                                )

                            print(tabla_productos)

                            producto_id = typer.prompt(
                                "\nIngrese el ID del producto ", type=int
                            )

                            producto_buscado = session.get(Producto, producto_id)

                            if producto_buscado is None:
                                print("\nProducto no encontrado\n")
                                continue

                            producto_cantidad = typer.prompt(
                                "\nIngrese la cantidad del producto ", type=int
                            )

                            if producto_cantidad > producto_buscado.stock:
                                print("\nStock insuficiente\n")
                                continue

                            if producto_cantidad > 3:
                                descuento = 0.10
                            elif producto_cantidad > 5:
                                descuento = 0.20
                            elif producto_cantidad > 10:
                                descuento = 0.30
                            else:
                                descuento = 0.0

                            detalle_pedido_agregar = Detalle_Pedido(
                                cantidad=producto_cantidad,
                                monto=producto_cantidad * producto_buscado.precio,
                                descuento=descuento,
                                producto_id=producto_buscado.id,
                                pedido_id=pedido_agregar.id,
                            )

                            producto_buscado.stock -= producto_cantidad

                            session.add(detalle_pedido_agregar)
                            session.commit()
                            session.refresh(detalle_pedido_agregar)
                            session.refresh(producto_buscado)

                        case 2:
                            pedido_creado = session.get(Pedido, pedido_agregar.id)

                            detalle_pedidos = session.scalars(
                                select(Detalle_Pedido).where(Detalle_Pedido.pedido_id == pedido_creado.id)
                            ).all()

                            if detalle_pedidos == []:
                                print("\nNo hay productos en el pedido\n")
                                session.delete(pedido_creado)
                                session.commit()
                                break

                            for detalle_pedido in detalle_pedidos:
                                pedido_creado.monto_total += detalle_pedido.monto

                            session.commit()
                            session.refresh(pedido_creado)

                            tabla_pedido = Table(title="Pedido Creado")
                            tabla_pedido.add_column("ID")
                            tabla_pedido.add_column("Monto Total")
                            tabla_pedido.add_column("Fecha")

                            tabla_pedido.add_row(
                                str(pedido_creado.id),
                                str(pedido_creado.monto_total),
                                str(pedido_creado.fecha),
                            )

                            print(tabla_pedido)

                            tabla_detalle_pedido = Table(title="Detalle Pedido")
                            tabla_detalle_pedido.add_column("ID")
                            tabla_detalle_pedido.add_column("Cantidad")
                            tabla_detalle_pedido.add_column("Monto")
                            tabla_detalle_pedido.add_column("Descuento")
                            tabla_detalle_pedido.add_column("Producto ID")
                            tabla_detalle_pedido.add_column("Pedido ID")

                            for detalle_pedido in detalle_pedidos:
                                tabla_detalle_pedido.add_row(
                                    str(detalle_pedido.id),
                                    str(detalle_pedido.cantidad),
                                    str(detalle_pedido.monto),
                                    str(detalle_pedido.descuento),
                                    str(detalle_pedido.producto_id),
                                    str(detalle_pedido.pedido_id),
                                )

                            print(tabla_detalle_pedido)
                            False
                            break
                        case 3:
                            print("\nPedido cancelado\n")
                            detalle_pedido_eliminar = session.scalars(
                                select(Detalle_Pedido).where(
                                    Detalle_Pedido.pedido_id == pedido_agregar.id
                                )
                            ).all()
                            for detalle_pedido in detalle_pedido_eliminar:
                                session.delete(detalle_pedido)

                            session.delete(pedido_agregar)
                            session.commit()
                            False
                            break
                        case _:
                            print("\nOpción no válida\n")
            case 2:

                pedidos_obtenidos_hoy = session.scalars(
                    select(Pedido).where(Pedido.fecha == str(date.today()))
                ).all()

                if len(pedidos_obtenidos_hoy) == 0:
                    print("\nNo hay pedidos realizados hoy\n")
                    continue


                pedidos_realizados = len(pedidos_obtenidos_hoy)

                total_ventas = sum(
                    pedido.monto_total for pedido in pedidos_obtenidos_hoy
                )

                fecha_hoy = str(date.today())

                # Hace una consulta tipo sql, lo que buscar es el producto mas vendido y el menos vendido, desde la tablas Producto, Detalle_Pedido y Pedido cuando la fecha del pedido es hoy y suma la cantidad de los productos vendidos
                #text_sql_producto_mas_vendido = text(
                #    f"select prod.nombre, sum(dp.cantidad) from productos as prod join detalle_pedido dp on prod.id = dp.producto_id join pedidos p on dp.pedido_id = p.id where p.fecha == {fecha_hoy} group by prod.id order by sum(dp.cantidad) desc limit 1"
                #)
                #text_sql_producto_menos_vendido = text(
                #    f"select prod.nombre, sum(dp.cantidad) from productos as prod join detalle_pedido dp on prod.id = dp.producto_id join pedidos p on dp.pedido_id = p.id where p.fecha == {fecha_hoy} group by prod.id order by sum(dp.cantidad) asc limit 1"
                #)

                producto_mas_vendido = (
                    session.query(
                        Producto.nombre,
                        func.sum(Detalle_Pedido.cantidad).label("total_vendido"),
                    )
                    .join(Detalle_Pedido, Producto.id == Detalle_Pedido.producto_id)
                    .join(Pedido, Detalle_Pedido.pedido_id == Pedido.id)
                    .filter(func.date(Pedido.fecha) == fecha_hoy)
                    .group_by(Producto.id, Producto.nombre)
                    .order_by(func.sum(Detalle_Pedido.cantidad).desc())
                    .limit(1)
                    .first()
                )
                producto_menos_vendido = (
                    session.query(
                        Producto.nombre,
                        func.sum(Detalle_Pedido.cantidad).label("total_vendido"),
                    )
                    .join(Detalle_Pedido, Producto.id == Detalle_Pedido.producto_id)
                    .join(Pedido, Detalle_Pedido.pedido_id == Pedido.id)
                    .filter(func.date(Pedido.fecha) == fecha_hoy)
                    .group_by(Producto.id, Producto.nombre)
                    .order_by(func.sum(Detalle_Pedido.cantidad).asc())
                    .limit(1)
                    .first()
                )

                print("\nResumen de Ventas\n")
                print(f"\nPedidos realizados hoy: {pedidos_realizados}")
                print(f"\nMonto total de ventas: S/{round(total_ventas, 2)}")
                if producto_mas_vendido is None:
                    print("\nNo se han vendido productos hoy")
                else:   
                    print(f"\nProducto mas vendido: {producto_mas_vendido[0]} ({producto_mas_vendido[1]} unidades)")

                if producto_menos_vendido is None:
                    print("\nNo se han vendido productos hoy")
                else:
                    print(f"\nProducto menos vendido: {producto_menos_vendido[0]} ({producto_menos_vendido[1]} unidades)")
            case 3:
                print("Crear Producto")
                producto_nuevo = Producto(
                    nombre=typer.prompt("Ingrese el nombre del producto"),
                    precio=typer.prompt("Ingrese el precio del producto", type=float),
                    stock=typer.prompt("Ingrese el stock del producto", type=int)
                )
                producto_buscado = session.scalars(
                    select(Producto).where(Producto.nombre == producto_nuevo.nombre)
                ).first()
                
                if producto_buscado is not None or producto_buscado != None:
                    print("\nEl producto ya existe\n")
                    continue

                if producto_nuevo.stock <= 0:
                    print("\nEl stock debe ser mayor a 0\n")
                    continue
                    
                if producto_nuevo.precio <= 0:
                    print("\nEl precio debe ser mayor a 0\n")
                    continue

                session.add(producto_nuevo)
                session.commit()
                print("\nProducto creado exitosamente\n")
            case 4:
                print("\nAgregar stock a un producto\n")
                
                productos = session.scalars(select(Producto)).all()

                if productos is None or len(productos) == 0:
                    print("\nNo hay productos disponibles\n")
                    continue

                tabla_productos = Table(title="Productos")
                tabla_productos.add_column("ID", justify="center")
                tabla_productos.add_column("Nombre", justify="center")
                tabla_productos.add_column("Precio", justify="center")
                tabla_productos.add_column("Stock", justify="center")

                for producto in productos:
                    tabla_productos.add_row(
                        str(producto.id),
                        str(producto.nombre),
                        str(producto.precio),
                        str(producto.stock),
                    )

                print(tabla_productos)

                producto_id = typer.prompt("Ingrese el ID del producto", type=int)

                producto = session.get(Producto, producto_id)
                
                if producto is None:
                    print("\nEl producto no existe\n")
                    continue

                stock_agregar = typer.prompt("Ingrese la cantidad de stock a agregar", type=int)
                
                if stock_agregar <= 0:
                    print("\nEl stock debe ser mayor a 0\n")
                    continue

                producto_agregar_stock = session.get(Producto, producto_id)
                producto_agregar_stock.stock += stock_agregar

                session.commit()
                session.refresh(producto_agregar_stock)

                print("\nStock agregado exitosamente\n")
                
                continue

            case 5:
                print("Saliendo")
                False
                break
            case _:
                print("Opción no válida")


if __name__ == "__main__":
    app()
