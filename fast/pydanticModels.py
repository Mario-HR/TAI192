from pydantic import BaseModel, Field, EmailStr

#Modelo de validaciones
class modeloUsuario(BaseModel):
    name:str = Field(...,min_length=3,max_length=85,description="Solo letras: min 3 max 85", example="max")
    age:int = Field(...,gt=0,lt=121,description="Solo numeros positivos")
    email:EmailStr = Field(..., description="Solo direcciones de correo electronico validas",example="correo@example.com")

class modeloAutentificacion(BaseModel):
    email:EmailStr = Field(..., description="Solo direcciones de correo electronico validas",example="correo@example.com")
    passwd:str = Field(...,min_length=8,strip_whitespace=True,description="Contraseña minimo 8 caracteres")