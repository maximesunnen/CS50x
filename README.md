# CS50-project
Repository for MY final project of [Harvard's CS50 course](https://pll.harvard.edu/course/cs50-introduction-computer-science).

Developing a webpage for a local scouts group using [Flask](https://flask.palletsprojects.com/en/3.0.x/). The webpage is currently only in luxembourgish. I will have to do the french transltion too and if there's maybe an automated way of translating a website I will add more.

The webpage should contain different routes: 
-   Home: name of the scouts, branches, maybe pictures, ...
-   Umellen (*apply*): where parents can register their child, a large form
-   Kontakt (*contact*): a leaflet map indicating the location and the address, maybe FAQ section
-   Cheffen/Persounen (*people*): people working for the scout group with maybe their contact data (thinking of Bootstrap cards, but looks bootstrappy)
-   Shop: display items, price and location where they can be purchased.

The backend contains a SQLite3 database where information from the forms is saved. **Important:** will have to check how this works with data protection. Probably need help from somebody who knows how to deal with "sensitive" information. A disclaimer that the data will be stored is most likely not sufficient. What is the standard for protecting data?

# Demo
Clone the repo and run the following command in your terminal (make sure you're inside the project directory).

`flask --app flaskr run --debug`

Make sure Python is installed.

-   Check with `python` in your terminal
-   if not installed: <https://www.python.org/downloads/>

Make sure Flask is installed.
`$ pip install Flask`




