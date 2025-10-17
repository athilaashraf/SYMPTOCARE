# Importing libraries
import os
import numpy as np
import pandas as pd
from scipy.stats import mode
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


class Disease:
    def __init__(self):
        # Use Django's BASE_DIR to get the correct path automatically
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.static_path = os.path.join(base_dir, "static") + "\\"
        
        # Reading the train.csv by removing the
        # last column since it's an empty column
        self.DATA_PATH = os.path.join(base_dir, "myapp", "Training.csv")
        self.data = pd.read_csv(self.DATA_PATH).dropna(axis=1)

        # Checking whether the dataset is balanced or not
        disease_counts = self.data["prognosis"].value_counts()
        temp_df = pd.DataFrame({
            "Disease": disease_counts.index,
            "Counts": disease_counts.values
        })

        # Encoding the target value into numerical
        # value using LabelEncoder
        encoder = LabelEncoder()
        self.data["prognosis"] = encoder.fit_transform(self.data["prognosis"])

        X = self.data.iloc[:, :-1]
        y = self.data.iloc[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=24)

        # Initializing Models
        self.models = {
            "SVC": SVC(),
            "Gaussian NB": GaussianNB(),
            "Random Forest": RandomForestClassifier(random_state=18)
        }

        # Producing cross validation score for the models
        for model_name in self.models:
            model = self.models[model_name]
            scores = cross_val_score(model, X, y, cv=10,
                                     n_jobs=-1,
                                     scoring=self.cv_scoring)
            print(f"Mean Score: {np.mean(scores)}")

        # Training and testing Random Forest Classifier
        rf_model = RandomForestClassifier(random_state=18)
        rf_model.fit(X_train, y_train)
        preds = rf_model.predict(X_test)
        print(f"Accuracy on train data by Random Forest Classifier: {accuracy_score(y_train, rf_model.predict(X_train))*100}")
        print(f"Accuracy on test data by Random Forest Classifier: {accuracy_score(y_test, preds)*100}")

        cf_matrix = confusion_matrix(y_test, preds)

        # Training the models on whole data
        self.final_svm_model = SVC()
        self.final_nb_model = GaussianNB()
        self.final_rf_model = RandomForestClassifier(random_state=18)
        self.final_svm_model.fit(X, y)
        self.final_nb_model.fit(X, y)
        self.final_rf_model.fit(X, y)

        # Reading the test data (optional - only for evaluation)
        try:
            self.test_data = pd.read_csv(os.path.join(base_dir, "myapp", "Testing.csv")).dropna(axis=1)
            test_X = self.test_data.iloc[:, :-1]
            test_Y = encoder.transform(self.test_data.iloc[:, -1])
        except FileNotFoundError:
            print("⚠️ Testing.csv not found - skipping test evaluation (not required for prediction)")
            self.test_data = None

        # Get symptom columns
        symptoms = X.columns.values

        # Creating a symptom index dictionary to encode the
        # input symptoms into numerical form
        symptom_index = {}
        for index, value in enumerate(symptoms):
            symptom = " ".join([i.capitalize() for i in value.split("_")])
            symptom_index[symptom] = index

        self.data_dict = {
            "symptom_index": symptom_index,
            "predictions_classes": encoder.classes_
        }

    def cv_scoring(self, estimator, X, y):
        return accuracy_score(y, estimator.predict(X))

    def predictDisease(self, symptoms):
        symptoms = symptoms.split(",")

        # Check if all symptoms provided in the input are in the symptom_index dictionary
        for symptom in symptoms:
            if symptom not in self.data_dict["symptom_index"]:
                raise ValueError(f"Symptom '{symptom}' not found in the dataset.")

        # Creating input data for the models
        input_data = [0] * len(self.data_dict["symptom_index"])
        for symptom in symptoms:
            index = self.data_dict["symptom_index"][symptom]
            input_data[index] = 1

        # Reshaping the input data and converting it into a suitable format for model predictions
        input_data = np.array(input_data).reshape(1, -1)

        # Generating individual outputs
        rf_prediction = self.data_dict["predictions_classes"][self.final_rf_model.predict(input_data)[0]]

        return rf_prediction