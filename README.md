# This project is written with three different programming models:

1- Simple coding based on preliminary principles.
2- Based on the function.
3- Based on the class.
It has also been tried to follow the principles of clean coding as much as possible.
The main goal was not only to learn how each model works but also improve my skills while writing readable and maintainable codes.

# Extracting and Analysis Used Car Data from TrueCar

This code extracts used car data from the TrueCar website using BeautifulSoup and saves it to a MySQL database. It then retrieves the data from the database and writes it to a CSV file. Finally, it uses the extracted data to train a decision tree model and make predictions.

## Installation

To run this code, you need to have the following libraries installed:

- csv
- re
- itertools
- mysql.connector
- requests
- bs4 (BeautifulSoup)
- sklearn (tree module)

You can install these libraries using pip by running the following command:

```
pip install csv re mysql-connector-python requests beautifulsoup4 scikit-learn
```

## Setup Database

Before running the code, you need to set up a MySQL database. You can follow these steps:

1. Install MySQL if you haven't already: [MySQL Installation Guide](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)
2. Create a new database called "MLLearning".
3. Create a new table called "car_information" with columns for ID, Name, Year, Price, Miles, and Color.

## Code Execution

To execute the code:

1. Set up the MySQL database as described above.
2. Make sure you have installed the necessary libraries.
3. Replace the host, user, and password values in the code with your MySQL connection details.
4. Run the code.

Note: The code assumes that you have permission to create databases and tables on your MySQL server. If you don't, you may need to modify the code accordingly.

Once the code has finished executing, it will print the collected car data for debugging and analysis purposes, as well as the predicted class label for a new data point.

## Full Explain Of Code

This code performs several tasks related to extracting used car data from a website, storing it in a MySQL database, writing it to a CSV file, and utilizing machine learning techniques.

1. Importing necessary modules: The code starts by importing various modules such as csv, re, mysql.connector, requests, BeautifulSoup, and sklearn.tree.

2. Creating a list of URLs: The code initializes an empty list `list_site` and then uses a for loop to generate a list of URLs for each page of listings on the TrueCar website. The URL is constructed using a formatted string with the page number.

3. Initializing lists for storing car data: The code initializes empty lists `names`, `prices`, `miles`, `years`, and `colors`.

4. Extracting car data using BeautifulSoup: The code loops through each URL in `list_site` and sends a GET request to retrieve the HTML content of the page. It then uses BeautifulSoup to parse the HTML content and find all the car listings. For each car listing, it extracts specific information such as name, price, mileage, year, and color. It cleans up the extracted data using regular expressions and appends them to their corresponding lists.

5. Printing out the collected car data: After extracting the car data, the code prints the lists of names, years, prices, mileage, and colors for debugging and analysis purposes.

6. Writing data to a MySQL database: The code establishes a connection with a MySQL database using the `mysql.connector` module. It creates a new database called "MLLearning" if it doesn't already exist and sets it as the active database. Then, it creates a table called "car_information" with columns for ID, name, year, price, mileage, and color. It uses a loop and SQL queries to insert the collected car data into the table. Finally, it commits the changes to the database and closes the connection.

7. Writing data from the database to a CSV file: The code establishes a connection with the MySQL database again and executes a SELECT query to fetch all the data from the "car_information" table. It opens a CSV file named "output.csv" in write mode and writes the fetched data to the file row by row using the `csv.writer` module. Finally, it closes the connections.

8. Implementing machine learning (Decision Tree Classifier) on the data: The code imports the csv and tree modules from the sklearn library. It initializes empty lists `x` and `y`. Then, it opens the "output.csv" file, reads the data as a CSV, and skips the first row (headers). It loops through the rows and appends the second, third, and fourth column values to the `x` list as a list of floats. It also appends the value from the first column to the `y` list. Next, it creates a DecisionTreeClassifier object, fits the model using the `x` and `y` data, and makes predictions for new data. Finally, it prints the predicted class label for the new data point.

Note: This code assumes that you have already set up a MySQL database and have the required Python modules installed. Also, make sure to provide the correct database credentials and adjust the code as per your requirements.

Please let me know if you need any further assistance!
