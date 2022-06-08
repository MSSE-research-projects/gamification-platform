# Gamification-platform

This project aims to provide a platform where students can give feedback to 
their classmates' presentation assignments, with specially designed gamification 
elements to encourage students' engagement. It is based on Django 3.2 and MySQL 
server database.

# Developer Environment setup

1. Install required python packages

   It is suggested to create a brand-new virtual environment then `pip install -r requirements.txt`.
   
   For MAC users, replace `mysqlclient==2.1.0` with `PyMySQL==1.0.2` in `requirements.txt` file. Then add following lines to `config/__init__.py`

   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

2. Install MySQL server locally

   MySQL server's version should be >= 5.7, as is required by `mysqlclient` package.

3. Configure MySQL server

    - Run `sudo mysql_secure_installation` if first-time installation of MySQL

      It will take you through a series of prompts where you can make some 
      changes to your MySQL installation's security options.
    
    - Add a user `dbuser`

      Run `sudo mysql` to get into mysql shell. Then execute the following SQL
      statements to add a user named `dbuser` with password as `dbuser`.

      ```sql
      CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'dbuser';
      GRANT ALL PRIVILEGES ON *.* TO 'dbuser'@'localhost' WITH GRANT OPTION;
      ```

      After creating new user `dbuser`, we can login into mysql shell as this
      new user with command `mysql -u dbuser -p` and then enter the password.
    
    - Create a database `dev`

      Run `sudo mysql` to get into mysql shell as `root` user (or `mysql -u dbuser -p`
      as `dbuser`). Then execute the following SQL statement to add a new
      database called `dev`.

      ```sql
      CREATE DATABASE dev;
      ```

      You can check the available databases with SQL statement:

      ```sql
      SHOW DATABASES;
      ```

      or check the tables inside `dev` database with SQL statement:

      ```sql
      USE dev;
      SHOW TABLES;
      ```

4. Test if everything is working

    Run command `python manage.py runserver`

# Contributing

## Python formatter

We use `autopep8` to format our code. Properly set your IDE to automatically 
format the python file before saving.

## Commit message convention

The commit message should be structured as follows, quoted from [here](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(optional scope): <description>

[optional body]

[optional footer(s)]
```

The types are specified as followed:
- **fix**: patches a bug in the codebase.
- **feat**: introduces a new feature to the codebase.
- **style**: codebase changes related to code format problems
- **test**: add test code
- **doc**
- **chore**
- **refactor**
- ......

## Commit as often as possible

Break down the code you implemented into small parts and commit as soon as you
finish a small part.

**DO NOT** squash all the work into one commit!

## Multiple authors for a commit

If there are multiple authors for a commit (for example, pair-programming), follow the instructions from this
[link](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors#creating-co-authored-commits-on-the-command-line)
here to add co-authors.