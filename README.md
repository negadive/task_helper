
# Task Helper

When you lazy enough to do simple repetitive stuff with your project tasks.


## Features

- Make branch from your task


## Installation

Install dependancies with pip

```bash
  pip install -r requirements.txt
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PIVOTAL_TRACKER_PROJECT_ID`

`PIVOTAL_TRACKER_TOKEN`

`CSV_PROJECT_REPO_DIR`

`REPO_DIR`

## Usage/Examples

### Help
```bash
python main.py --help
```

### Register project
```bash
python main.py register-project $PROJECT_ID $PROJECT_NAME
```
Examples:

```bash
python main.py register-project 4264 disco
```

### Make branch
```bash
python main.py mkb $TASK_ID
```
```bash
python main.py mkb --project=$PROJECT_ID $TASK_ID
```
Examples:

```bash
python main.py mkb 6969
```
```bash
python main.py mkb --project=4264 6969
```
## Running Tests

To run tests, run the following command

```bash
  pytest
```

