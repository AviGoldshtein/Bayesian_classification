from fastapi import APIRouter
from logics_classification.controller import Controller

router = APIRouter()
controller = Controller()

@router.get("/")
def health() -> dict:
    return {"message": "classifier_is_working"}

@router.get("/get_features_and_unique_keys")
def get_features_and_unique_keys():
    return controller.get_features_and_unique_keys()

@router.get("/sync_model_from_main_server")
def sync_model_from_main_server():
    controller.sync_model_from_main_server()
    return {"status": "success"}

@router.post("/classify")
def classification(features_and_values: dict) -> dict:
    return controller.classify(features_and_values)