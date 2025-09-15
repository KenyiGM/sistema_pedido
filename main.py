from datetime import datetime, timezone, date
import typer
from rich import print
from rich.table import Table

app = typer.Typer()


class Pedido:
    def __init__(
        self,
        id,
        monto_total,
        fecha=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    ):
        self.id = id
        self.fecha = fecha
        self.monto_total = monto_total


class Producto:
    def __init__(self, id, nombre, precio, stock):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock


class Detalle_Pedido:
    def __init__(
        self, id, cantidad, monto, descuento, producto: Producto, pedido: Pedido
    ):
        self.id = id
        self.producto = producto
        self.pedido = pedido
        self.cantidad = cantidad
        self.monto = monto
        self.descuento = descuento


datos_productos = {
    "productos": [
        Producto(id=1, nombre="Producto 1", precio=10.0, stock=10),
        Producto(id=2, nombre="Producto 2", precio=20.0, stock=5),
    ]
}

datos_pedidos = {"pedidos": []}

datos_detalle_pedido = {"detalle_pedido": []}


@app.command()
def main():
    while True:
        pedidos = datos_pedidos["pedidos"]
        detalle_pedidos = datos_detalle_pedido["detalle_pedido"]
        productos = datos_productos["productos"]
        print("Interfaz de Pedidos")
        print("1. Crear Pedido")
        print("2. Ver Resumen de Ventas")
        print("3. Salir")

        opcion_principal = typer.prompt("Ingrese una opción ", type=int)
        
        match opcion_principal:
            case 1:
                while True:
                    print("Crear Pedido")
                    pedido_agregar = Pedido(len(pedidos) + 1, 0.0)
                    print("1. Agregar Producto")
                    print("2. Finalizar Pedido")
                    print("3. Cancelar Pedido")
                    opcion_secundaria = typer.prompt("Ingrese una opción ", type=int)
                    match opcion_secundaria:
                        case 1:
                            print("Agregar Producto")
                            
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
                                "Ingrese el ID del producto ", type=int
                            )

                            if producto_id not in [
                                producto.id for producto in productos
                            ]:
                                print("Producto no encontrado")
                                continue

                            producto_cantidad = typer.prompt(
                                "Ingrese la cantidad del producto ", type=int
                            )

                            producto_obtenido = productos[producto_id - 1]

                            if producto_cantidad > producto_obtenido.stock:
                                print("Stock insuficiente")
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
                                id=len(detalle_pedidos) + 1,
                                producto=producto_obtenido,
                                cantidad=producto_cantidad,
                                monto=producto_cantidad * producto_obtenido.precio,
                                descuento=descuento,
                                pedido=pedido_agregar,
                            )

                            detalle_pedidos.append(detalle_pedido_agregar)
                            producto_obtenido.stock -= producto_cantidad

                        case 2:
                            print("Pedido creado con éxito")
                            monto_total_acumulado = 0
                            
                            for detalle_pedido in detalle_pedidos:
                                if pedido_agregar.id == detalle_pedido.pedido.id:
                                    monto_total_acumulado += detalle_pedido.monto - (detalle_pedido.monto * detalle_pedido.descuento)
                            
                            pedido_agregar.monto_total = monto_total_acumulado
                            pedidos.append(pedido_agregar)

                            tabla_pedidos = Table(title="Pedidos")
                            tabla_pedidos.add_column("ID")
                            tabla_pedidos.add_column("Fecha")
                            tabla_pedidos.add_column("Monto Total")

                            for pedido in pedidos:
                                tabla_pedidos.add_row(
                                    str(pedido.id),
                                    pedido.fecha,
                                    str(pedido.monto_total),
                                )

                            print(tabla_pedidos)

                            tabla_detalle_pedidos = Table(title="Detalle de Pedidos")
                            tabla_detalle_pedidos.add_column("ID")
                            tabla_detalle_pedidos.add_column("Producto")
                            tabla_detalle_pedidos.add_column("Cantidad")
                            tabla_detalle_pedidos.add_column("Monto")
                            tabla_detalle_pedidos.add_column("Descuento")
                            tabla_detalle_pedidos.add_column("Monto con Descuento")

                            for detalle_pedido in detalle_pedidos:
                                tabla_detalle_pedidos.add_row(
                                    str(detalle_pedido.id),
                                    detalle_pedido.producto.nombre,
                                    str(detalle_pedido.cantidad),
                                    str(detalle_pedido.monto),
                                    str(detalle_pedido.descuento * 100)+"%",
                                    str(detalle_pedido.monto - (detalle_pedido.monto * detalle_pedido.descuento)),
                                )
                            print(tabla_detalle_pedidos)
                            False
                            break
                        case 3:
                            print("Pedido cancelado")
                            for detalle_pedido in detalle_pedidos:
                                if pedido_agregar.id == detalle_pedido.pedido.id:
                                    producto_obtenido = detalle_pedido.producto
                                    producto_obtenido.stock += detalle_pedido.cantidad
                                    detalle_pedidos.remove(detalle_pedido)
                                    pedidos.remove(pedido_agregar)
                            False
                            break
                        case _:
                            print("Opción no válida")
            case 2:
                
                if len(pedidos) == 0:
                    print("No se han realizado pedidos hoy")
                    continue

                pedidos_realizados = len(pedidos)

                total_ventas = sum(pedido.monto_total for pedido in pedidos)

                producto_mas_vendido = "No hay productos"

                producto_menos_vendido = "No hay productos"

                datos_productos_hoy = {}

                for producto in productos:
                    datos_productos_hoy[producto.nombre] = 0

                for detalle_pedido in detalle_pedidos:
                    fecha = detalle_pedido.pedido.fecha
                    convertir_fecha = str(date(int(fecha[0:4]), int(fecha[5:7]), int(fecha[8:10])))
                    hoy = str(datetime.now(timezone.utc).strftime("%Y-%m-%d"))
                    if convertir_fecha == hoy:
                        for producto in productos:
                            if detalle_pedido.producto.nombre == producto.nombre:
                                datos_productos_hoy[producto.nombre] += detalle_pedido.cantidad
                        
                for producto, cantidad in datos_productos_hoy.items():
                    if cantidad == 0:
                        continue
                    elif max(datos_productos_hoy.values()) == min(datos_productos_hoy.values()):
                        producto_mas_vendido = producto
                        producto_menos_vendido = producto
                    elif cantidad == max(datos_productos_hoy.values()):
                        producto_mas_vendido = producto
                        pass
                    elif cantidad == min(datos_productos_hoy.values()):
                        producto_menos_vendido = producto
                        pass

                print("Resumen de Ventas")
                print(f"Pedidos realizados hoy: {pedidos_realizados}")
                print(f"Total de ventas: S/{total_ventas}")
                print(f"Producto mas vendido: {producto_mas_vendido}")
                print(f"Producto menos vendido: {producto_menos_vendido}")
            case 3:
                print("Salir")
                False
                break
            case _:
                print("Opción no válida")


if __name__ == "__main__":
    app()
