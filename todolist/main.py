from fastapi import FastAPI, HTTPException

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='API de Gestión de Tareas (To-Do List)',
    description='Mario Alberto Hernandez Rodarte',
    version='1.0'
)
