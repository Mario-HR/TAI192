from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from pydanticModels import modeloUsuario
from middleware import BearerJWT
from db.connection import Session
from models.modelsDb import User
from fastapi import APIRouter

routerUsuarios = APIRouter()

#Endpoint consulta todos
@routerUsuarios.get('/todosusuarios', dependencies={Depends(BearerJWT())}, response_model=List[modeloUsuario], tags=['Operaciones CRUD'])
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
@routerUsuarios.get('/usuario/{id}', response_model=modeloUsuario, tags=['Operaciones CRUD'])
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
@routerUsuarios.post('/agregarusuario/', response_model=modeloUsuario, tags=['Operaciones CRUD'])
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
@routerUsuarios.put('/actualizarusuario/{id}', response_model=modeloUsuario, tags=['Operaciones CRUD'])
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

@routerUsuarios.delete('/eliminarusuario/{id}', tags=['Operaciones CRUD'])
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