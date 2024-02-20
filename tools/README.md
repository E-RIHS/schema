# Tools for managing E-RIHS schemas

Python tools to facilitate JSON Schema management.

## General advise on Python virtual environments

Different Python projects will require different Python packages. When you have multiple projects side-by-side, it could happen that these require different versions of the same packages, which could lead to issues. Therefore, it is good practice to run each project in a different *virtual environment*, each with its own set of dependencies.

Note: for all the commands below, we assume they are executed in a contemporary version of Linux, with Python (version >3.10) installed. Possibly they also work under MacOS without changes, but this has not been tested. In principle, all these should also work in Windows, but the syntax will be slightly different. If you insist on using an inferior OS, you're on your own ;-).

When you run these tools for the first time, you will need to create a virtual environment. This __needs to be done once__.

```shell
python -m venv venv         # Creating a virtual environment for our application
```

From now on you can enter the virtual environment with:

```shell
source venv/bin/activate    # Activating the virtual environment
```

In an active virtual environment, you can proceed with installing the external dependencies and libraries from PyPi with `pip`. All dependencies in this project are collected in the `requirements.txt` file. The command below only needs to be invoked (1) after the initial virtual environment is created, and (2) whenever the requirements change.

```shell
pip install -r requirements.txt  # Installing requirements
```

After creating and activating the virtual environment, and installing the dependencies, all is ready to use the tools.

When done, you can deactivate the virtual environment with:

```shell
deactivate
```

In automations (e.g. systemd service units), it is possible to run the tools within their virtual environment invoking the `python` executable in the virtual environment. Example:

```shell
./venv/bin/python update_schemas.py
```

## `update_schemas.py`

The `update_schemas.py` script:

- retrieves a list of JSON Schemas on Github
- retrieves the individual JSON Schema
- validates the schema against the JSON Schema draft (that is embedded in $schema)
- extracts the object type and version
- [TODO] creates or updates the schema in Cordra (latest versions only)
- [TODO] performs version management in Cordra

