from sklearn.model_selection import train_test_split
from client.utiles.extract_keys import Extract_keys
from client.utiles.cleaner import Cleaner
from server.logics.models.classifier import Classifier
from client.ui.menu import Menu
import requests
import pandas as pd

class Manager:
    def __init__(self):
        self.URL = "http://127.0.0.1:8000/"
        self.model = None
        self.labels_and_unique_keys = None
        self.accuracy = None

    def run(self):
        running = True
        while running:
            choice = Menu.show_menu()
            if choice == "1":
                list_of_files = requests.get(self.URL + "get_files_list").json()['files_list']
                chosen_file = Menu.suggest_options(list_of_files)
                raw_df_list_of_dicts = requests.get(f"{self.URL}/load_data/{chosen_file}").json()['df']
                raw_df = pd.DataFrame(raw_df_list_of_dicts)
                self.raw_df_handler(raw_df)
            elif choice == "2":
                url = input("Enter a link or URL")
                # raw_df = Dal.load_data(url)
                # self.raw_df_handler(raw_df)
                print("Currently under renovations")
            elif choice == "3":
                if self.model:
                    chosen_params_and_values = Menu.choose_params_and_values(self.labels_and_unique_keys)
                    print(f"the answer is:  {Classifier.ask_a_question(self.model, chosen_params_and_values)}.\n"
                          f"but take care, because the accuracy is: {self.accuracy}.%\n")
                else:
                    print("Choose first a file to work with\n")
            elif choice == "1000":
                print("have a good day")
                running = False
            else:
                print("invalid choice")

    def raw_df_handler(self, raw_df):
        raw_df = self.suggest_deleting_columns(raw_df)
        cleaned_df = Cleaner.ensure_there_is_no_nan(raw_df)
        self.labels_and_unique_keys = Extract_keys.extract_labels_and_unique_keys(cleaned_df)
        train_df, test_df = train_test_split(cleaned_df, test_size=0.3)
        response = requests.post(f"{self.URL}train_model", json=train_df.to_dict(orient="records"))
        if response.ok:
            self.model = response.json()
            response = requests.post(f"{self.URL}check_accuracy", json={"trained_model": self.model, "test_df": test_df.to_dict(orient="records")})
            self.accuracy = response.json()['accuracy']
            print(f'The testing is over. Accuracy of {self.accuracy} %')
        else:
            print("There was a problem loading the file.")

    def suggest_deleting_columns(self, df):
        choice = input("1. to delete any column of the table before training\n"
                       "2. to continue to training")
        if choice == "1":
            columns_to_delete = []
            list_of_columns = Extract_keys.get_columns_list(df)[:-1]
            while len(list_of_columns) > 0:
                chosen_column = Menu.suggest_options(list_of_columns)
                columns_to_delete.append(chosen_column)
                list_of_columns.remove(chosen_column)
                done = input("write 'done' to execute, any other key to continue inserting")
                if done == "done":
                    break
            print("executing..")
            cleaned_df = Cleaner.drop_requested_columns(df, columns_to_delete)
        elif choice == "2":
            print("Here we go")
            return df
        else:
            print("invalid input")
            return self.suggest_deleting_columns(df)
        return cleaned_df