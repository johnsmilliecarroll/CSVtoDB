A program that takes an input csv for a math competition and creates a database, which it then queries for statistical information on the competition results.

### Requirements:

Download dotenv and mysql connector.

    % pip install python-dotenv
    % pip install mysql-connector-python

Install mySQL if you don't have it already. Create an empty database, then create a .env file in the same folder as main.py, with the following set up:

    MY_HOSTNAME = "yourhost"
    MY_USERNAME = "yourusername"
    MY_PASSWORD = "yourpassword"
    MY_DB = "yourdatabasename"

## How to use:

In the same folder as main.py, place the csv file you'd like to read. Next, run main.py via command line with the name of the file as the first argument.

So if the file you would like to parse is named 2015.csv, this is what you should run.

    % python main.py 2015.csv

If everything is set up correctly this should create an institution table and a team table in your database. This program can be ran repeatedly without creating repeated values.

Next, run method.py.

    % python method.py

This will create a text file with the following information:

* The average number of teams entered per institution
* An ordered list of the institutions that entered the most teams, including the number of teams that they entered (ordered by number of teams)
* A list of all institutions whose team(s) earned 'Outstanding' rankings (ordered by institution name)
* A list of all US teams who received 'Meritorious' ranking or better.
