import os
import datetime
import time
import logging
import pandas as pd


import psycopg
import joblib

from prefect import task, flow
from scipy.io.arff import loadarff 
from sklearn.preprocessing import LabelEncoder

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric, ColumnValueRangeMetric, ColumnQuantileMetric


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = int(os.getenv("SEND_TIMEOUT", 10))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "test")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "example")

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float,
	range_value float,
	quantile_value float
)
"""

reference_data = pd.read_parquet('data/reference.parquet')
with open('models/log_reg.bin', 'rb') as f_in:
	model = joblib.load(f_in)

raw_data = loadarff('./data/credit-g.data.arff')
df = pd.DataFrame(raw_data[0])
le = LabelEncoder()
df['class'] = le.fit_transform(df['class'])

num_features = ['duration', 'credit_amount', 'installment_commitment', 'age', 'existing_credits', 'num_dependents']
cat_features = ['checking_status', 'credit_history', 'purpose', 'savings_status', 'employment', 'personal_status', 
                'other_parties', 'property_magnitude', 'other_payment_plans', 'housing', 'job', 'own_telephone', 
                'foreign_worker']
column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

report = Report(metrics = [
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric(),
    ColumnValueRangeMetric(column_name='credit_amount', left=1365, right=3972),
    ColumnQuantileMetric(column_name='credit_amount', quantile=0.5)
])

@task
def get_database_connection():
    return psycopg.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, autocommit=True
    )


@task
def prep_db(conn):
    res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
    if len(res.fetchall()) == 0:
        conn.execute("create database test;")
    conn.execute(create_table_statement)

@task
def calculate_metrics_postgresql(curr, i, name="calculate metrics"):
	current_data = df

	#current_data.fillna(0, inplace=True)
	current_data['prediction'] = model.predict(current_data[num_features + cat_features].fillna(0))

	report.run(reference_data = reference_data, current_data = current_data,
		column_mapping=column_mapping)

	result = report.as_dict()

	prediction_drift = result['metrics'][0]['result']['drift_score']
	num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
	share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']
	range_value = result['metrics'][3]['result']['current']['share_in_range']
	quantile_value = result['metrics'][4]['result']['current']['value']

	curr.execute(
    "insert into dummy_metrics(prediction_drift, num_drifted_columns, share_missing_values, range_value, quantile_value) values (%s, %s, %s, %s, %s)",
    (prediction_drift, num_drifted_columns, share_missing_values, range_value, quantile_value)
)

@flow
def batch_monitoring_backfill():
    conn = get_database_connection()
    prep_db(conn)
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    try:
        for i in range(1, 2): 
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)
                
            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            
            logging.info("data sent for iteration %d", i)

    except Exception as e:
        logging.error("Error in batch monitoring backfill: " + str(e))

if __name__ == '__main__':
    batch_monitoring_backfill()
