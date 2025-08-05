from utiles.http_helpers import handle_response
from ui.menu import Menu
import requests

class Manager:
    def __init__(self):
        # self.trainer_URL = "http://baesyan_server_con:8000/"  # for docker
        # self.classifier_URL = "http://classification_server_con:8001/"  # for docker

        self.trainer_URL = "http://127.0.0.1:8000/"
        self.classifier_URL = "http://127.0.0.1:8001/"

    def run(self):
        running = True
        while running:
            choice = Menu.show_menu()
            if choice == "1":
                self.handel_file_choice()
            elif choice == "2":
                self.handel_url_choice()
            elif choice == "3":
                self.handel_classification()
            elif choice == "1000":
                print("have a good day")
                running = False
            else:
                print("invalid choice")

    def handel_file_choice(self):
        try:
            response = requests.get(self.trainer_URL + "files_list")
            content = handle_response(response, failure_msg="There was a problem getting the files list.")
            if content:
                list_of_files = content['files_list']
                chosen_file = Menu.suggest_options(list_of_files)
                response = requests.get(f"{self.trainer_URL}/load_data/{chosen_file}")
                content = handle_response(response,success_msg=f"The file '{chosen_file}' loaded successfully." ,failure_msg="There was a problem loading the file.")
                if content:
                    self.suggest_deleting_columns()
                    response = requests.get(f"{self.trainer_URL}clean_and_train_model")
                    content = handle_response(response, success_msg="The cleaning and training has succeeded", failure_msg="There was a problem while cleaning and training the model.")
                    if content:
                        accuracy = content['accuracy']
                        print(f'The testing is over. Accuracy of {accuracy} %')
                        response = requests.get(f"{self.classifier_URL}sync_model_from_main_server")
                        handle_response(response, failure_msg="There was a problem in syncing the model from the main server.")
        except Exception as e:
            print("There was a error with the server.")
            print(f"Error: {e}.")

    def handel_url_choice(self):
        url = input("Enter a link or URL")
        # raw_df = Dal.load_data(url)
        # self.raw_df_handler(raw_df)
        print("Currently under renovations")

    def handel_classification(self):
        try:
            response = requests.get(f"{self.classifier_URL}get_features_and_unique_keys")
            content = handle_response(response, failure_msg="There was a problem with the get_features_and_unique_keys")
            if content:
                if content['exists']:
                    features_and_unique_keys = content['features_and_unique_keys']
                    chosen_params_and_values = Menu.choose_params_and_values(features_and_unique_keys)
                    response = requests.post(f"{self.classifier_URL}classify", json=chosen_params_and_values)
                    content = handle_response(response, failure_msg="There was a problem with the classification")
                    if content:
                        print(f"the answer is:  {content['classification']}.\n"
                              f"The accuracy of this model is {content['accuracy']}%.")
                else:
                    print("Choose first a file to work with")
        except Exception as e:
            print("There was an error with the server.")
            print(f"Error: {e}.")

    def suggest_deleting_columns(self):
        choice = input("1. to delete any column of the table before training\n"
                       "2. to continue to training")
        if choice == "1":
            response = requests.get(f"{self.trainer_URL}deletable_columns")
            content = handle_response(response, failure_msg="there was a problem getting to the columns to delete")
            if content:
                columns_to_drop = []
                deletable_columns = content["deletable_columns"]
                while len(deletable_columns) > 0:
                    chosen_column = Menu.suggest_options(deletable_columns)
                    columns_to_drop.append(chosen_column)
                    deletable_columns.remove(chosen_column)
                    done = input("write 'done' to execute, any other key to continue inserting")
                    if done == "done":
                        break
                print("executing..")
                response = requests.post(f"{self.trainer_URL}drop_columns", json={"columns_to_drop": columns_to_drop})
                handle_response(response, success_msg="The requested columns has been dropped", failure_msg="There was a problem dropping the columns")
        elif choice == "2":
            print("Here we go")
        else:
            print("invalid input")
            self.suggest_deleting_columns()