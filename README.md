COMP 373 – Final Project
*A admin portal web app for doctors viewing diabetic patients' records*

## Code structure overview
docs/ <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ~ *miscellaneous documents* ~<br>
project/ <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;src/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AdminPortal/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;schema.sql<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;website/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;website/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;manage.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;website/<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;admin_portal/<br>
README.md <br>

### **docs/**
Contains milestone write ups and other related documents that were turned in.

### **project/**
Where all the code exists!

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **project/src/**
Contains the scheme.sql file and AdminPortal directory used for MySQL/JDBC driver.

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **project/website/website/**
Contains all website related code. Most important/non-boilerplate code exist in [project/website/website/admin_portal](project/website/website/admin_portal) (backend) and [project/website/website/templates](project/website/website/templates) (HTML/front end).

## Set up
##### Data insertion
- Run [project/src/schema.sql](project/src/schema.sql) in MySQL to initialize database (admin_portal) and the necessary tables in MySQL.

- Ensure your MySQL's settings has the **only_full_group_by** turned off.

```
mysql >   SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```

- Open [project/src/AdminPortal/](project/src/AdminPortal) in IntelliJ or Eclipse and run the project to insert the data.

  - Insert.java takes in 2 program parameters, your **MySQL password** and **MySQL username**. Passing in your username is optional if you're using "root" as your username.

  - Run Insert.java to add data to database (Warning, this may take a while!)

#### Django Environment
- Django requires a virtual environment to run itself locally.

- First navigate to website folder.

```
$   cd project/website/website/
```

- Within [project/website/website/](project/website/website), create and enter your virtual environment.

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

  - Navigate to [project/website/website/](project/website/website) directory.

  - Run server (default port is 8000)

  ```
  $   python3 manage.py runserver <optional port number>
  ```
- Navigate to [127.0.0.1:8000/home/](http://127.0.0.1:8000/home/) and play around with the different features!

  - Quit the server whenever with ^C **(CONTROL - C)**

  - To close the virtual environment:

  ```
  $   deactivate
  ```
  
## Features
- Filter on through the patients' data with the different inputs on the page.

- Click on specific rows to get more information on the patient

- Look at pie charts/bar graphs analyzing data with the specific filters you used.

- Search for specific patients used the search bar by entering in their patient id number
 
  - *limitation!!* you must use the button "**Search for Patient**", rather than pressing enter, or else the query will not work properly. <br>
*Created by Charlotte Cullip and Stephanie Angulo.*
