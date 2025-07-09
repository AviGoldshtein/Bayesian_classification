from models.classifier import Classifier

class Tester:
    @staticmethod
    def check_accuracy(trained_model, test_df):
        if len(test_df.index) == 0:
            return 0

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