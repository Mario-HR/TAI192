from fastapi import FastAPI, HTTPException
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

#Endpoint consulta todos
@app.get('/todosusuarios', tags=['Operaciones CRUD'])
def leerUsuarios():
    return {"Los usuarios registrados son ":usuarios}

@app.post('/usuarios/', tags=['Operaciones CRUD'])
def agregarUsuario(usuario:dict):
    for usr in usuarios:
        if usr["id"]==usuario.get("id"):
            raise HTTPException(status_code=400, detail="ID ya existe")
    usuarios.append(usuario)
    return usuario

@app.put('/actualizarusuario/', tags=['Operaciones CRUD'])
def actualizarUsuario(usuario: dict):
    for usr in usuarios:
        if usr["id"]==usuario.get("id"):
            usuarios[usuarios.index(usr)]=usuario
            return usuario
        else:
            raise HTTPException(status_code=404, detail="Usuario no existe")

@app.delete('/eliminarusuario/{id}', tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    for usr in usuarios:
        if usr["id"]==id:
            usuarios.remove(usr)
            return {"Usuario eliminado con éxito"}
        else:
            raise HTTPException(status_code=404, detail="Usuario no existe")
            