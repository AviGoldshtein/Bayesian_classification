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

@router.get("/get_files_list")
def get_files_list() -> dict:
    return {"files_list": controller.get_list_files()}

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file) -> dict:
    controller.load_and_store_file(chosen_file)
    return {"status": "success"}

@router.get("/get_columns_list")
def get_columns_list() -> dict:
    return {"columns_to_delete": controller.get_columns_list()}

@router.post("/drop_requested_columns")
def drop_requested_columns(data: DropColumnsRequest) -> dict:
    controller.drop_columns(data.columns_to_drop)
    return {"status": "success"}

@router.get("/clean_and_train_model")
def raw_df_handler() -> dict:
    accuracy = controller.clean_and_train_model()
    return {"accuracy": accuracy}

@router.get("/get_model_metadata")
def get_features_and_unique_keys_and_model() -> dict:
    return controller.get_model_metadata()