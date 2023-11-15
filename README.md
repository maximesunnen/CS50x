# CS50-project
Repository for MY final project of [Harvard's CS50 course](https://pll.harvard.edu/course/cs50-introduction-computer-science).

Developing a webpage for a local scouts group using [Flask](https://flask.palletsprojects.com/en/3.0.x/). The webpage is currently only available in luxembourgish.

The webpage should contain different routes: 
-   Home: name of the scouts, branches, maybe pictures, ...
-   Umellen (*apply*): where parents can register their child, a large form
-   Kontakt (*contact*): a leaflet map indicating the location and the address, maybe FAQ section
-   Cheffen/Persounen (*people*): people working for the scout group with maybe their contact data (thinking of Bootstrap cards, but looks bootstrappy)
-   Shop: display items, price and location where they can be purchased.

The crux of this project is the "Apply" route, where parents can register their child by filling out a form (child details, parent details, etc) and the data is saved in a SQL database using SQLite3.

-   I want a multi-page form because a large form requiring the user to scroll is not user-friendly imo. This was not trivial at all.
-   The form data should be saved in my db but duplications should be prevented. 

Example: 
Parent 1 registers his/her contact details during the registration of his/her child. The contact details are saved inside the database. A year later, the same Parent 1 registers his or her second child. I don't want the contact details of Parent 1 to be saved twice inside my database! So I had to implement some SQL logic to check if the contact details entered in the form match a parent in the database. If yes, only a new connection in a junction table (using a unique composite key) should be made. 

-   currently, scout registrations are in logged in an excel file. Because transitioning to a database is not trivial I also implemented a feature where form data is saved into an Excel file and sent via email to the dedicated person. The excel data can then be copy-pasted to their excel file. I tested this using MailTrap, and it works.

# Demo
Clone the repo and run the following command in your terminal (make sure you're inside the project directory).

`flask --app flaskr run --debug`

## Make sure Python is installed.

-   Check with `python` in your terminal
-   if not installed: <https://www.python.org/downloads/>

## Make sure Flask is installed.
`$ pip install Flask`

## Configure your email settings

In `__init__.py`, I use the following to configure my email settings.

    import configparser

    config = configparser.ConfigParser()
    config.read('flaskr/config.ini')

    app.config['MAIL_SERVER'] = config.get('DEFAULT', 'MAIL_SERVER')
    app.config['MAIL_PORT'] = config.getint('DEFAULT', 'MAIL_PORT')
    app.config['MAIL_USERNAME'] = config.get('DEFAULT', 'MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config.get('DEFAULT', 'MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = config.getboolean('DEFAULT', 'MAIL_USE_TLS', fallback=True)
    app.config['MAIL_USE_SSL'] = config.getboolean('DEFAULT', 'MAIL_USE_SSL', fallback=False)

Change the configuration file:

-   replace `config.read('flaskr/config.ini')` with the path to your own configuration file. 

Or change the configuration directly:

    `app.config['MAIL_PORT'] = 2525`
    `...`


