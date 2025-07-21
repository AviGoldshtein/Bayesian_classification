class Cleaner:
    @staticmethod
    def ensure_there_is_no_nan(df):
        """
        Ensures there are no NaN values in the DataFrame by cleaning it.

        :param df: Raw (non-cleaned) pandas DataFrame.
        :return: Cleaned DataFrame.
        """
        df = Cleaner.drop_columns_with_nan_above_threshold(df, threshold=0.6)
        df = Cleaner.drop_empty_rows(df)
        return df

    @staticmethod
    def drop_empty_rows(df):
        """
        Drop all rows containing at least one NaN.
        Does not modify the original DataFrame.

        :param df: Raw (non-cleaned) pandas DataFrame.
        :return: A new cleaned DataFrame.
        """
        return df.dropna(axis=0).copy()

    @staticmethod
    def drop_columns_with_nan_above_threshold(df, threshold=0.6):
        """
        Drop columns from the DataFrame if the percentage of NaNs in a column exceeds the given threshold.

        :param df: Raw (non-cleaned) pandas DataFrame.
        :param threshold: Float between 0 and 1, representing max allowed NaN ratio per column.
        :return: A new cleaned DataFrame with selected columns dropped.
        """
        num_of_rows = len(df)
        columns_to_drop = [
            column for column in df.columns
            if df[column].isna().sum() / num_of_rows > threshold
        ]
        return df.drop(columns=columns_to_drop).copy()

    @staticmethod
    def drop_requested_columns(df, requested_columns):
        """
        Drop requested columns from a DataFrame.
        :param df: row DataFrame.
        :param requested_columns: a list of selected columns to drop.
        :return: a new cleaned DataFrame.
        """
        return df.drop(columns=requested_columns).copy()