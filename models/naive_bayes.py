class Naive_bayes:

    @staticmethod
    def train_model(df):
        copy_df = df.copy()

        trained_by = df.columns[-1]

        df.sort_values(trained_by, inplace=True)
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
                    statistics[target_value][column][unique_key] = (((copy_df[column] == unique_key) & (copy_df[trained_by] == target_value)).sum() + 1) / (statistics['sum'][target_value] + len(unique_keys_in_column))
        return statistics