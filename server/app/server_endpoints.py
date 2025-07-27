from fastapi import APIRouter
from pydantic import BaseModel
from logics.controller import Controller

class DropColumnsRequest(BaseModel):
    columns_to_drop: list[str]

router = APIRouter()
controller = Controller()

@router.get("/")
def health() -> dict:
    return {"message": "working"}

@router.get("/files_list")
def get_files_list() -> dict:
    return {"files_list": controller.get_list_files()}

@router.get("/load_data/{file_name}")
def load_data(file_name: str) -> dict:
    controller.load_and_store_file(file_name)
    return {"status": "success"}

@router.get("/deletable_columns")
def get_deletable_columns() -> dict:
    return {"deletable_columns": controller.get_deletable_columns()}

@router.post("/drop_columns")
def drop_requested_columns(data: DropColumnsRequest) -> dict:
    controller.drop_columns(data.columns_to_drop)
    return {"status": "success"}

@router.get("/clean_and_train_model")
def clean_and_train() -> dict:
    accuracy = controller.clean_and_train_model()
    return {"accuracy": accuracy}

@router.get("/model_metadata")
def get_model_metadata() -> dict:
    return controller.get_model_metadata()