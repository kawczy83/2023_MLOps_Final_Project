# Model Monitoring with Evidently, Grafana, Adminer, and Prefect

This repository provides a simple setup for monitoring Machine Learning models using Evidently, Grafana, Adminer, and Prefect. The scripts herein compute and report metrics, and store Evidently reports in HTML format. If you need assistance creating a virtual environment with Pipfile, refer to this [stackoverflow thread](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment).

## Execution Instructions

Follow the steps below to execute the scripts:

1. Open three terminal windows. In each terminal, navigate to the `model_monitoring` directory and activate the virtual environment containing the libraries specified in the Pipfile. Use the command below to activate the environment:

   ```
   pipenv shell
   ```
   
2. In the first terminal, launch the Evidently, Adminer, and Grafana services with this command:

   ```
   docker-compose up
   ```
   > **Note:** Leave these services running and proceed to the second terminal for the subsequent steps.

3. Download the dataset by executing the `baseline_model_credit_data.ipynb` Jupyter Notebook.

4. Before moving to the next step, ensure all services from Step 2 are operational.

5. (Optional) You can observe the data drift at [http://localhost:3000/](http://localhost:3000/) either while the data is being sent or afterwards. Use `admin` as the username and password. The Adminer database can be accessed at [http://localhost:8080/](http://localhost:8080/).

6. Once the data is sent, launch the Prefect server in the second terminal:

   ```
   prefect server start
   ```
   Prefect can be accessed at [http://localhost:4200/](http://localhost:4200/). Now, switch to the third terminal to run `evidently_metrics_calculation.py`.

7. In the third terminal, execute the `evidently_metrics_calculation.py` script:

   ```
   python evidently_metrics_calculation.py
   ```
   This script will:

   - Extract PostgreSQL database connection parameters from the environment variables.
   - Load reference data and a machine learning model from disk.
   - Load and preprocess a dataset from an ARFF file.
   - Define Prefect tasks for database connection, database preparation, and metric computation.
   - In a Prefect flow, it will prepare the database and create a table (if it doesn't already exist). Then, in a loop, it will compute prediction metrics using the loaded model and data, insert the calculated metrics into the PostgreSQL database table, and implement a delay between iterations to prevent database overload.
   
   You can view the flows, flow runs, and radar plot at [http://localhost:4200/](http://localhost:4200/).

To view the Evidently report (HTML file), first download it to your local system and then open it with your preferred browser.
