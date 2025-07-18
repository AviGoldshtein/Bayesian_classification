from fastapi import APIRouter
from server.logics.dal.dal import Dal
from server.logics.models.naive_bayes import Naive_bayes
from server.logics.utiles.servise import convert_numpy_types
from server.logics.tests.test import Tester
import pandas as pd
from typing import List, Dict, Any

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
    json_data = df.to_dict(orient="records")
    return {"df": json_data}

@router.post("/train_model")
def train_model(data: List[Dict[str, Any]]) -> dict:
    train_df = pd.DataFrame(data)
    statistics = Naive_bayes.train_model(train_df)
    statistics = convert_numpy_types(statistics)
    return statistics

@router.post("/check_accuracy")
def check_accuracy(data: Dict[str, Any]) -> dict:
    trained_model = data['trained_model']
    test_df = data['test_df']
    accuracy = Tester.check_accuracy(trained_model, pd.DataFrame(test_df))
    return {"accuracy": accuracy}