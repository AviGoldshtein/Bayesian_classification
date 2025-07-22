from logics.services.data_service import DataService
from logics.services.model_service import ModelService

from logics.storage import Storage
from fastapi import APIRouter
from pydantic import BaseModel

class DropColumnsRequest(BaseModel):
    columns_to_drop: list[str]

storage = Storage()
router = APIRouter()

@router.get("/")
def health() -> dict:
    return {"message": "working"}

@router.get("/get_files_list")
def get_files_list() -> dict:
    files_list = DataService.get_list_files()
    return {"files_list": files_list}

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file) -> dict:
    DataService.load_and_store_file(storage, chosen_file)
    return {"status": "success"}

@router.get("/get_columns_list")
def get_columns_list() -> dict:
    return {"columns_to_delete": DataService.get_columns_list(storage)}

@router.post("/drop_requested_columns")
def drop_requested_columns(data: DropColumnsRequest) -> dict:
    DataService.drop_columns(storage, data.columns_to_drop)
    return {"status": "success"}

@router.get("/raw_df_handler")
def raw_df_handler() -> dict:
    DataService.prepare_data_for_training(storage)
    accuracy = ModelService.train_model(storage)
    return {"accuracy": accuracy}

@router.get("/get_model_metadata")
def get_features_and_unique_keys_and_model() -> dict:
    return ModelService.get_model_metadata(storage)

@router.post("/classify")
def classify(params_and_values: dict[str, str]) -> dict:
    return ModelService.classify(storage, params_and_values)