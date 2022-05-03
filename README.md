# simpleboun
A simple registration database system for CmpE321 project 2.

To run the application;

1)  Install:

    Django==3.2.3
    environ
    django_environ
    mysql_connector_python
    mysqlclient
    django-crispy-forms
    mysql-server==8.0

2) Run your mysql server, preferably on 127.0.0.1/3306

3) Create a database on your mysql server.

4) Create .env file containing the host, user, password and database-name information to connect to the mysql server from the app.
   The file should look like:
   
   MYSQL_HOST=127.0.0.1
   MYSQL_USER=root
   MYSQL_PASSWORD=<root-password>
   MYSQL_DATABASE=<database-name>

5) add .env into directories
   simpleboun
   simpleboun/simpleboundb
   simpleboun/registration
  
6) run the following command while in simpleboun directory:
  python createdb.py
  
7) run the following command while in simpleboun directory:
  python manage.py migrate
  
8) run the following command while in simpleboun directory:
  python manage.py runserver
  
9) go to the address your application server is running on in your browser
