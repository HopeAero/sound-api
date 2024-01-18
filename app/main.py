from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile
from .config.config import settings
from .routers.works import works as works_router
from .routers.authors import authors as authors_router
from .routers.publications import publications as publications_router
from .routers.multimedia import sounds as multimedia_router
from app.models import authors, multimedia, works, publications
from .db.session import engine, Base, SessionLocal
from fastapi.middleware.cors import CORSMiddleware


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    Base.metadata.create_all(bind=engine)
    return app


app = start_application()

app.include_router(works_router)
app.include_router(authors_router)
app.include_router(publications_router)
app.include_router(multimedia_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"msg":"Hello FastAPI🚀"}
