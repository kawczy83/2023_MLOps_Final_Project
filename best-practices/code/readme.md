# Project Best Practices

This document provides an overview of the key elements of the project structure and a guide on how to execute key tasks such as running tests, linting, code formatting, and using pre-commit hooks.

## Project Structure

- **Unit Tests**: Located in the `tests` directory.
- **Integration Tests**: Located in the `integration-test` directory.
- **Linting and Code Formatting**: Configuration specified in `pyproject.toml`.
- **Build Automation**: A `Makefile` is included to simplify certain tasks.
- **Pre-Commit Hooks**: Configuration specified in `.pre-commit-config.yaml`.

## Environment Setup

A `Pipfile` has been provided to manage dependencies and setup the Python environment. In case of issues with the environment, the `Pipfile` can be used to create a virtual environment using the command: `pipenv install`. More information on creating a virtual environment using a `Pipfile` can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment).

To activate the virtual environment, execute the following command in the terminal:

```
pipenv shell
```

## Running Integration Tests

The `integration-test` directory includes a `run.sh` file. It's important to ensure that the appropriate permissions are set for this file, otherwise a permission denied error may occur. 

While in the `code` directory, permissions can be granted by executing the following command in the terminal:

```
chmod +x integration-test/run.sh
```

## How to Run Unit Tests, Integration Tests, Linting, and Code Formatting

1. Open the terminal and activate the virtual environment that includes the libraries specified in the `Pipfile`. Ensure that the current working directory in the terminal is `code`.

2. Execute the following command:
```
make publish
```

This command will:

- Run unit tests (ignore any warnings related to the sklearn version).
- Perform quality checks, including linting and code formatting. The `batch.py` file will be reformatted using "black".
- Build a Docker container and image.
- Create a bucket in AWS.
- Run the integration tests, which will output the predicted credit classification and print the contents of AWS (input and output files).
- Print the contents of the `publish.sh` file.

## Pre-Commit Hooks

1. Open the terminal, activate the virtual environment containing the libraries mentioned in the `Pipfile`, and ensure that the current working directory is `code`.

2. Initialize an empty Git repository:
```
git init
```

3. Install pre-commit hooks:
```
pre-commit install
```

4. Check the status of your files:
```
git status
```

5. Add all the files:
```
git add .
```

6. Commit the files:
```
git commit -m 'initial commit'
```

If all tests pass, your commit will be successful. If some tests fail, the pre-commit hook will reformat the necessary files. Repeat steps 4-6 to add the files modified by pre-commit.
