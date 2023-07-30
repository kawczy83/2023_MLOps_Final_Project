import pandas as pd
import pickle
import requests as req
import os
from scipy.io.arff import loadarff 

from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from botocore.exceptions import ClientError

from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
from prefect.filesystems import S3
import boto3


# first 5 lines of credit card data sample
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

@task
def read_data(filename: str):
    data = loadarff('./data/credit_data.arff')
    df = pd.DataFrame(data[0])
    le = LabelEncoder()
    df['class'] = le.fit_transform(df['class'])
    return df


@task
def train_model(df, numerical):
    
    logger = get_run_logger()
    train_dicts = df[numerical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df['class'].values

    logger.info(f"The shape of X_train is {X_train.shape}")
    logger.info(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    accuracy = accuracy_score(y_train, y_pred)
    logger.info(f"The accuracy of training is: {accuracy}")
    return lr, dv

@task
def run_model(df, numerical, dv, lr):
    logger = get_run_logger()
    val_dicts = df[numerical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df['class'].values

    accuracy = accuracy_score(y_val, y_pred)
    logger.info(f"The accuracy of validation is: {accuracy}")
    return
        
@flow(name="main", task_runner=SequentialTaskRunner())
def main():

    numerical = ['duration', 'credit_amount', 'installment_commitment', 'residence_since', 'age', 'existing_credits', 'num_dependents']
    
    df = read_data('./data/credit_data.arff')
    
    # Split into training and validation sets
    df_train, df_val = train_test_split(df, test_size=0.2, random_state=42)   

    # train the model
    lr, dv = train_model(df_train, numerical)
    run_model(df_val, numerical, dv, lr)
    
    with open('models/log_reg.pkl', 'wb') as f_out:
        pickle.dump((lr), f_out)
    
    with open('models/dv.pkl', 'wb') as f_out:
        pickle.dump((dv), f_out)
    
    block = S3(bucket_path="credit-card-mlops-orchestration/prefect-orion")
    block.save("mlops-project-block", overwrite=True) 

if __name__ == "__main__":
    main()