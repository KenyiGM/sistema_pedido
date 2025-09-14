from datetime import datetime, timezone
import typer
from rich import print
from rich.table import Table

app = typer.Typer()

@app.command()
def main():
    while True:
        print("Interfaz de Pedidos y Ventas")
        print("1. Crear Pedido")
        print("2. Ver Resumen de Ventas")
        print("3. Salir")

        opcion_principal = typer.prompt("Ingrese una opción: ", type=int)

        match opcion_principal:
            case 1:
                print("Crear Pedido")
                print("1. Agregar Producto")
                print("2. Finalizar Pedido")
                print("3. Cancelar Pedido")
                opcion_secundaria = typer.prompt("Ingrese una opción: ", type=int)
                match opcion_secundaria:
                    case 1:
                        print("Agregar Producto")
                        tabla_productos = Table(title="Productos Disponibles")
                        tabla_productos.add_column("ID")
                        tabla_productos.add_column("Nombre")
                        tabla_productos.add_column("Precio")
                        tabla_productos.add_column("Stock")
                        tabla_productos.add_row()
                        tabla_productos.add_row()
                        print(tabla_productos)
                        producto_id = typer.prompt("Ingrese el ID del producto: ", type=int)
                        producto_cantidad = typer.prompt("Ingrese la cantidad del producto: ", type=int)
                        print("Producto agregado con éxito")
                    case 2:
                        print("Pedido creado con éxito")
                    case 3:
                        print("Pedido cancelado")
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