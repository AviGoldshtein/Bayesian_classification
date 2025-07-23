from sklearn.model_selection import train_test_split
from logics.utils.service import convert_numpy_types
from logics.models.classifier import Classifier
from logics.models.naive_bayes import Naive_bayes
from logics.tests.test import Tester

class ModelService:
    @staticmethod
    def get_model_metadata(store):
        if store.model:
            return {"exists": True,
                    "features_and_unique_keys": convert_numpy_types(store.features_and_unique_keys),
                    "trained_model": convert_numpy_types(store.model),
                    "accuracy": store.accuracy
            }
        else:
            return {"exists": False}

    @staticmethod
    def classify(store, params_and_values):
        return {
            "classification": Classifier.ask_a_question(store.model, params_and_values),
            "accuracy": store.accuracy
        }

    @staticmethod
    def train_model(store):
        train_df, test_df = train_test_split(store.pending_data, test_size=0.3)
        store.model = Naive_bayes.train_model(train_df)
        store.accuracy = Tester.check_accuracy(store.model, test_df)
        return store.accuracy