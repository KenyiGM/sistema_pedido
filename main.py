from datetime import datetime, timezone
import typer
from rich import print
from rich.table import Table

app = typer.Typer()

datos_productos = {
    "productos": [
        {"id": 1, "nombre": "Producto 1", "precio": 10.00, "stock": 10},
        {"id": 2, "nombre": "Producto 2", "precio": 20.00, "stock": 5},
    ]
}

datos_pedidos = {"pedidos": []}


@app.command()
def main():
    while True:
        print("Interfaz de Pedidos")
        print("1. Crear Pedido")
        print("2. Ver Resumen de Ventas")
        print("3. Salir")

        opcion_principal = typer.prompt("Ingrese una opción ", type=int)

        match opcion_principal:
            case 1:
                while True:
                    print("Crear Pedido")
                    pedidos = datos_pedidos["pedidos"]
                    pedido_agregar = {
                        'id': len(pedidos) + 1,
                        'fecha': datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                        'descuento': 0.0,
                        'total': 0.0,
                        'productos': []
                    }
                    print("1. Agregar Producto")
                    print("2. Finalizar Pedido")
                    print("3. Cancelar Pedido")
                    opcion_secundaria = typer.prompt("Ingrese una opción ", type=int)
                    match opcion_secundaria:
                        case 1:
                            print("Agregar Producto")
                            productos = datos_productos["productos"]
                            producto_agregar = {
                                "id": 0,
                                "nombre": "",
                                "precio": 0.0,
                                "cantidad": 0,
                                "descuento": 0.0
                            }
                            tabla_productos = Table(title="Productos Disponibles")
                            tabla_productos.add_column("ID")
                            tabla_productos.add_column("Nombre")
                            tabla_productos.add_column("Precio")
                            tabla_productos.add_column("Stock")
                            for producto in productos:
                                tabla_productos.add_row(
                                    str(producto["id"]),
                                    producto["nombre"],
                                    str(producto["precio"]),
                                    str(producto["stock"]),
                                )
                            print(tabla_productos)
                            producto_id = typer.prompt("Ingrese el ID del producto ", type=int)
                            
                            if producto_id not in [producto["id"] for producto in productos]:
                                print("Producto no encontrado")
                                continue
                            
                            producto_cantidad = typer.prompt("Ingrese la cantidad del producto ", type=int)
                            
                            if producto_cantidad > productos[producto_id - 1]["stock"]:
                                print("Stock insuficiente")
                                continue

                            # Creamos un preliminar del producto para evitar modificar datos
                            producto_agregar["id"] = producto_id
                            producto_agregar["nombre"] = [
                                producto for producto in productos if producto["id"] == producto_id
                            ][0]["nombre"]
                            producto_agregar["precio"] = [
                                producto for producto in productos if producto["id"] == producto_id
                            ][0]["precio"]
                            producto_agregar["cantidad"] = producto_cantidad

                            if producto_cantidad > 3:
                                producto_agregar["descuento"] = 0.10 # 10%
                            elif producto_cantidad > 5:
                                producto_agregar["descuento"] = 0.20 # 20%
                            elif producto_cantidad > 10:
                                producto_agregar["descuento"] = 0.30 # 30%
                            else:
                                producto_agregar["descuento"] = 0.0 # 0%

                            # Agregar producto al pedido
                            pedido_agregar["productos"].append(producto_agregar)
                            print(pedido_agregar)
                        case 2:
                            print("Pedido creado con éxito")
                            False
                            break
                        case 3:
                            print("Pedido cancelado")
                            False
                            break
                        case _:
                            print("Opción no válida")
            case 2:
                print("Resumen de Ventas")
                print("Pedidos realizados hoy: 20")
                print("Total de ventas: S/500.00")
                print("Producto mas vendido: Producto 1 (10 ventas)")
                print("Producto menos vendido: Producto 2 (5 ventas)")
            case 3:
                print("Salir")
                False
                break
            case _:
                print("Opción no válida")


if __name__ == "__main__":
    app()
