class Extract_keys:
    @staticmethod
    def extract_labels_and_unique_keys(df):
        labels_and_unique_keys = {}
        for column in df.columns[:-1]:
            unique_keys = df[column].unique()
            labels_and_unique_keys[column] = unique_keys
        return labels_and_unique_keys

    @staticmethod
    def get_columns_list(df):
        return list(df.columns)