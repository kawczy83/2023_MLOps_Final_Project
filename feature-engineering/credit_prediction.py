import pandas as pd
import pickle
from scipy.io.arff import loadarff 
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, mean_squared_error

# Data source: https://www.openml.org/search?type=data&sort=runs&status=active&id=31
raw_data = loadarff('credit_data.arff')

df_data = pd.DataFrame(raw_data[0])
df_data = df_data.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)

pd.set_option('display.max_columns', None)
print(df_data.head())

'''
checking_status  duration                  credit_history  \
0              <0       6.0  critical/other existing credit
1        0<=X<200      48.0                   existing paid
2     no checking      12.0  critical/other existing credit
3              <0      42.0                   existing paid
4              <0      24.0              delayed previously

               purpose  credit_amount    savings_status employment  \
0             radio/tv         1169.0  no known savings        >=7
1             radio/tv         5951.0              <100     1<=X<4
2            education         2096.0              <100     4<=X<7
3  furniture/equipment         7882.0              <100     4<=X<7
4              new car         4870.0              <100     1<=X<4

   installment_commitment     personal_status other_parties  residence_since  \
0                     4.0         male single          none              4.0
1                     2.0  female div/dep/mar          none              2.0
2                     2.0         male single          none              3.0
3                     2.0         male single     guarantor              4.0
4                     3.0         male single          none              4.0

  property_magnitude   age other_payment_plans   housing  existing_credits  \
0        real estate  67.0                none       own               2.0
1        real estate  22.0                none       own               1.0
2        real estate  49.0                none       own               1.0
3     life insurance  45.0                none  for free               1.0
4  no known property  53.0                none  for free               2.0

                  job  num_dependents own_telephone foreign_worker class
0             skilled             1.0           yes            yes  good
1             skilled             1.0          none            yes   bad
2  unskilled resident             2.0          none            yes  good
3             skilled             2.0          none            yes  good
4             skilled             2.0          none            yes   bad
'''

print(df_data['class'].value_counts())

le = LabelEncoder()
df_data = df_data.apply(le.fit_transform)

print(df_data.head())

X = df_data.iloc[:, :-1]
y = df_data.iloc[:, -1]
print(X.columns)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the models
models = [
    {"name": "Logistic Regression", "model": LogisticRegression(max_iter=1000)},
    {"name": "Random Forest", "model": RandomForestClassifier(n_estimators=100)},
    {"name": "Support Vector Classifier", "model": SVC()},
    {"name": "K-Nearest Neighbors", "model": KNeighborsClassifier()},
    {"name": "Naive Bayes", "model": GaussianNB()}
]
# Train and evaluate each model
for m in models:
    model = m["model"]
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    precision = round(precision_score(y_test, y_pred),3)
    f1 = round(f1_score(y_test, y_pred),3)
    recall = round(recall_score(y_test, y_pred),3)
    print(f"Model: {m['name']}, Precision: {precision}")
    print(f"Model: {m['name']}, F1 Score: {f1}")
    print(f"Model: {m['name']}, Recall: {recall}")
    print("\n")

# random forest classifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Get feature importances
importances = model.feature_importances_

# Create a DataFrame to display feature and importance
print("Most important features in descending order")
feature_importances = pd.DataFrame({'feature': X.columns, 'importance': importances})

'''       
                    feature  importance
4            credit_amount    0.130056
12                     age    0.112338
0          checking_status    0.105016
1                 duration    0.096958
3                  purpose    0.070540
2           credit_history    0.054358
6               employment    0.049217
11      property_magnitude    0.045751
5           savings_status    0.045511
10         residence_since    0.043245
7   installment_commitment    0.042388
8          personal_status    0.032512
16                     job    0.031100
14                 housing    0.030839
13     other_payment_plans    0.028458
15        existing_credits    0.025999
18           own_telephone    0.021759
9            other_parties    0.017030
17          num_dependents    0.013316
19          foreign_worker    0.003611
'''

# Sort the DataFrame by importance in descending order
feature_importances = feature_importances.sort_values('importance', ascending=False)

print(feature_importances)

y_pred = model.predict(X_test)
print(y_pred)

print("Precision: ", round(precision_score(y_test, y_pred),3))
print("F1 Score: ", round(f1_score(y_test, y_pred),3))
print("Recall Score: ", round(recall_score(y_test, y_pred),3))

# Create a dictionary to hold your model and preprocessing objects
model_objects = {
    'model': model,
    'label_encoders': {},  # To hold all the label encoders
    'scaler': scaler  # The StandardScaler
}

# Iterate over the columns and fit the label encoders
# Save each label encoder to the dictionary
for column in df_data.columns:
    if df_data[column].dtype == 'object':
        le = LabelEncoder()
        df_data[column] = le.fit_transform(df_data[column])
        model_objects['label_encoders'][column] = le

# Save the model and preprocessing objects to a pickle file
with open('random_forest_model.bin', 'wb') as f:
    pickle.dump(model_objects, f)