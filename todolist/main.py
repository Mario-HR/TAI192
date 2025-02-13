from fastapi import FastAPI, HTTPException

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='API de Gestión de Tareas (To-Do List)',
    description='Mario Alberto Hernandez Rodarte',
    version='1.0'
)

tareas=[
    {
        "id": 1,
        "titulo": "Estudiar para el examen",
        "descripcion": "Repasar los apuntes de TAI ",
        "vencimiento": "14-02-24",
        "estado": "completada"
    }
]

#Endpoint para obtener todas las tareas
@app.get('/tareas', tags=['Consulta de tareas'])
def leer_tareas():
    return {"Tareas": tareas}

#Endpoint para obtener una tarea especifica por su ID
@app.get('/tarea/{id}', tags=['Consulta de tarea específica'])
def leer_tarea(id: int):
    for tarea in tareas:
        if tarea["id"]==id:
            return tarea
    raise HTTPException(status_code=404, detail=f"No se ha encontrado la tarea con ID {id}")

#Endpoint para agregar una nueva tarea
@app.post('/agregartarea/', tags=['Agregar tarea'])
def agregar_tarea(tarea:dict):
    for t in tareas:
        if t["id"]==tarea.get("id"):
            raise HTTPException(status_code=400, detail="ID ya existe")
    tareas.append(tarea)
    return tarea

#Endpoint para actualizar una tarea existente
@app.put('/actualizartarea/', tags=['Actualizar tarea'])
def actualizar_tarea(tarea: dict):
    for t in tareas:
        if t["id"]==tarea.get("id"):
            tareas[tareas.index(t)]=tarea
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

#Endpoint para eliminar una tarea
@app.delete('/eliminartarea/{id}', tags=['Eliminar tarea'])
def eliminar_tarea(id: int):
    for t in tareas:
        if t["id"]==id:
            tareas.remove(t)
            return {"message": "Tarea eliminada con éxito"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")