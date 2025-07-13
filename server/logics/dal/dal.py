import os
import pandas as pd

class Dal:
    @staticmethod
    def load_data(file):
        path = f"data/{file}"
        df = pd.read_csv(path)
        return df
    @staticmethod
    def get_list_files():
        return os.listdir("data")
