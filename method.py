import csv
import os
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# credentials needed for the sql connection
hostname = os.getenv("MY_HOSTNAME")
myusername = os.getenv('MY_USERNAME')
mypassword = os.getenv('MY_PASSWORD')
db = os.getenv('MY_DB')


query1 = "SELECT AVG(teamcount) from (SELECT COUNT(id) as teamCount from team GROUP BY institution_id) as subtable"

query2 = "SELECT name, COUNT(t.id) as numEntered from institution i JOIN team t ON i.id = institution_id GROUP BY institution_id ORDER BY numEntered DESC"

query3 = "SELECT DISTINCT name from institution i LEFT JOIN team t ON i.id = institution_id WHERE ranking " \
                                    "= 5 ORDER BY name "

query4 = "SELECT DISTINCT name, ranking from institution i LEFT JOIN team t ON i.id = institution_id WHERE ranking " \
                                             ">= 3 AND country = 'USA' ORDER BY ranking"


f = open('results.txt', 'w')

f.write('Average number of teams entered per institution: ')

mydb = mysql.connector.connect(host=hostname, username=myusername, password=mypassword, database=db)
cursor = mydb.cursor()
try:
    cursor.execute(query1)
    results = cursor.fetchall()
    myresults = [item[0] for item in results]
    for result in myresults:
        f.write(str(result))
except Error as e:  # if there's an error catch it and print it
    print("ERROR: " + str(e))

f.write('\n\nInstitutions who entered the most teams:\n\n')

try:
    cursor.execute(query2)
    results = cursor.fetchall()
    for result in results:
        myline = str(result[0]) + ", " + str(result[1]) + "\n"
        f.write(myline)
except Error as e:  # if there's an error catch it and print it
    print("ERROR: " + str(e))

f.write('\n\nInstitutions whose teams received a ranking of Outstanding:\n\n')

try:
    cursor.execute(query3)
    results = cursor.fetchall()
    myresults = [item[0] for item in results]
    for result in myresults:
        f.write(str(result))
        f.write('\n')
except Error as e:  # if there's an error catch it and print it
    print("ERROR: " + str(e))

f.write('\n\nUS Institutions whose teams received a ranking of Meritorious or higher:\n\n')

try:
    cursor.execute(query4)
    results = cursor.fetchall()
    for result in results:
        myranking = ""
        if result[1] == 3:
            myranking = "MERITORIOUS"
        elif result[1] == 4:
            myranking = "FINALIST"
        elif result[1] == 5:
            myranking = "OUTSTANDING"
        myline = str(result[0]) + ", " + myranking + "\n"
        f.write(myline)
except Error as e:  # if there's an error catch it and print it
    print("ERROR: " + str(e))

cursor.close()
f.close()

print("Successfully created filename results.txt")