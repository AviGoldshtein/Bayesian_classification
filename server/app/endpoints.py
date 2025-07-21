from sklearn.model_selection import train_test_split
from server.logics.models.naive_bayes import Naive_bayes
from server.logics.models.classifier import Classifier
from server.logics.utils.service import convert_numpy_types
from server.logics.utils.extract_keys import Extract_keys
from server.logics.utils.cleaner import Cleaner
from server.logics.tests.test import Tester
from server.logics.dal.dal import Dal
from server.logics.store import Store
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
    return {"files_list": Dal.get_list_files()}

@router.get("/load_data/{chosen_file}")
def load_data(chosen_file) -> dict:
    df = Dal.load_data(chosen_file)
    store.pending_data = df
    return {"status": "success"}

@router.get("/get_columns_list")
def get_columns_list() -> dict:
    return {"columns_to_delete": Extract_keys.get_column_names(store.pending_data)[:-1]}

@router.post("/drop_requested_columns")
def drop_requested_columns(data: DropColumnsRequest) -> dict:
    store.pending_data = Cleaner.drop_requested_columns(store.pending_data, data.columns_to_drop)
    return {"status": "success"}

@router.get("/raw_df_handler")
def raw_df_handler() -> dict:
    store.pending_data = Cleaner.ensure_there_is_no_nan(store.pending_data)
    store.features_and_unique_keys = Extract_keys.extract_features_and_unique_keys(store.pending_data)
    train_df, test_df = train_test_split(store.pending_data, test_size=0.3)
    store.model = Naive_bayes.train_model(train_df)
    store.accuracy = Tester.check_accuracy(store.model, test_df)
    return {"accuracy": store.accuracy}

@router.get("/get_features_and_unique_keys")
def get_features_and_unique_keys() -> dict:
    if store.model:
        return {"model": True, "features_and_unique_keys": convert_numpy_types(store.features_and_unique_keys)}
    else:
        return {"model": False}

@router.post("/classify")
def classify(test_dict: dict[str, str]) -> dict:
    return {"classification": Classifier.ask_a_question(store.model, test_dict), "accuracy": store.accuracy}