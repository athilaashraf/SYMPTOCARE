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
        self.DATA_PATH = self.static_path + "Training.csv"
        self.data = pd.read_csv(self.DATA_PATH).dropna(axis=1)
        
        # ... rest of your code continues"


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

        # print(f"Train: {X_train.shape}, {y_train.shape}")
        # print(f"Test: {X_test.shape}, {y_test.shape}")


        # Defining scoring metric for k-fold cross validation


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
            # print("==" * 30)
            # print(model_name)
            # print(f"Scores: {scores}")
            print(f"Mean Score: {np.mean(scores)}")

        # Training and testing SVM Classifier
        # svm_model = SVC()
        # svm_model.fit(X_train, y_train)
        # preds = svm_model.predict(X_test)

        # print(f"Accuracy on train data by SVM Classifier\
        # : {accuracy_score(y_train, svm_model.predict(X_train))*100}")

        # print(f"Accuracy on test data by SVM Classifier\
        # : {accuracy_score(y_test, preds)*100}")
        # cf_matrix = confusion_matrix(y_test, preds)
        # plt.figure(figsize=(12,8))
        # sns.heatmap(cf_matrix, annot=True)

        # Training and testing Naive Bayes Classifier
        # nb_model = GaussianNB()
        # nb_model.fit(X_train, y_train)
        # preds = nb_model.predict(X_test)
        # print(f"Accuracy on train data by Naive Bayes Classifier\
        # : {accuracy_score(y_train, nb_model.predict(X_train))*100}")

        # print(f"Accuracy on test data by Naive Bayes Classifier\
        # : {accuracy_score(y_test, preds)*100}")
        # cf_matrix = confusion_matrix(y_test, preds)
        # plt.figure(figsize=(12,8))
        # sns.heatmap(cf_matrix, annot=True)

        # Training and testing Random Forest Classifier
        rf_model = RandomForestClassifier(random_state=18)
        rf_model.fit(X_train, y_train)
        preds = rf_model.predict(X_test)
        print(f"Accuracy on train data by Random Forest Classifier\
        : {accuracy_score(y_train, rf_model.predict(X_train))*100}")

        print(f"Accuracy on test data by Random Forest Classifier\
        : {accuracy_score(y_test, preds)*100}")

        cf_matrix = confusion_matrix(y_test, preds)
        # plt.figure(figsize=(12,8))
        # sns.heatmap(cf_matrix, annot=True)

        # Training the models on whole data
        self.final_svm_model = SVC()
        self.final_nb_model = GaussianNB()
        self.final_rf_model = RandomForestClassifier(random_state=18)
        self.final_svm_model.fit(X, y)
        self.final_nb_model.fit(X, y)
        self.final_rf_model.fit(X, y)

        # Reading the test data
        self.test_data = pd.read_csv(self.static_path+"Testing.csv").dropna(axis=1)

        test_X = self.test_data.iloc[:, :-1]
        test_Y = encoder.transform(self.test_data.iloc[:, -1])

        # Making prediction by take mode of predictions
        # made by all the classifiers
        # svm_preds = self.final_svm_model.predict(test_X)
        # nb_preds = self.final_nb_model.predict(test_X)
        rf_preds = self.final_rf_model.predict(test_X)

        # final_preds = [mode([i, j, k])[0][0] for i, j,
        #                                          k in zip(svm_preds, nb_preds, rf_preds)]

        # print(f"Accuracy on Test dataset by the combined model\
        # : {accuracy_score(test_Y, final_preds)*100}")

        # cf_matrix = confusion_matrix(test_Y, final_preds)
        # plt.figure(figsize=(12, 8))

        # sns.heatmap(cf_matrix, annot=True)

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


        # Defining the Function
        # Input: string containing symptoms separated by commmas
        # Output: Generated predictions by models

    def cv_scoring(self,estimator, X, y):
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
        # nb_prediction = self.data_dict["predictions_classes"][self.final_nb_model.predict(input_data)[0]]
        # svm_prediction = self.data_dict["predictions_classes"][self.final_svm_model.predict(input_data)[0]]

        # # Making the final prediction by finding the most frequent element
        # predictions = [rf_prediction, nb_prediction, svm_prediction]
        # final_prediction = max(set(predictions), key=predictions.count)

        return rf_prediction

