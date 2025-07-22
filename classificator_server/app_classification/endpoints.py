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

@router.get("/update_storage")
def update_storage():
    controller.update_storage()

@router.post("/classify")
def classification(params_and_values: dict[str, str]) -> dict:
    return controller.classify(params_and_values)