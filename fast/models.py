from pydantic import BaseModel, Field

#Modelo de validaciones
class modeloUsuario(BaseModel):
    id:int = Field(...,gt=0,description="ID unico y solo numeros positivos")
    nombre:str = Field(...,min_length=3,max_length=85,description="Solo letras: min 3 max 85", example="max")
    edad: int = Field(...,gt=0,lt=121,description="Solo numeros positivos")
    email: str = Field(...,pattern="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", description="Solo direcciones de correo electronico validas",example="correo@example.com")
