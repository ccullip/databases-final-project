COMP 373 – Final Project
*A admin portal web app for doctors viewing diabetic patients' records*

## Code structure overview

## Set up
#### Data insertion
- Run src/schema.sql in MySQL to initialize database (admin_portal) and the necessary tables in MySQL.

- Ensure your MySQL's settings has the **only_full_group_by** turned off.

```
mysql >   SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```

- Open src/AdminPortal in IntelliJ or Eclipse and run the project to insert the data.

  - Insert.java takes in 2 program parameters, your **MySQL password** and **MySQL username**. Passing in your username is optional if you're using "root" as your username.

  - Run Insert.java to add data to database (Warning, this may take a while!)

#### Django Environment
- Django requires a virtual environment to run itself locally.

- First navigate to website folder.

```
$   cd project/website/website/
```

- Within website/ path, create and enter your virtual environment.

```
$   python3 -m venv env   # to create a virtual environment
$   . env/bin/activate    # activate/enter virtual environment
```

- Then you must install the necessary dependencies for this web app to run.

```
$   pip3 install django
$   pip install --upgrade pip   # pip will probably be out of date, so upgrade it
$   pip install pygal
$   env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip3 install mysqlclient
```

Then you should be ready to deploy our website! :)

## Deploying Web App
- After completing the set up above, deploying is easy:

  - Navigate to project/website/website/ directory.

  - Run server (default port is 8000)

  ```
  $   python3 manage.py runserver <optional port number>
  ```

  - Quit the server whenever with ^C **(CONTROL - C)**

  - To close the virtual environment:

  ```
  $   deactivate
  ```

*Created by Charlotte Cullip and Stephanie Angulo.*
