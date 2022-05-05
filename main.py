import csv
import os
import sys
from math import floor

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# credentials needed for the sql connection
hostname = os.getenv("MY_HOSTNAME")
myusername = os.getenv('MY_USERNAME')
mypassword = os.getenv('MY_PASSWORD')
db = os.getenv('MY_DB')

mydb = mysql.connector.connect(host=hostname, username=myusername, password=mypassword, database=db)
cursor = mydb.cursor()
try:
    cursor.execute("SHOW TABLES")
    results = cursor.fetchall()
    myresults = [item[0] for item in results]
    if "institution" in myresults:
        print("table exists")
        cursor.execute("DROP TABLE institution")
    if "team" in myresults:
        cursor.execute("DROP TABLE team")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS institution (id int, name varchar(150), city varchar(40), state "
        "varchar(40), country varchar(40))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS team (id int, advisor varchar(40), problem varchar(1), ranking "
        "int, institution_id int)")
    mydb.commit()
except Error as e:  # if there's an error catch it and print it
    print("ERROR: " + str(e))

rankings = {"Unsuccessful": 0,
            "Successful Participant": 1,
            "Honorable Mention": 2,
            "Meritorious": 3,
            "Finalist": 4,
            "Outstanding Winner": 5}

#  set up CSV
filename = str(sys.argv[1])
print("Reading " + filename)
myfile = open(filename)  # load first arg
mycsv = csv.DictReader(myfile)  # read file

#  look for the Columns we need in the file
createNewFiles = False
requiredCols = ["Institution", "Team", "City", "State", "Country", "Advisor", "Problem", "Ranking"]
myDict = {}  # dictionary to use to get the value our csv uses for our required column values
for col in mycsv:
    for i in range(0, len(col)):  # check if the csv file columns have names that include our required names
        for j in range(0, len(requiredCols)):
            if requiredCols[j].lower() in list(col)[i].lower():
                myDict[requiredCols[j]] = list(col)[i]
                break
    break  # only want header values

if len(requiredCols) == len(myDict):  # we have all our columns
    createNewFiles = True
if not createNewFiles:  # we dont have all our columns
    print("The columns of the input file are too ambiguous to be used. Please use a file that "
          "includes aptly named columns for Institution, Team Number, City, State/Province, Country, Advisor, "
          "Problem, and Ranking.")
else:
    instID = 0  # id value to increment
    institutions = {}  # dictionary to keep track of institutions
    lines = list(mycsv)
    numlines = len(lines)
    printstatement = "Inserting values "
    linecount = 0
    for col in lines:
        instrow = []
        teamrow = []
        instval = col[myDict['Institution']]  # institution name
        if instval not in institutions:  # only append if it's a new unique name
            institutions[instval] = instID  # create dictionary entry
            instrow.append(instID)  # add the values
            try:
                cursor.execute('INSERT INTO institution (id, name, city, state, country)'
                               'values (' + str(instID) + ',"'
                               + instval + '","'
                               + col[myDict['City']] + '","'
                               + col[myDict['State']] + '","'
                               + col[myDict['Country']] + '")')
            except Error as e:  # if there's an error catch it and print it
                print("ERROR: " + str(e))
            instID += 1  # increment id number
        try:
            cursor.execute('INSERT INTO team (id, advisor, problem, ranking, institution_id)'
                           'values (' + col[myDict['Team']] + ',"'
                           + col[myDict['Advisor']] + '","'
                           + col[myDict['Problem']] + '","'
                           + str(rankings[col[myDict['Ranking']]]) + '",'
                           + str(institutions[instval]) + ')')
        except Error as e:  # if there's an error catch it and print it
            print("ERROR: " + str(e))
        linecount += 1
        percentdone = (linecount / numlines) * 100
        sys.stdout.write('\r' + printstatement + str(floor(percentdone)) + "%")  # overwrite last statement
    mydb.commit()
    cursor.close()
    print("\nSuccessfully inserted info into databases")

