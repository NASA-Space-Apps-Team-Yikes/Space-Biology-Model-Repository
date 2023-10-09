# Space Biology Model Repository

This repository contains various resources and modules for the Space Biology Model project. Here is a brief overview of the directory structure:

- `requirements.txt`: Contains the Python dependencies required for this project.
- `data`: Directory for storing data related to the project.
- `database`: Contains scripts for database connection and verification.
    - `db_connector.py`: Script for connecting to the PostgreSQL database.
    - `Verify RDS Database.py`: Script for verifying the connection to the RDS database.
- `docs`: Contains documentation related to the project.
- `LICENSE`: The license for this project.
- `models`: Directory for storing trained machine learning models.
- `preprocessing`: Contains scripts for preprocessing the data.
- `training`: Contains scripts for training the machine learning models.
    - `Read data fom RDS.py`: Script for reading data from the RDS database for training.
- `webapp`: Contains the web application for the project.
    - `app.py`: The main script for running the web application.
    - `templates`: Contains HTML templates for the web application.
        - `about.html`: Template for the About page.
        - `analysis.html`: Template for the Analysis page.
        - `index.html`: Template for the Home page.
        - `upload.html`: Template for the Upload Data page.
