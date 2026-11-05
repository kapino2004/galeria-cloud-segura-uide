# Galería Cloud Segura - Plataforma de Streaming 
## Arquitectura del Proyecto
* **Frontend:** Construido con HTML, CSS y Js. Implementado como un sitio web estático en **AWS S3**.
* **Backend:** Desarrollado con **FastAPI** (Python) e integración de CORS para Private Network Access.
* **Base de Datos:** SQLite (`database.db`).

## Enlace de Producción (AWS S3)
**[https://streaming-galeria-segura-2026.s3.us-east-1.amazonaws.com/index.html]**

## Instrucciones
Dado que el frontend alojado en la nube consume los datos de la API local, hay levantar el servidor backend antes de abrir el enlace de AWS.

1. Descargar este repositorio y abrir la carpeta en la terminal.
2. Instalar las dependencias necesarias:
   ```bash
   pip install fastapi uvicorn sqlmodel

3. Ejecutamos el server local:
   python -m uvicorn main:app --reload

4. Una vez que la terminal indique Application startup complete, abrir el enlace de AWS S3 en el navegador.
