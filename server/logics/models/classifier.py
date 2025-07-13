import numpy as np

class Classifier:
    @staticmethod
    def ask_a_question(model, dict_test):
        final_result = {}
        for option in model["sum"]:
            list_of_nums = []
            if not option == "total_cases":
                for column in dict_test:
                    try:
                        num = model[option][column][dict_test[column]]
                    except KeyError:
                        num = 1e-10
                    list_of_nums.append(num)
                list_of_nums.append(model['sum'][option] / model['sum']['total_cases'])
                list_of_nums = np.array(list_of_nums)
                result = np.prod(list_of_nums)
                final_result[option] = result

        strong = max(final_result, key=final_result.get)
        return strong