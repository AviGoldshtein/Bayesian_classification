from logics_classification.models.classifier import Classifier
import requests

class Controller:
    def __init__(self):
        self._model = None
        self._accuracy = None
        self._features_and_unique_keys = None

    def get_features_and_unique_keys(self):
        if self._model:
            return {"exists": True, "features_and_unique_keys": self._features_and_unique_keys}
        else:
            return {"exists": False}

    def sync_model_from_main_server(self):
        try:
            # response = requests.get("http://baesyan_server_con:8000/model_metadata")  # for docker
            response = requests.get("http://127.0.0.1:8000/model_metadata")
            if response.ok:
                content = response.json()
                if content['exists']:
                    features_and_unique_keys = content['features_and_unique_keys']
                    trained_model = content['trained_model']
                    accuracy = content['accuracy']

                    self._features_and_unique_keys = features_and_unique_keys
                    self._model = trained_model
                    self._accuracy = accuracy
                    print("synced successfully with main server.")
        except Exception as e:
            print("There was a error with the server.")
            print(f"Error: {e}.")

    def classify(self, params_and_values: dict[str, str]) -> dict:
        return {
            "classification": Classifier.predict(self._model, params_and_values),
            "accuracy": self._accuracy
        }