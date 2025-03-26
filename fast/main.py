from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional,List
from pydanticModels import modeloUsuario, modeloAutentificacion
from genToken import createToken
from middleware import BearerJWT
from db.connection import Session,engine,Base
from models.modelsDb import User

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
@app.get('/todosusuarios', dependencies={Depends(BearerJWT())}, response_model=List[modeloUsuario], tags=['Operaciones CRUD'])
def leerUsuarios():
    db=Session()
    try:
        consultauno=db.query(User).all()
        if not consultauno:
            return JSONResponse(content={"message": "Usuuario no encontrado"})
        return JSONResponse(content=jsonable_encoder(consultauno))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar", "Exception": str(e)})
    finally:
        db.close()

#Endpoint buscar por ID
@app.get('/usuario/{id}', tags=['Operaciones CRUD'])
def buscarUno(id:int):
    db=Session()
    try:
        consulta=db.query(User).filter(User.id==id).first()
        if consulta:
            return JSONResponse(content=jsonable_encoder(consulta))
        else:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar usuario", "Exception": str(e)})
    finally:
        db.close()

@app.post('/usuario/', response_model=modeloUsuario, tags=['Operaciones CRUD'])
def agregarUsuario(usuario:modeloUsuario):
    db=Session()
    try:
        db.add(User(**usuario.model_dump()))
        db.commit()
        return JSONResponse(status_code=201,content={"mesage":"Usuario guardado","usuario": usuario.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,content={"message": "Error al guardar usuario", "Exception": str(e)})
    finally:
        db.close()

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
