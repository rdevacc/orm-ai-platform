from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.embedding import router as embedding_router
from routes.classifier import router as classifier_router


app = FastAPI(
    title="Face Recognition API"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(
    embedding_router
)

app.include_router(
    classifier_router
)


@app.get("/")
def root():

    return {
        "message": "Face Recognition API Running"
    }