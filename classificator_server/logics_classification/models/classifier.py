from typing import Dict
import numpy as np

class Classifier:
    @staticmethod
    def ask_a_question(model: dict, dict_test: Dict[str, str]) -> str:
        """
        Predicts the most likely class using a trained Naive Bayes model and input features.

        :param model: Trained model as a nested dictionary.
        :param dict_test: Dictionary of feature_name -> selected_value.
        :return: Most likely class label.
        """
        final_result = {}
        for label in model["sum"]:
            likelihoods = []
            if label == "total_cases":
                continue

            for feature, value in dict_test.items():
                try:
                    num = model[label][feature][value]
                except KeyError:
                    num = 1e-10
                likelihoods.append(num)
            likelihoods.append(model['sum'][label] / model['sum']['total_cases'])
            likelihoods = np.array(likelihoods)
            result = np.prod(likelihoods)
            final_result[label] = result

        most_likely_label = max(final_result, key=final_result.get)
        return most_likely_label