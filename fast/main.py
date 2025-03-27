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
@app.get('/todosusuarios', response_model=List[modeloUsuario], tags=['Operaciones CRUD'])
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
@app.get('/usuario/{id}', response_model=modeloUsuario, tags=['Operaciones CRUD'])
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

#Endpoint para agregar usuario
@app.post('/agregarusuario/', response_model=modeloUsuario, tags=['Operaciones CRUD'])
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

#Endpoint para actualizar usuario
@app.put('/actualizarusuario/{id}', response_model=modeloUsuario, tags=['Operaciones CRUD'])
def actualizarUsuario(id:int,usuarioActualizado: modeloUsuario):
    db=Session()
    try:
        usuario=db.query(User).filter(User.id==id).first()
        if usuario:
            usuario.name=usuarioActualizado.name
            usuario.age=usuarioActualizado.age
            usuario.email=usuarioActualizado.email
            db.commit()
            return JSONResponse(status_code=200, content={"message":"Usuario actualizado con éxito","usuario": usuarioActualizado.model_dump()})
        else:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar usuario", "Exception": str(e)})
    finally:
        db.close()

@app.delete('/eliminarusuario/{id}', tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    db=Session()
    try:
        usuario=db.query(User).filter(User.id==id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return JSONResponse(status_code=200, content={"message":"Usuario eliminado con éxito"})
        else:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar usuario", "Exception": str(e)})
    finally:
        db.close()