from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional,List
from pydanticModels import modeloUsuario, modeloAutentificacion
from genToken import createToken

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='Mi primer API 192',
    description='Mario Alberto Hernandez Rodarte',
    version='1.0.1'
)

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

#Endpoint de autenticacion
@app.post('/auth', tags=['Autentificacion'])
def login(autorizacion:modeloAutentificacion):
    if autorizacion.email == "mario@example.com" and autorizacion.passwd == "12345678":
        token:str=createToken(autorizacion.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return("Aviso: Usuario sin aurorización")

#Endpoint consulta todos
@app.get('/todosusuarios', response_model=List[modeloUsuario], tags=['Operaciones CRUD'])
def leerUsuarios():
    return usuarios

@app.post('/usuario/', response_model=modeloUsuario, tags=['Operaciones CRUD'])
def agregarUsuario(usuario:modeloUsuario):
    for usr in usuarios:
        if usr["id"]==usuario.get("id"):
            raise HTTPException(status_code=400, detail="ID ya existe")
    usuarios.append(usuario)
    return usuario

@app.put('/usuarios/', response_model=modeloUsuario, tags=['Operaciones CRUD'])
def actualizarUsuario(usuarioActualizado: modeloUsuario):
    for index,usr in enumerate(usuarios):
        if usr["id"]==usuarioActualizado.id:
            usuarios[index]=usuarioActualizado.model_dump()
            return usuarios[index]
    raise HTTPException(status_code=404, detail="Usuario no existe")

@app.delete('/eliminarusuario/{id}', tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    for usr in usuarios:
        if usr["id"]==id:
            usuarios.remove(usr)
            return {"Usuario eliminado con éxito"}
    raise HTTPException(status_code=404, detail="Usuario no existe")
