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

Please let me know if you need any further assistance!
