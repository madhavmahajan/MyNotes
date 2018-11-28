## MyNotes

#### Requirements
1. Python 3.7.1
2. Django 2.1.3
3. PostgreSQL database

#### Setting up the project
1. Checkout the project
2. Install all 3rd party Python modules,
    ```
    # pip install requirements.txt
    ```
3. Update PostgreSQL database credentials in notes/settings.py
4. Execute following commands to migrate models in db,
    ```
    # python manage.py makemigrations mynotes
    # python manage.py sqlmigrate mynotes 0001
    # python manage.py migrate
    ```
5. Execute command to setup databse with default records,
    ```
    # python manage.py setup
    ```
6. Run Django server,
    ```
    # python manage.py runserver
    ```
7. Access URL, http://127.0.0.1:8000/mynotes
