# Workflow Orchestration with Prefect

This repository demonstrates a workflow orchestration process using [Prefect](https://www.prefect.io/), with data stored in an AWS S3 bucket. 

The following Prefect services are demonstrated:

- Deployments
- Storage (S3)
- Blocks
- Work Queues and Agents

## Prefect Storage

Storage in Prefect is responsible for persisting and retrieving flow code for deployments. When we build a deployment, a storage block uploads the entire directory containing our workflow code to a configured location. This approach ensures the portability of relative imports, configuration files, and other dependencies.

If no storage is explicitly configured, Prefect uses LocalFileSystem storage by default. However, due to potential portability issues, this project utilizes AWS S3 for remote storage.

## Prefect Blocks

Blocks within Prefect store configuration details and provide an interface for interacting with external systems. They are useful for sharing configuration across flow runs and between flows.

## Prefect Agents and Work Queues

Agents and work queues in Prefect connect the orchestration environment with the execution environment. When a deployment creates a flow run, it is submitted to a specific work queue for scheduling. Agents in the execution environment poll their work queues for new runs to execute. Work queues are automatically created whenever referenced by either a deployment or an agent.

## Preparations

Before running any commands, ensure you have an S3 bucket created in your AWS account, as the script saves data files to this bucket.

You'll also need to configure your AWS credentials for CLI access. This can be done in the terminal by running the command `aws configure`, and entering the following details:

- AWS Access Key ID
- AWS Secret Access Key
- Default region name
- Default output format

**Note**: This project uses the terminal. If you encounter environment issues, a Pipfile is provided for creating a virtual environment using the command `pipenv install`. [This guide](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment) provides further details.

Before executing the script, make the following changes in `orchestration.py`:

- On line 122, enter the name of your S3 bucket, and remove `credit-card-mlops-orchestration`.

## Steps to Run the Script

Open three terminal windows (Terminal 1, Terminal 2, Terminal 3). In all the terminals, activate your virtual environment (with the libraries mentioned in the Pipfile) and navigate to the `workflow_orchestration` directory.

Activate the virtual environment by running `pipenv shell`.

1. In Terminal 1, execute `prefect server start`.
2. In Terminal 2, run `prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`.
3. In Terminal 2, run the command as shown in the original readme.
4. In Terminal 2, run `prefect deployment apply main-deployment.yaml`.
5. To view the deployments, run `prefect deployment ls` in Terminal 2.
6. Create a work queue by running `prefect work-queue create {work-queue-name}` in Terminal 2.
7. To deploy the flow runs present in the work queue, start an agent by running `prefect agent start 'uuid'` in Terminal 2.

For further details on scheduling deployments and changes in yaml files, follow [this guide](https://orion-docs.prefect.io/concepts/schedules/).

You can view your flows, deployments, blocks, and work queues at http://127.0.0.1:4200.
