from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='Mi primer API 192',
    description='Mario Alberto Hernandez Rodarte',
    version='1.0.1'
)

#Modelo de validaciones
class Usuario(BaseModel):
    id: int
    nombre: str
    edad: int
    email: str

#Base de datos ficticia
usuarios=[
    {"id": 1, "nombre": "mario", "edad": 19, "email": "mario@example.com"},
    {"id": 2, "nombre": "jose", "edad": 20, "email": "jose@example.com"},
    {"id": 3, "nombre": "pedro", "edad": 21, "email": "pedro@example.com"},
    {"id": 4, "nombre": "ana", "edad": 37, "email": "ana@example.com"}
]

#Endpoint home
@app.get('/', tags=['Hola Mundo'])
def home():
    return {'hello':'world FastAPI'}

#Endpoint consulta todos
@app.get('/todosusuarios', response_model=List[Usuario], tags=['Operaciones CRUD'])
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
    raise HTTPException(status_code=404, detail="Usuario no existe")

@app.delete('/eliminarusuario/{id}', tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    for usr in usuarios:
        if usr["id"]==id:
            usuarios.remove(usr)
            return {"Usuario eliminado con éxito"}
    raise HTTPException(status_code=404, detail="Usuario no existe")
            