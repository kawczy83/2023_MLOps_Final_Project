# Feature Engineering

## Credit Classification Model

In this project, we preprocess a dataset related to credit scoring and apply multiple machine learning algorithms, with an emphasis on the Random Forest model, to predict credit classifications.

The dataset is sourced from OpenML and loaded via the `scipy.io.arff` function. After an initial exploration and preprocessing, which includes encoding categorical variables, we split the data into training and test sets.

We train five different machine learning models: Logistic Regression, Random Forest, Support Vector Classifier, K-Nearest Neighbors, and Naive Bayes. Each model's performance is evaluated based on precision, F1 score, and recall.

The Random Forest model was particularly highlighted, with additional analysis performed. We extract and display the feature importances, providing insights into which factors are most influential in credit classification. The top five most important features, as determined by the Random Forest model, are:

1. `credit_amount`: This feature had the highest importance score, indicating that the amount of credit is the most significant predictor of credit classification.
2. `age`: The age of the credit holder is the second most important feature.
3. `checking_status`: The status of the checking account of the credit holder is the third most important feature.
4. `duration`: The duration of credit is the fourth most important feature.
5. `purpose`: The purpose of the credit is the fifth most important feature.

These feature importances provide insight into what factors the Random Forest model considers most significant when making its predictions.

Based on the F1 scores, the Random Forest model, with an F1 score of 0.866, outperforms the other models (Logistic Regression, Support Vector Classifier, K-Nearest Neighbors, and Naive Bayes) on the test set.

The final trained Random Forest model is saved to a binary file, `random_forest_model.bin`, for potential reuse in future applications.

Please note that this script requires the `credit_data.arff` file in the same directory to function properly. It uses a variety of data science libraries, including `pandas`, `scipy`, `sklearn`, and `pickle`.

Please refer to `credit_prediction.py` for the detailed implementation and comments.

## Instructions to Run the Script

**Set up the virtual environment**: In the project directory (where your Python script and the Pipfile are located), set up a new virtual environment and install the required packages. If you don't have a Pipfile, you can create one using the pipenv install command followed by the names of the packages you want to install:
shell

```
pipenv install pandas scipy scikit-learn pickle5
```

**Activate the virtual environment**: Use the following command to activate the Pipenv virtual environment:

```
pipenv shell
```

**Data file:** Make sure the **credit_data.arff** data file is in the same directory as your Python script. The script will read this data file.

**Running the script**: With the virtual environment activated and in the same directory as your Python script, run the script with the following command:


```
python credit_prediction.py
```
The script will execute, pre-processing the data, training the machine learning models, evaluating their performance, and saving the trained Random Forest model as a binary file.