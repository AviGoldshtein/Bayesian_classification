class Extract_keys:
    @staticmethod
    def extract_features_and_unique_keys(df):
        """
        Extracts unique values for each feature column (excluding the target).

        :param df: Input pandas DataFrame.
        :return: A dictionary where keys are column names and values are lists of unique (non-NaN) values.
        """
        features_and_unique_keys = {}
        for column in df.columns[:-1]:
            unique_keys = df[column].unique()
            features_and_unique_keys[column] = unique_keys
        return features_and_unique_keys

    @staticmethod
    def get_column_names(df):
        """
        Returns the column names of the given DataFrame.

        :param df: Input pandas DataFrame.
        :return: A list of column names as strings.
        """
        return list(df.columns)
