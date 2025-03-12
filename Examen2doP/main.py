from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field

app=FastAPI(
    title="API de conductores",
    description="Mario Alberto Hernandez Rodarte",
    version="1.0"
)

#Modelo de conductores
class ModeloConductor(BaseModel):
    nombre:str=Field(..., min_length=3)
    tipoLicencia:str=Field(...,pattern=r"^[A-D]$",min_length=1,max_length=1)
    noLicencia:str=Field(...,min_length=12,max_length=12)

#Base de datos de conductores
conductores=[
    {"nombre": "Juan Perez", "tipoLicencia": "A", "noLicencia": "B8D7X4R82BO9"},
    {"nombre": "Ana Lopez", "tipoLicencia": "C", "noLicencia": "XJFCI7378XUY"}
]

#Endpoint para consultar todos los conductores
@app.get("/todosconductores")
def consultarConductores():
    return conductores

#Endpoint para consultar un conductor
@app.get("/conductor/{lic}")
def consultarConductor(lic:str):
    for conductor in conductores:
        if conductor["noLicencia"]==lic:
            return conductor
    raise HTTPException(status_code=404, detail=f"No existe el conductar con licencia {lic}.")


#Endpoint para agregar un conductor
@app.post("/agregarconductor/")
def agregarConductor(conductor:ModeloConductor):
    for cond in conductores:
        if cond["noLicencia"]==conductor.noLicencia:
            raise HTTPException(status_code=400, detail=f"Ya existe un conductor con el codigo de licencia {conductor.get("noLicencia")}.")
    conductores.append(conductor)
    return conductor

#Endpoint para editar un conductor
@app.put("/modificarconductor/")
def modificarConductor(conductor:ModeloConductor):
    for index,cond in enumerate(conductores):
        if cond["noLicencia"]==conductor.noLicencia:
            conductores[index]=conductor.model_dump()
            return conductores[index]
    raise HTTPException(status_code=404, detail="No existe el conductor con esa licencia.")

#Endpoint para eliminar un conductor
@app.delete("/eliminarconductor/{lic}")
def eliminarConductor(lic:str):
    for conductor in conductores:
        if conductor["noLicencia"]==lic:
            conductores.remove(conductor)
            return {"Conductor eliminado."}
    raise HTTPException(status_code=404, detail=f"No existe el conductar con licencia {lic}.")