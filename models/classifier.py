import numpy as np

class Classifier:
    @staticmethod
    def ask_a_question(model, dict_test):
        final_result = {}
        for option in model["sum"]:
            list_of_nums = []
            if not option == "total_cases":
                for column in dict_test:
                    num = model[option][column][dict_test[column]]
                    list_of_nums.append(num)
                list_of_nums.append(model['sum'][option] / model['sum']['total_cases'])
                list_of_nums = np.array(list_of_nums)
                if 0 in list_of_nums:
                    list_of_nums += 1
                result = np.prod(list_of_nums)
                result %= 1
                final_result[option] = result

        for key, val in final_result.items():
            print(f"{key} has {val}")
        strong = max(final_result, key=final_result.get)
        print(f"it is obviously {strong} 😉\n")