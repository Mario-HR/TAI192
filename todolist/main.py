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