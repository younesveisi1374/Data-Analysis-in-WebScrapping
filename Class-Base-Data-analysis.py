import csv
import re
from itertools import zip_longest

import mysql.connector
import requests
from bs4 import BeautifulSoup
from sklearn import tree


class CarDataExtractor:
    def __init__(self):
        self.list_site = []
        self.names = []
        self.prices = []
        self.miles = []
        self.years = []
        self.colors = []

    def extract_car_data(self):
        for i in range(1, 31):
            string = f"https://www.truecar.com/used-cars-for-sale/listings/?page={i}"
            i += 1
            self.list_site.append(string)

        for url in self.list_site:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            cars = soup.find_all("div", {"class": "card-content order-3 vehicle-card-body"})

            for ad in cars:
                name = ad.find("span", {"class": "truncate"})
                mile = ad.find("div", {"data-test": "vehicleMileage"})
                price = ad.find("div", {"data-test": "vehicleCardPricingBlockPrice"})
                year = ad.find("span", {"class": "vehicle-card-year text-xs"})
                color = ad.find("div", {"class": "vehicle-card-location mt-1 truncate text-xs"})

                result0 = name.get_text().split(" ")
                result1 = price.get_text().split("$")
                result2 = mile.get_text().split(" ")
                result3 = year.get_text()
                result4 = color.get_text().split(" ")
                reges1 = re.sub(r"(,)", ".", result1[1])
                reges2 = re.sub(r"(,)", ".", result2[0])

                self.names.append(result0[0])
                self.prices.append(float(reges1))
                self.miles.append(float(reges2))
                self.years.append(int(result3))
                self.colors.append(result4[0])

    def write_data_to_database(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password="2236541")
        cursor = mydb.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS MLLearning")
        cursor.execute("USE MLLearning")

        sql_table = "CREATE TABLE car_information (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255) NOT NULL, Year VARCHAR(255)  NOT NULL, Price FLOAT  NOT NULL, Miles FLOAT  NOT NULL, Color VARCHAR(255) NOT NULL)"
        cursor.execute(sql_table)

        for name, year, price, mile, color in zip_longest(
            self.names, self.years, self.prices, self.miles, self.colors
        ):
            sql_column = f"INSERT INTO car_information (Name, Year, Price, Miles, Color) VALUES ('{name}', '{year}', '{price}', '{mile}', '{color}')"
            cursor.execute(sql_column)

        mydb.commit()
        mydb.close()

    def write_data_to_csv(self):
        mydb = mysql.connector.connect(
            host="localhost", user="root", password="2236541", database="MLLearning"
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM car_information")
        data = cursor.fetchall()

        with open("output.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([i[0] for i in cursor.description])
            for row in data:
                writer.writerow(row)

        cursor.close()
        mydb.close()

    def ml_learning(self):
        x = []
        y = []

        with open("output.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                x.append([float(val) for val in row[2:5]])
                y.append(row[1])

        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(x, y)

        new_data = [[2023, 11.500, 123.572]]
        answer = clf.predict(new_data)

        print(answer[0])


car_data_extractor = CarDataExtractor()
car_data_extractor.extract_car_data()
car_data_extractor.write_data_to_database()
car_data_extractor.write_data_to_csv()
car_data_extractor.ml_learning()
