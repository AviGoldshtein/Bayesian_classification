class Menu:
    @staticmethod
    def show_menu():
        choice = input("1. to select a local file to work with\n"
                       "2. copy a link for a csv file\n"
                      "3. Analyze by model statistics\n"
                      "1000. to exit\n")
        return choice

    @staticmethod
    def suggest_options(options):
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
    def get_params(suggestion_dict):
        chosen_options = {}
        for suggestion in suggestion_dict:
            print(f"for the parameter {suggestion}:")
            chosen = Menu.suggest_options(suggestion_dict[suggestion])
            chosen_options[suggestion] = chosen
        return chosen_options
