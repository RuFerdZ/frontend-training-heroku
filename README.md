## Run Locally (Without Docker)   

### Install and configure postgres SQL

1. Download and Install PostgresSQL locally and set it up to run with a superuser
2. In Ubuntu, `sudo su - postgres` to switch to postgres user
3. `psql`
4. `CREATE DATABASE demoappdb;`
5. `CREATE USER demoapp WITH PASSWORD 'demopassword';`
6. `GRANT ALL PRIVILEGES ON DATABASE "demoappdb" to demoapp;`
7. `ALTER ROLE miriam CREATEDB;`
8. `\q`
9. If you put the settings differently, change `settings.py` accordingly

### Setup Django

1. You need python 3.7.0 or higher
2. `pip -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
5. `python manage.py runserver` 


## Boilerplate Features

* Custom User profile (you need to implement the registration service method)
* Email/SMS sending integrated
* For 2-step verification, check `intrview` codebase


## Postman Collection

(https://www.getpostman.com/collections/0fc70999e1d207602b34)[https://www.getpostman.com/collections/0fc70999e1d207602b34]

Updated collection - 07-07-2022: (https://www.getpostman.com/collections/da6ea8d568271eae71da)[https://www.getpostman.com/collections/da6ea8d568271eae71da]