import os
import pickle
import click
import mlflow

from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

os.environ["AWS_PROFILE"] = "default"
os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'

HPO_EXPERIMENT_NAME = "test"
EXPERIMENT_NAME = "credit-card-random-forest-best-models-1"
RF_PARAMS = ['max_depth', 'n_estimators', 'min_samples_split', 'min_samples_leaf', 'random_state', 'n_jobs']

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.sklearn.autolog()


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def train_and_log_model(data_path: str, params: dict):
    
    with mlflow.start_run():
        
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
        
        for key, value in params.items():
            if value == 'True':
                params[key] = True
            elif value == 'False':
                params[key] = False
            elif value == 'None':
                params[key] = None
            elif '.' in value:  # value could be a float
                try:
                    params[key] = float(value)
                except ValueError:
                    pass
            else:
                try:
                    params[key] = int(value)
                except ValueError:
                    pass

        rf = RandomForestClassifier(**params)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)
        mlflow.log_metric("accuracy", accuracy)
        
    return accuracy


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed credit card data was saved"
)
@click.option(
    "--top_n",
    default=5,
    type=int,
    help="Number of top models that need to be evaluated to decide which one to promote"
)
def run_register_model(data_path: str, top_n: int):

    client = MlflowClient()

    # Retrieve the top_n model runs and log the models
    experiment = client.get_experiment_by_name(HPO_EXPERIMENT_NAME)
    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.accuracy DESC"]
    )
    
    best_run = None
    best_accuracy = float('-inf')
    for run in runs:
        run_accuracy = train_and_log_model(data_path=data_path, params=run.data.params)
        if run_accuracy > best_accuracy:
            best_accuracy = run_accuracy
            best_run = run

    # Register the best model
    mlflow.register_model(f"runs:/{best_run.info.run_id}/model", "BestRandomForestModel")


if __name__ == '__main__':
    run_register_model()
