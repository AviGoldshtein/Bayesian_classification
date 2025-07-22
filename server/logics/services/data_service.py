from logics.utils.cleaner import Cleaner
from logics.utils.extract_keys import Extract_keys
from logics.dal.dal import Dal

class DataService:
    @staticmethod
    def get_list_files():
        return Dal.get_list_files()

    @staticmethod
    def load_and_store_file(store, filename):
        df = Dal.load_data(filename)
        store.pending_data = df

    @staticmethod
    def get_columns_list(store):
        return Extract_keys.get_column_names(store.pending_data)[:-1]

    @staticmethod
    def drop_columns(store, columns):
        store.pending_data = Cleaner.drop_requested_columns(store.pending_data, columns)

    @staticmethod
    def prepare_data_for_training(store):
        store.pending_data = Cleaner.ensure_there_is_no_nan(store.pending_data)
        store.features_and_unique_keys = Extract_keys.extract_features_and_unique_keys(store.pending_data)