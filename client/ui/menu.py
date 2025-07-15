class Menu:
    @staticmethod
    def show_menu():
        """
        Presents the menu with all its options and gets user's choice.
        :return: the user's choice as a string
        """
        choice = input("\n1. to select a local file to work with\n"
                       "2. copy a link for a csv file\n"
                      "3. Analyze by model statistics\n"
                      "1000. to exit\n")
        return choice

    @staticmethod
    def suggest_options(options: list) -> str:
        """
        Presents a numbered list of options and asks the user to choose one.
        :param options: list of options to present
        :return: the selected option as a string
        """
        print("choose one of the options below:")
        choices = {}
        i = 1
        for option in options:
            choices[i] = option
            print(f"{i}. {option}")
            i += 1
        choice = input()
        if not choice.isdigit():
            print("Enter only numbers")
            return Menu.suggest_options(options)
        num_choice = int(choice)
        if not (0 < num_choice < i):
            print(f"the number must be between 1 and {i - 1}")
            return Menu.suggest_options(options)
        return choices[num_choice]

    @staticmethod
    def choose_params_and_values(suggestion_dict: dict) -> dict[str, str]:
        """
        Suggests the user parameters (labels), and for each parameter, suggests possible values.
        The user selects one value per parameter. The selections are collected into a dictionary.

        :param suggestion_dict: A dictionary where keys = labels, values = list of unique options per label.
        :return: A dictionary where key = label, value = selected option.
        """
        chosen_options = {}
        for label, options in suggestion_dict.items():
            print(f"For the parameter '{label}':")
            chosen = Menu.suggest_options(options)
            chosen_options[label] = chosen
        return chosen_options
