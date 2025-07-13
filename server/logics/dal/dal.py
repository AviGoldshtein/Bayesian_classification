import os
import pandas as pd

class Dal:
    @staticmethod
    def load_data(file: str) -> pd.DataFrame:
        """
        Loads a CSV file from the 'data' directory into a pandas DataFrame.

        :param file: Name of the CSV file (e.g., 'mydata.csv').
        :return: pandas DataFrame with the contents of the file.
        """
        path = f"data/{file}"
        df = pd.read_csv(path)
        return df
    @staticmethod
    def get_list_files() -> list[str]:
        """
        Returns a list of CSV file names in the 'data' directory.
        :return: A list of file names ending with .csv
        """
        return os.listdir("data")
