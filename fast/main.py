from fastapi import FastAPI
from typing import Optional

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='Mi primer API 192',
    description='Mario Alberto Hernandez Rodarte',
    version='1.0.1'
)

usuarios=[
    {"id": 1, "nombre": "mario", "edad": 19},
    {"id": 2, "nombre": "jose", "edad": 20},
    {"id": 3, "nombre": "pedro", "edad": 21},
    {"id": 4, "nombre": "ana", "edad": 37}
]

#Endpoint home
@app.get('/', tags=['Hola Mundo'])
def home():
    return {'hello':'world FastAPI'}

#Endpoint promedio
@app.get('/promedio', tags=['Calificación'])
def promedio():
    numeros = [1, 2, 3, 4, 5, 6, 7, 8]
    suma = sum(numeros)
    promedio = suma / len(numeros)
    return {'promedio': promedio}

#Endpoint parametro obligatorio
@app.get('/usuario/{id}', tags=['Parametro Obligatorio'])
def consultaUsuario(id: int):
    #conexion a la BD
    #consulta
    return {'Se encontro el usuario': id}

#Endpoint parametro opcional
@app.get('/usuario/', tags=['Parametro Opcional'])
def consultaUsuario(id: Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "Usuario encontrado", "usuario": usuario}
        return {"mensaje": f"No se encontró el usuario con el id: {id}"}
    else:
        return {"mensaje": "No se ha proporcionado un id"}