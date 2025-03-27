from fastapi import FastAPI
from db.connection import engine,Base
from routers.users import routerUsuarios
from routers.auth import routerAuth

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='Mi primer API 192',
    description='Mario Alberto Hernandez Rodarte',
    version='1.0.1'
)

Base.metadata.create_all(bind=engine)

#Endpoint home
@app.get('/', tags=['Hola Mundo'])
def home():
    return {'hello':'world FastAPI'}

app.include_router(routerUsuarios)

app.include_router(routerAuth)