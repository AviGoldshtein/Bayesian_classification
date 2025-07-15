class Naive_bayes:

    @staticmethod
    def train_model(df) -> dict:
        """
        Trains a frequency-based model from a DataFrame.

        The model returns a nested dictionary:
        - Top-level keys: unique values from the target column (last column of the DataFrame).
        - Each target value maps to a dictionary:
            - Keys: feature column names.
            - Each maps to another dictionary:
                - Keys: unique values in that column.
                - Values: the smoothed conditional frequency of that feature value given the target value.

        Smoothing: Laplace smoothing (add-1).

        :param df: Input DataFrame. The last column is assumed to be the target.
        :return: Nested dictionary with frequency-based statistics.
        """
        copy_df = df.copy()

        trained_by = df.columns[-1]

        column_trained_by = df[trained_by]
        df.drop(inplace=True, columns=[trained_by])

        statistics = {"sum": {"total_cases": len(copy_df.index)}}
        for target_value in column_trained_by.unique():
            statistics['sum'][target_value] = (copy_df[trained_by] == target_value).sum()
            statistics[target_value] = {}
            for column in df.columns:
                statistics[target_value][column] = {}
                unique_keys_in_column = df[column].unique()
                for unique_key in unique_keys_in_column:
                    num_of_matched_rows = ((copy_df[column] == unique_key) & (copy_df[trained_by] == target_value)).sum() + 1
                    num_of_target_value = statistics['sum'][target_value] + len(unique_keys_in_column)
                    statistics[target_value][column][unique_key] = num_of_matched_rows / num_of_target_value
        return statistics