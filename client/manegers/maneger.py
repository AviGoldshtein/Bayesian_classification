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
            response = requests.get(self.trainer_URL + "get_files_list")
            if response.ok:
                list_of_files = response.json()['files_list']
                chosen_file = Menu.suggest_options(list_of_files)
                response = requests.get(f"{self.trainer_URL}/load_data/{chosen_file}")
                if response.ok:
                    self.suggest_deleting_columns()
                    response = requests.get(f"{self.trainer_URL}clean_and_train_model")
                    if response.ok:
                        accuracy = response.json()['accuracy']
                        print(f'The testing is over. Accuracy of {accuracy} %')
                        response = requests.get(f"{self.classifier_URL}sync_model_from_main_server")
                        if not response.ok:
                            print("There was a problem in syncing the model from the main server.")
                            print(f"status code: {response.status_code}")
                    else:
                        print("There was a problem while cleaning and training the model.")
                        print(f"status code: {response.status_code}")
                else:
                    print("There was a problem loading the file.")
                    print(f"Status code: {response.status_code}")
            else:
                print("There was a problem getting the files list.")
                print(f"Status code: {response.status_code}")
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
            if response.ok:
                content = response.json()
                if content['exists']:
                    features_and_unique_keys = content['features_and_unique_keys']
                    chosen_params_and_values = Menu.choose_params_and_values(features_and_unique_keys)
                    response = requests.post(f"{self.classifier_URL}classify", json=chosen_params_and_values)
                    if response.ok:
                        content = response.json()
                        print(f"the answer is:  {content['classification']}.\n"
                              f"but take care because the accuracy is {content['accuracy']}%.")
                    else:
                        print("There was a problem with the classification")
                        print(f"status code: {response.status_code}")
                else:
                    print("Choose first a file to work with")
            else:
                print("There was a problem with the get_features_and_unique_keys")
                print(f"status code: {response.status_code}")
        except Exception as e:
            print("There was a error with the server.")
            print(f"Error: {e}.")

    def suggest_deleting_columns(self):
        choice = input("1. to delete any column of the table before training\n"
                       "2. to continue to training")
        if choice == "1":
            columns_to_drop = []
            response = requests.get(f"{self.trainer_URL}get_columns_list")
            if response.ok:
                list_of_columns = response.json()["columns_to_delete"]
                while len(list_of_columns) > 0:
                    chosen_column = Menu.suggest_options(list_of_columns)
                    columns_to_drop.append(chosen_column)
                    list_of_columns.remove(chosen_column)
                    done = input("write 'done' to execute, any other key to continue inserting")
                    if done == "done":
                        break
                print("executing..")
                response = requests.post(f"{self.trainer_URL}drop_requested_columns", json={"columns_to_drop": columns_to_drop})
                if response.ok:
                    print("The requested columns has been dropped")
                else:
                    print("There was a problem dropping the columns")
                    print(f"status code: {response.status_code}")
            else:
                print("there was a problem getting to the columns to delete")
                print(f"status code: {response.status_code}")
        elif choice == "2":
            print("Here we go")
        else:
            print("invalid input")
            self.suggest_deleting_columns()