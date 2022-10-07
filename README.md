# Vehicle-Maintenance-Manager

An application to make keeping track of vehicle maintenance easier.

## Setting Up a Development Environment

### Virtual Environment

#### Creation

To begin, it's advisable to work within a virtual environment. To set up the virtual environment for this project, navigate to the project directory in a terminal shell and enter

```shell
python3 -m venv venv
```

More about venv: <https://www.infoworld.com/article/3239675/virtualenv-and-venv-python-virtual-environments-explained.html>

#### Activation

This will create a new directory inside your project folder named `venv` containing the virtual environment.

Before you launch Flask and begin working on the project, you'll need to execute this command from within the project directory to activate the virtual environment:

```shell
source venv/bin/activate
```

#### Installing Pip Packages

Once you have activated the virtual environment, you can install all of the Python package dependencies in your environment using pip. You only need to do this when you first create your virtual environment, or whenever a new dependency is added to the project. To install these, simply invoke the following command:

```shell
pip install -r requirements.txt
```

Once all the dependencies are installed, you are ready to start Flask and begin developing.

### Launching the App (Development)

While you are working, you can launch the Flask app in debug mode. Flask will reload each time you save changes to the project files, and helpful messages and debugging information will print to the terminal while in debug mode.

```shell
Flask --debug run
```

#### Database

When you run Flask for the first time, or if you delete the database file, the init sequence will create an SQLite database named `database.sqlite` in the project directory. The tables for this database are definied in `dbconfig.py`.
