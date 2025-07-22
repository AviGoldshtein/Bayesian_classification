from logics.services.data_service import DataService
from logics.services.model_service import ModelService

from logics.store import Store
from fastapi import APIRouter
from pydantic import BaseModel

class DropColumnsRequest(BaseModel):
    columns_to_drop: list[str]

store = Store()
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
    DataService.load_and_store_file(store, chosen_file)
    return {"status": "success"}

@router.get("/get_columns_list")
def get_columns_list() -> dict:
    return {"columns_to_delete": DataService.get_columns_list(store)}

@router.post("/drop_requested_columns")
def drop_requested_columns(data: DropColumnsRequest) -> dict:
    DataService.drop_columns(store, data.columns_to_drop)
    return {"status": "success"}

@router.get("/raw_df_handler")
def raw_df_handler() -> dict:
    DataService.prepare_data_for_training(store)
    accuracy = ModelService.train_model(store)
    return {"accuracy": accuracy}

@router.get("/get_features_and_unique_keys")
def get_features_and_unique_keys() -> dict:
    return ModelService.get_model_metadata(store)

@router.post("/classify")
def classify(params_and_values: dict[str, str]) -> dict:
    return ModelService.classify(store, params_and_values)