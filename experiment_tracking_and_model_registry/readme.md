# Experiment Tracking and Model Registry

This section aims to perform experiment tracking and register best models using MLflow. 

**Note:** HPO stands for Hyperparameter Optimization

File Structure : 

1. preprocess.py -> This script loads the raw data from input folder, processes it and saves the pre-processed data in output folder.

2. train.py -> The script will load the pre-processed data from output folder, train the model on the training set and calculate the accuracy on the validation set. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

3. hpo.py -> This script tries to reduce the validation error by tuning the hyperparameters of the random forest regressor using hyperopt. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

4. register_model.py -> This script will promote the best model (with highest test_accuracy) to the model registry. It will check the results from the previous step and select the top 5 runs. After that, it will calculate the accuracy of those models on the test set and save the results to a new experiment called "credit-card-random-forest-best-models-1". The model with highest test accuracy from the 5 runs is registered.

**Artifacts can be saved locally as well as on cloud (AWS). My script saves these artifacts in S3 bucket. It meets the requirement of developing project on Cloud (mentioned in README of course project of MLOps Zoomcamp Github Repo).**

The scripts use SQLite as backend and Cloud (AWS S3) for storing the artifacts.

Before running any commands, **please create a S3 bucket in your AWS account**. The scripts will log artifacts in your S3 bucket. It will also log in MLflow, locally
(http://127.0.0.1:5000)

It will ask you for your :

1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region name
4. Default output format

Please enter the credentials above before running the scripts.

These credentials have profile name as "default". I recommend to use your default AWS profile for running the scripts so that you won't need to make any changes in the python scripts provided. However, if you wish to use any other AWS profile other than the "default" one, then please make changes in credentials and config files accordingly. These files are located at **~/.aws/credentials** for Linux and Mac and at **%USERPROFILE%\.aws\credentials** for Windows. More information on setting up profile can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)

If you use any other AWS profile other than "default", then you will have to make some changes in train.py, hpo.py and register_model.py. These changes are discussed later in this document.

### Steps to run the scripts

1. Open 2 terminal - Terminal 1 and Terminal 2. In both the terminals, activate virtual environment which has the libraries mentioned in **requirements.txt** file. You should be inside experiment_tracking_and_model_registry directory in both the terminals.

2. In terminal 1, start the MLflow server using the following command :

       python3 -m mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3:///{bucket-name}
       
If your S3 bucket name is mlops-zoomcamp-project, the command should look like : 

       python3 -m mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://credit-card-mlops-project/

**NOTE :** The server should keep running, and you should go to terminal 2 to execute the scripts.

3. Go to terminal 2, and execute the script preprocess.py. This script loads the raw data from input folder, preprocesses it and saves the pre-processed data in output folder. Run the script using the following command : 

       python3 preprocess.py

4. Make sure the server from step 1 is up and running. After the execution of step-2 is finished, execute the script train.py in terminal 2. Run the script using the following command : 

       python3 train.py
       
The script will load the datasets produced by the previous step, train the model on the training set and calculates the accuracy on the validation set. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud). 

**NOTE :** If you use other AWS profile other than "default", then please go to **line number 10** of train.py and change the os.environ["AWS_PROFILE"] variable to your profile name before executing the script. If the profile name is "user1", then line number 10 should look like : os.environ["AWS_PROFILE"] = "user1"

5. After the execution of step 3 is finished, execute the script hpo.py in terminal 2. Run the script using the following command :

       python3 hpo.py
       
This script tries to reduce the validation error by tuning the hyperparameters of the random forest regressor using hyperopt. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

**NOTE :** If you use other AWS profile other than "default", then please go to **line number 11** of hpo.py and change the os.environ["AWS_PROFILE"] variable to your profile name before executing the script. If the profile name is "user1", then line number 11 should look like : os.environ["AWS_PROFILE"] = "user1"

6. After the execution of step 4 is finished, execute the script register_model.py in terminal 2. Run the script using the following command :

       python3 register_model.py
   
This script will promote the best model (with highest test_accuracy) to the model registry. It will check the results from the previous step and select the top 5 runs. After that, it will calculate the accuracy of those models on the test set and save the results to a new experiment called "credit-card-random-forest-best-models-1". 

For model registry, out of the 5 runs in "credit-card-random-forest-best-models-1" experiment, the run with highest test_accuracy is registered. You can view the registered model at **http://127.0.0.1:5000/#/models** 

The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

**NOTE :** If you use other AWS profile other than "default", then please go to **line number 11** of register_model.py and change the os.environ["AWS_PROFILE"] variable to your profile name before executing the script. If the profile name is "user1", then line number 11 should look like : os.environ["AWS_PROFILE"] = "user1"

**NOTE :** If you encounter **connection in use** error while running MLflow, the run the following command in terminal :

    pkill gunicorn

Experiments and models(and artifacts) can be viewed locally at http://127.0.0.1:5000 Registered model can also be viewed at http://127.0.0.1:5000/#/models

To view the artifacts on cloud, please visit your AWS S3 bucket. The bucket will have 3 folders named "1/", "2/", and "3/". These 3 folders will have artifacts of the models which were logged by running the 3 scripts train.py, hpo.py, and register_model.py respectively. Refresh the website if these folders are not visible in your S3 bucket.
