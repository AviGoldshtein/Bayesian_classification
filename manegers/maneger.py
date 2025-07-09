from utiles.extract_keys import Extract_keys
from utiles.cleaner import Cleaner
from models.naive_bayes import Naive_bayes
from models.classifier import Classifier
from dal.dal import Dal
from ui.menu import Menu

class Manager:
    def __init__(self):
        self.model = None
        self.suggestions = None

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
                    Classifier.ask_a_question(self.model, chosen_params)
                else:
                    print("Choose first a file to work with\n")
            elif choice == "1000":
                print("have a good day")
                running = False
            else:
                print("invalid choice")

    def raw_df_handler(self, raw_df):
        cleaned_data = Cleaner.clean_data(raw_df)
        self.suggestions = Extract_keys.extract(cleaned_data)
        trained_model = Naive_bayes.train_model(cleaned_data)
        self.model = trained_model