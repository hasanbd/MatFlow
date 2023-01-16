# Import necessary libraries
import json
import os

import joblib
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from forms.utils import isNumerical


def main():
    if 'iris.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        data = pd.read_csv('data/iris.csv')

        # Create the model parameters dictionary
        params = {}

        # Use two column technique
        col1, col2 = st.columns(2)
        # Design column 1
        y_var = col1.radio("1️⃣ Predict for ..... (Y) Variable⤵️", options=data.columns)
        # Design column 2
        X_var = col2.multiselect("2️⃣Prediction based on (X) Variables::⤵️", options=list(data.columns),
                                 default=list(data.columns))

        if len(X_var) == 0:
            st.error("You have to put in some X variable and it cannot be left empty.")

        # Check if y not in X
        if y_var in X_var:
            st.error("Warning! Y variable cannot be present in your X-variable.")
        pred_type = st.radio("3️⃣-🗯Select the process you want to run:(Now default 🔸Regression🔸)",
                             options=["Regression"],
                             )
        # Add to model parameters
        params = {
            'X': X_var,
            'y': y_var,
            'pred_type': pred_type,
        }

        # if st.button("4️⃣⚙️Run Models⚙️"):

        st.write(f"**🟩Predict for➡️** {y_var}")
        st.write(f"**🟩Prediction based on➡️** {X_var}")
        st.write("\n")
        st.write("\n")
        # Divide the data into test and train set
        X = data[X_var]
        y = data[y_var]
        # Perform encoding
        X = pd.get_dummies(X)
        # Check if y needs to be encoded
        if not isNumerical(y):
            le = LabelEncoder()
            y = le.fit_transform(y)

        # Perform train test ratio
        st.markdown(f"4️⃣🔹**Separate Training and Testing Data in Percentage:**")
        size = st.slider(f"🔸Percentage Ratio(%) for Training and Testing Data🔸",
                         min_value=0.1,
                         max_value=0.9,
                         step=0.1,
                         value=0.8,
                         )

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=size, random_state=100)
        st.write(f"⏩**Distribution of Testing and Training Data**🔸 ")
        st.write(f"Number of Training Data⇾{X_train.shape[0]}")
        st.write(f"Number of Testing Data⇾{X_test.shape[0]}")

        # Save the model params as a json file
        with open('data/metadata/model_params.json', 'w') as json_file:
            json.dump(params, json_file)

        if pred_type == "Regression":
            st.write(f"5️⃣🔵**Results of Regression Model**🟠")

            # Table to store model and accurcy
            model_r2 = []
            # Linear regression model
            lr_model = LinearRegression()
            lr_model.fit(X_train, y_train)
            lr_r2 = lr_model.score(X_test, y_test)
            model_r2.append(['Linear Regression', lr_r2])
            joblib.dump(lr_model, 'data/metadata/model_reg.sav')
            # Show results
            results = pd.DataFrame(model_r2, columns=['Models', 'R2 Score']).sort_values(by='R2 Score', ascending=False)
            st.dataframe(results)

            # Store model and accurcy
            model_acc = []
            # Linear Regression Model
            lc_model = LogisticRegression()
            lc_model.fit(X_train, y_train)
            lc_acc = lc_model.score(X_test, y_test)
            model_acc.append(['Linear Regression', lc_acc])
            joblib.dump(lc_model, 'data/metadata/model_classification.sav')
            res = pd.DataFrame(model_acc, columns=['Models', 'Accuracy']).sort_values(by='Accuracy', ascending=False)
            st.dataframe(res)
