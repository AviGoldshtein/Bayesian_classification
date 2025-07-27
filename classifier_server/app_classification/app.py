from fastapi import FastAPI
from .classifier_endpoints import router

app = FastAPI()

app.include_router(router)