# Testing the function
# d=Disease()
# dg= ['Itching', 'Skin Rash', 'Nodal Skin Eruptions', 'Continuous Sneezing', 'Shivering', 'Chills', 'Joint Pain', 'Stomach Pain', 'Acidity', 'Ulcers On Tongue', 'Muscle Wasting', 'Vomiting', 'Burning Micturition', 'Spotting  urination', 'Fatigue', 'Weight Gain', 'Anxiety', 'Cold Hands And Feets', 'Mood Swings', 'Weight Loss', 'Restlessness', 'Lethargy', 'Patches In Throat', 'Irregular Sugar Level', 'Cough', 'High Fever', 'Sunken Eyes', 'Breathlessness', 'Sweating', 'Dehydration', 'Indigestion', 'Headache', 'Yellowish Skin', 'Dark Urine', 'Nausea', 'Loss Of Appetite', 'Pain Behind The Eyes', 'Back Pain', 'Constipation', 'Abdominal Pain', 'Diarrhoea', 'Mild Fever', 'Yellow Urine', 'Yellowing Of Eyes', 'Acute Liver Failure', 'Fluid Overload', 'Swelling Of Stomach', 'Swelled Lymph Nodes', 'Malaise', 'Blurred And Distorted Vision', 'Phlegm', 'Throat Irritation', 'Redness Of Eyes', 'Sinus Pressure', 'Runny Nose', 'Congestion', 'Chest Pain', 'Weakness In Limbs', 'Fast Heart Rate', 'Pain During Bowel Movements', 'Pain In Anal Region', 'Bloody Stool', 'Irritation In Anus', 'Neck Pain', 'Dizziness', 'Cramps', 'Bruising', 'Obesity', 'Swollen Legs', 'Swollen Blood Vessels', 'Puffy Face And Eyes', 'Enlarged Thyroid', 'Brittle Nails', 'Swollen Extremeties', 'Excessive Hunger', 'Extra Marital Contacts', 'Drying And Tingling Lips', 'Slurred Speech', 'Knee Pain', 'Hip Joint Pain', 'Muscle Weakness', 'Stiff Neck', 'Swelling Joints', 'Movement Stiffness', 'Spinning Movements', 'Loss Of Balance', 'Unsteadiness', 'Weakness Of One Body Side', 'Loss Of Smell', 'Bladder Discomfort', 'Foul Smell Of urine', 'Continuous Feel Of Urine', 'Passage Of Gases', 'Internal Itching', 'Toxic Look (typhos)', 'Depression', 'Irritability', 'Muscle Pain', 'Altered Sensorium', 'Red Spots Over Body', 'Belly Pain', 'Abnormal Menstruation', 'Dischromic  Patches', 'Watering From Eyes', 'Increased Appetite', 'Polyuria', 'Family History', 'Mucoid Sputum', 'Rusty Sputum', 'Lack Of Concentration', 'Visual Disturbances', 'Receiving Blood Transfusion', 'Receiving Unsterile Injections', 'Coma', 'Stomach Bleeding', 'Distention Of Abdomen', 'History Of Alcohol Consumption', 'Fluid Overload.1', 'Blood In Sputum', 'Prominent Veins On Calf', 'Palpitations', 'Painful Walking', 'Pus Filled Pimples', 'Blackheads', 'Scurring', 'Skin Peeling', 'Silver Like Dusting', 'Small Dents In Nails', 'Inflammatory Nails', 'Blister', 'Red Sore Around Nose', 'Yellow Crust Ooze']
# print(len(dg))
# print(d.predictDisease("Shivering,Chills"))
