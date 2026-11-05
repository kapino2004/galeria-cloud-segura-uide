from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Optional

app = FastAPI(title="API de Streaming de Video")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_private_network_header(request, call_next):
    if request.method == "OPTIONS":
        response = await call_next(request)
        response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response
    response = await call_next(request)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    categoria: str
    url_video: str  
    url_miniatura: str

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    texto: str
    video_id: Optional[int] = Field(default=None, foreign_key="video.id")



@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"mensaje": "¡El backend está funcionando!"}


def get_session():
    with Session(engine) as session:
        yield session

@app.post("/videos/")
def crear_video(video: Video, session: Session = Depends(get_session)):
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

@app.get("/videos/", response_model=List[Video])
def obtener_videos(session: Session = Depends(get_session)):
    videos = session.exec(select(Video)).all()
    return videos


from fastapi import HTTPException
import random


@app.get("/videos/{video_id}", response_model=Video)
def obtener_video(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return video

@app.get("/videos/{video_id}/recommendations", response_model=List[Video])
def obtener_recomendaciones(video_id: int, session: Session = Depends(get_session)):
    video_actual = session.get(Video, video_id)
    if not video_actual:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    
    videos_misma_categoria = session.exec(
        select(Video).where(Video.categoria == video_actual.categoria).where(Video.id != video_id)
    ).all()
    
    if len(videos_misma_categoria) <= 10:
        return videos_misma_categoria
    else:
        return random.sample(videos_misma_categoria, 10)

@app.post("/videos/{video_id}/comments")
def crear_comentario(video_id: int, comentario: Comment, session: Session = Depends(get_session)):
    
    comentario.video_id = video_id
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario

@app.get("/videos/{video_id}/comments", response_model=List[Comment])
def obtener_comentarios(video_id: int, session: Session = Depends(get_session)):
    comentarios = session.exec(select(Comment).where(Comment.video_id == video_id)).all()
    return comentarios


@app.delete("/videos/{video_id}")
def eliminar_video(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    session.delete(video)
    session.commit()
    return {"mensaje": "Video eliminado correctamente"}