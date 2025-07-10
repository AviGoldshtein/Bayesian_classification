from sklearn.model_selection import train_test_split
from utiles.extract_keys import Extract_keys
from utiles.cleaner import Cleaner
from models.naive_bayes import Naive_bayes
from models.classifier import Classifier
from tests.test import Tester
from dal.dal import Dal
from ui.menu import Menu

class Manager:
    def __init__(self):
        self.model = None
        self.suggestions = None
        self.accuracy = None

    def run(self):
        running = True
        while running:
            choice = Menu.show_menu()
            if choice == "1":
                chosen_file = Menu.suggest_options(Dal.get_list_files())
                raw_df = Dal.load_data("data/" + chosen_file)
                self.raw_df_handler(raw_df)
            elif choice == "2":
                url = input("Enter a link or URL")
                raw_df = Dal.load_data(url)
                self.raw_df_handler(raw_df)
            elif choice == "3":
                if self.model:
                    chosen_params = Menu.get_params(self.suggestions)
                    print(f"the answer is:  {Classifier.ask_a_question(self.model, chosen_params)}.\n"
                          f"but take care, because the accuracy is: {self.accuracy}.%\n")
                else:
                    print("Choose first a file to work with\n")
            elif choice == "1000":
                print("have a good day")
                running = False
            else:
                print("invalid choice")

    def raw_df_handler(self, raw_df):
        self.suggest_deleting_columns(raw_df)
        cleaned_df = Cleaner.ensure_there_is_no_nan(raw_df)
        self.suggestions = Extract_keys.extract(cleaned_df)
        train_df, test_df = train_test_split(cleaned_df, test_size=0.3)
        self.model = Naive_bayes.train_model(train_df)
        self.accuracy = Tester.check_accuracy(self.model, test_df)
        print(f'The testing is over. Accuracy of {self.accuracy} %')

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
            Cleaner.drop_requested_columns(df, columns_to_delete)
        elif choice == "2":
            print("Here we go")
        else:
            print("invalid input")
            self.suggest_deleting_columns(df)