from fastapi import FastAPI
from .server_endpoints import router
from .error_handler import add_exception_handlers

app = FastAPI()

add_exception_handlers(app)

app.include_router(router)
