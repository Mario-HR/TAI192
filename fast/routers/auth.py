from fastapi.responses import JSONResponse
from pydanticModels import modeloAutentificacion
from genToken import createToken
from fastapi import APIRouter

routerAuth = APIRouter()

#Endpoint de autenticacion
@routerAuth.post('/auth', tags=['Autentificacion'])
def login(autorizacion:modeloAutentificacion):
    if autorizacion.email == "mario@example.com" and autorizacion.passwd == "12345678":
        token:str=createToken(autorizacion.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return("Aviso: Usuario sin aurorización")