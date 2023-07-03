# Extracting Used Car Data from TrueCar
import csv
import re
from itertools import zip_longest

import mysql.connector
import requests
from bs4 import BeautifulSoup
from sklearn import tree

def extract_car_data(list_site):
    # Initialize lists for storing car data
    names = []
    prices = []
    miles = []
    years = []
    colors = []

    # Loop through each URL and extract car data using BeautifulSoup
    for i in list_site:
        url = f"{i}"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        cars = soup.find_all("div", {"class": "card-content order-3 vehicle-card-body"})

        # Extract individual car information by searching for specific HTML tags and attributes
        for ad in cars:
            name = ad.find("span", {"class": "truncate"})
            mile = ad.find("div", {"data-test": "vehicleMileage"})
            price = ad.find("div", {"data-test": "vehicleCardPricingBlockPrice"})
            year = ad.find("span", {"class": "vehicle-card-year text-xs"})
            color = ad.find("div", {"class": "vehicle-card-location mt-1 truncate text-xs"})

            # Clean up extracted data using regular expressions
            result0 = name.get_text().split(" ")
            result1 = price.get_text().split("$")
            result2 = mile.get_text().split(" ")
            result3 = year.get_text()
            result4 = color.get_text().split(" ")
            reges1 = re.sub(r"(,)", ".", result1[1])
            reges2 = re.sub(r"(,)", ".", result2[0])

            # Append cleaned up data to corresponding lists
            names.append(result0[0])
            prices.append(float(reges1))
            miles.append(float(reges2))
            years.append(int(result3))
            colors.append(result4[0])

    # Return the collected car data
    return names, years, prices, miles, colors

def write_data_to_database(names, years, prices, miles, colors):
    # Establish connection with MySQL database
    mydb = mysql.connector.connect(host="localhost", user="root", password="2236541")
    cursor = mydb.cursor()

    # Create a new database called MLLearning (if it doesn't already exist) and use it
    cursor.execute("CREATE DATABASE IF NOT EXISTS MLLearning")
    cursor.execute("USE MLLearning")

    # Create a table called "car_information" with columns for ID, name, year, price, miles, and color
    sql_table = "CREATE TABLE car_information (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255) NOT NULL, Year VARCHAR(255)  NOT NULL, Price FLOAT  NOT NULL, Miles FLOAT  NOT NULL, Color VARCHAR(255) NOT NULL)"
    cursor.execute(sql_table)

    # Iterate over lists of car data using zip_longest (which allows for missing values)
    for name, year, price, mile, color in zip_longest(names, years, prices, miles, colors):
        # Create an SQL query to insert a new row into the "car_information" table with the current values
        sql_column = f"INSERT INTO car_information (Name, Year, Price, Miles, Color) VALUES ('{name}', '{year}', '{price}', '{mile}', '{color}')"

        # Execute the SQL query using cursor.execute()
        cursor.execute(sql_column)

    # Commit changes to the database and close the connection
    mydb.commit()
    mydb.close()

def write_data_to_csv():
    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="2236541", database="MLLearning"
    )

    # Execute the MySQL query
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM car_information")

    # Fetch the data
    data = cursor.fetchall()

    # Write the data to the CSV file
    with open("output.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow([i[0] for i in cursor.description])
        # Loop through data and write each row to the CSV file
        for row in data:
            writer.writerow(row)

    # Close the connections
    cursor.close()
    mydb.close()

def ml_learning_from_csv():
    # Create empty lists for x and y data
    x = []
    y = []

    # Open the output.csv file and read the data as a CSV
    with open("output.csv", "r") as csvfile:
        # Create a reader object for the CSV data
        reader = csv.reader(csvfile)
        # Skip the first row (headers) in the CSV data
        next(reader)
        # Loop through the rows in the CSV data
        for row in reader:
            # Append the values from columns 2, 3, and 4 to the x list as a list of floats
            x.append([float(val) for val in row[2:5]])
            # Append the value from column 1 to the y list
            y.append(row[1])

    # Create a new DecisionTreeClassifier object from sklearn
    clf = tree.DecisionTreeClassifier()
    # Fit the decision tree model using the x and y data
    clf = clf.fit(x, y)

    # Create a new set of data to predict using the trained model
    new_data = [[2023, 11.500, 123.572]]
    # Predict the class label for the new data point
    answer = clf.predict(new_data)

    # Return the predicted class label for the new data point
    return answer[0]

# Create a list of URLs for each page of listings on TrueCar (2 pages in this example)
list_site = []
for i in range(1, 31):
    string = f"https://www.truecar.com/used-cars-for-sale/listings/?page={i}"
    i += 1
    list_site.append(string)

# Extract car data from TrueCar
names, years, prices, miles, colors = extract_car_data(list_site)

# Write car data to database
write_data_to_database(names, years, prices, miles, colors)

# Write car data from database to CSV file
write_data_to_csv()

# Perform machine learning on car data from CSV
prediction = ml_learning_from_csv()

# Print out the collected car data for debugging and analysis purposes
print(names)
print(years)
print(prices)
print(miles)
print(colors)
print(prediction)
