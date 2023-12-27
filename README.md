# Flask web application for user registration with implemented SQL database backend and mail support
This repository contains the source code for a template web application for a local scouts group in Luxembourg. The main functionality is the registration/application of new users with their personal information. This information, if passing backend validation, is stored inside a SQL user database. Additionally, if a registration is successful, an email is sent to a defined email address containing the information of the registered user as an `.xlsx` file.

>[!NOTE]
>This website is in Luxembourgish. Most of the functionality, however, is self-explanatory.

# Usage
Clone the repo. Inside the project directory, run the following command in your terminal.

`flask --app flaskr run --debug`

## Make sure Python is installed.

-   Run `python` in your terminal
-   if not installed: <https://www.python.org/downloads/>

## Make sure Flask is installed.
`pip install Flask`

## Configure your email settings

In `__init__.py`, I use the following to configure my email settings.

```
    import configparser

    config = configparser.ConfigParser()
    config.read('flaskr/config.ini')

    app.config['MAIL_SERVER'] = config.get('DEFAULT', 'MAIL_SERVER')
    app.config['MAIL_PORT'] = config.getint('DEFAULT', 'MAIL_PORT')
    app.config['MAIL_USERNAME'] = config.get('DEFAULT', 'MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config.get('DEFAULT', 'MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = config.getboolean('DEFAULT', 'MAIL_USE_TLS', fallback=True)
    app.config['MAIL_USE_SSL'] = config.getboolean('DEFAULT', 'MAIL_USE_SSL', fallback=False)
```

1. Create a configuration file
 `mkdir config.ini`
 
2. Inside `__init__.py`, replace `config.read('flaskr/config.ini')` with the path to your own configuration file. **Or**, change the configuration directly:

    `app.config['MAIL_PORT'] = 2525`
    `...`

# Overview
The webpage contains different routes: Home, Umellen (*apply*), Kontakt(*contact*).

## The Home route
This route contains the name of the scouts group as well as their different "branches" or age categories.

## The Umellen (or *apply*) route
This route allows parents to register their child using a multi-page form.

## The Kontact (or *contact*) route
This route contains a leaflet map specifying the location of the scouts house on a map as well as the exact address.

Example: 
Parent 1 registers his/her contact details during the registration of his/her child. The contact details are saved inside the database. A year later, the same Parent 1 registers his or her second child. I don't want the contact details of Parent 1 to be saved twice inside my database! So I had to implement some SQL logic to check if the contact details entered in the form match a parent in the database. If yes, only a new connection in a junction table (using a unique composite key) should be made. 

# Development criteria
The crux of this project was the implementation of the SQL database backend. Currently, scout registrations are logged in a `.xlsx` file. New members fill out a paper form and the information is then entered inside the exisiting `.xlsx` file. Because transitioning to a database is not trivial, I also implemented mail support allowing form data to be sent as a `.xlsx` file to the responsible person. This allows it to be easily copy-pasted into the existing file. I used MailTrap during development.

## Database implementation
By far the most challenging. Form data collects information on the registered child and on its legal representative(s). For both, database duplications should be avoided. This means that:

- parents cannot register a child twice 
- there should not be duplicated parent entries for parents registering two childs 

Careful backend form validation and a junction table using a composite key was thus necessary.

## Form implementation
Very challenging too. The form needed was extremely large. Instead of creating on large form requiring users to scroll on the web page, I wanted to implement a multi-page form. It turned out that this is not trivial at all in Flask, as individual sub-form submissions trigger a page reload. A very trivial problem appeared. If a user proceeded from one subform to the next and backend validation failed, all the entered data was gone and the user would have to type everything again.

In Flask, solving this was not trivial at all. I managed to solve this but in a rather unelegant way. Multi-page forms are something I've come across dozens of times, so there must be some other way to do this. Perhaps this is much easier in other web development frameworks.


# Debugging
During development, an `ImportError: cannot import name 'JSONEncoder' from 'flask.json'` caused problems. The issue was solved by downgrading flask `pip install flask==2.2.5`, as suggested [here](https://stackoverflow.com/questions/76570896/importerror-cannot-import-name-jsonencoder-from-flask-json).

