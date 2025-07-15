from server.logics.models.classifier import Classifier

class Tester:
    @staticmethod
    def check_accuracy(trained_model: dict, test_df) -> float:
        """
        Evaluates the accuracy of a trained model on a given test DataFrame.

        For each row in the test set, predicts the class using the model and compares it
        to the actual class (last column in the DataFrame). Returns the percentage of correct predictions.

        :param trained_model: A dict representing the trained model.
        :param test_df: A pandas DataFrame containing features and the target column (last).
        :return: Accuracy as a float (0-100).
        """
        if len(test_df.index) == 0:
            return 0.0

        correct = 0
        for i in range(len(test_df.index)):
            params_and_values = {}
            has_to_be = test_df.iloc[i, -1]
            row_values = test_df.iloc[i, :-1]
            for inx_row in row_values.index:
                params_and_values[inx_row] = row_values[inx_row]
            predicted = Classifier.ask_a_question(trained_model, params_and_values)
            if predicted == has_to_be:
                correct += 1

        return (correct / len(test_df.index)) * 100