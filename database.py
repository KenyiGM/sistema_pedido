from sqlalchemy import create_engine

engine = create_engine("sqlite:///sistema_pedidos.db", echo=False)