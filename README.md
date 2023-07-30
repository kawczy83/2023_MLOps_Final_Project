# MLOps Zoomcamp Project - Credit Prediction

This is my project for MLOps Zoomcamp from DataTalks.Club

## About MLOps Zoomcamp

MLOps Zoomcamp is a course designed to teach the practical aspects of productionizing ML services, ranging from training and experimenting to model deployment and monitoring. It's intended for data scientists and ML engineers, as well as software engineers and data engineers who are interested in learning about putting ML in production.

The course covers a wide range of topics, including experiment tracking and model management, workflow orchestration and ML pipelines, model deployment, model monitoring, and best practices for testing, linting, formatting, CI/CD, and Infrastructure as Code (IaC).

More information about the course can be found [here](https://github.com/DataTalksClub/mlops-zoomcamp).

## Objective

Credit is differentiated according to various factors like credit history, payment behavior, and current income. Judging the creditworthiness of an individual manually is a complex task. Even professional credit analysts don't always achieve perfect accuracy.

This project aims to alleviate this complexity. Our objective is to identify the features that best predict the creditworthiness of an individual and to produce insights into how each of these features impacts the credit classification in our model. Understanding how each feature will impact the creditworthiness will help financial institutions, lenders, and companies in the credit sector to better evaluate their lending, risk management, and pricing strategy.

This project uses the [German Credit Dataset](https://www.openml.org/search?type=data&sort=runs&status=active&id=31), which classifies people described by a set of attributes as good or bad credit risks

## Project Structure

This project is organized according to the criteria mentioned in the [MLOps Zoomcamp Course Project](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/07-project). Each part of the project is contained within its own directory:

1. **feature_engineering**: Contains code and resources related to the feature engineering stage of the project.

2. **experiment_tracking_and_model_registry**: Houses code and files for tracking experiments and managing the model registry.

3. **workflow_orchestration**: Includes scripts and files for orchestrating the machine learning workflow.

4. **model_deployment**: Consists of code and resources for deploying the machine learning model.

5. **model_monitoring**: Contains scripts and files for monitoring the performance of the deployed model.

6. **best_practices**: Includes resources and documents outlining the best practices followed in this project.

Each directory has its own README file with instructions on how to run the relevant code. Additionally, each directory contains a Pipfile. If you encounter any issues with the virtual environment, you can use the Pipfile to set up a new one.

For more information on creating a virtual environment using a Pipfile, please refer to this [StackOverflow post](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment).

## Tools and Technologies Used 

* **Cloud Computing**: **AWS** is used for scalable, on-demand cloud computing capabilities.

* **Experiment Tracking and Model Registry**: **MLflow** is used to track experiments and manage the model registry. It enables reproducibility and collaboration by tracking experiments, sharing predictions, and deploying models.

* **Workflow Orchestration**: **Prefect** is used to build, schedule, and monitor workflows. It allows the creation of robust data pipelines that can handle tasks such as data ingestion, data processing, and model training.

* **Containerization**: **Docker** and **Docker Compose** are used to create, deploy, and run applications by using containers. This ensures that the application works uniformly across different computing environments.

* **Model Deployment**: The model is deployed as a web service using **Flask**, **Docker**, **MLflow**, and **AWS**. This combination of tools allows for a robust and scalable model deployment.

* **Model Monitoring**: **Evidently AI** is used for detailed data and model monitoring, **Grafana** for creating interactive visual analytics, and **Adminer** for database management.

* **Best Practices**: A variety of methods are used to ensure high-quality, maintainable code, including unit tests, integration tests, linting, code formatting, Makefile for automating code tasks, and pre-commit hooks for maintaining consistent commit standards.


## Future Works

While the current project provides a comprehensive approach to credit prediction, there are several areas identified for future enhancements:

1. **Model Retraining and Alerts**: Implement functionality for model retraining, and establish alert systems to notify the relevant teams when data drift is detected. This can help ensure that the model's performance remains optimal over time.

2. **CI/CD**: Incorporate continuous integration and continuous deployment (CI/CD) pipelines to automate the testing and deployment of the project. This can improve efficiency, increase deployment speed, and reduce the risk of human error.

3. **IaC**: Integrate Infrastructure as Code (IaC) practices to automate the setup and management of the computing environment. IaC can help ensure consistent and reproducible computing environments, reducing the risk of environment-related issues.

**NOTE** : For the peer review process, it is recommended to download the repository as a zip file rather than cloning it using Git bash. Cloning the repository may lead to issues when reviewing the 'best_practices' section of the project.