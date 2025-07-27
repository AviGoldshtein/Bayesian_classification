from sklearn.model_selection import train_test_split
from logics.utils.service import convert_numpy_types
from logics.dal.dal import Dal
from logics.utils.extract_keys import Extract_keys
from logics.utils.cleaner import Cleaner
from logics.models.naive_bayes import Naive_bayes
from logics.tests.test import Tester

class Controller:
    def __init__(self):
        self._model = None
        self._accuracy = None
        self._pending_data = None
        self._features_and_unique_keys = None

    def get_list_files(self):
        return Dal.get_list_files()

    def load_and_store_file(self, filename):
        df = Dal.load_data(filename)
        self._pending_data = df

    def get_columns_list(self):
        return Extract_keys.get_column_names(self._pending_data)[:-1]

    def drop_columns(self, columns_to_drop):
        self._pending_data = Cleaner.drop_requested_columns(self._pending_data, columns_to_drop)

    def clean_and_train_model(self):
        self._pending_data = Cleaner.ensure_there_is_no_nan(self._pending_data)
        self._features_and_unique_keys = Extract_keys.extract_features_and_unique_keys(self._pending_data)
        train_df, test_df = train_test_split(self._pending_data, test_size=0.3)
        self._model = Naive_bayes.train_model(train_df)
        self._accuracy = Tester.check_accuracy(self._model, test_df)
        return self._accuracy

    def get_model_metadata(self):
        if self._model:
            return {"exists": True,
                    "features_and_unique_keys": convert_numpy_types(self._features_and_unique_keys),
                    "trained_model": convert_numpy_types(self._model),
                    "accuracy": self._accuracy
            }
        else:
            return {"exists": False}