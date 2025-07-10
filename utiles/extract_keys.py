class Extract_keys:
    @staticmethod
    def extract(df):
        suggestions = {}
        for column in df.columns[:-1]:
            unique_list = df[column].unique()
            suggestions[column] = unique_list
        return suggestions

    @staticmethod
    def get_columns_list(df):
        return list(df.columns)