import pandas as pd

class Cleaner:
    @staticmethod
    def ensure_there_is_no_nan(df):
        Cleaner.drop_columns_with_nan_above_threshold(df, threshold=0.6)
        Cleaner.drop_empty_rows(df)
        return df

    @staticmethod
    def drop_empty_rows(df):
        df.dropna(axis=0, inplace=True)

    @staticmethod
    def drop_columns_with_nan_above_threshold(df, threshold=0.6):
        num_of_rows = len(df.index)
        columns_to_drop = []
        for column in df.columns:
            num_of_nans = df[column].isna().sum()
            percentage_of_nans = num_of_nans / num_of_rows
            if percentage_of_nans > threshold:
                columns_to_drop.append(column)
        df.drop(columns=columns_to_drop, inplace=True)

    @staticmethod
    def drop_requested_columns(df, requested_columns):
        df.drop(columns=requested_columns, inplace=True)