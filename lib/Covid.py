

from prettytable import PrettyTable
import mysql.connector
import requests

if __name__ == "__main__":
    pass


class GetCovid19:
    def __init__(self,  HOSTNAME, USERNAME, PASSWORD, COVID_19):
        self.__COVID_19 = COVID_19

        self.__db = mysql.connector.connect(
            host=HOSTNAME,
            user=USERNAME,
            password=PASSWORD
        )
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS telepy")
        self.__cursor.execute("USE telepy")

        self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS Countries (id INT AUTO_INCREMENT PRIMARY KEY, Country VARCHAR(64), CountryCode VARCHAR(3), Slug VARCHAR(64), NewConfirmed INT, TotalConfirmed INT, NewDeaths INT, TotalDeaths INT, NewRecovered INT, TotalRecovered INT, Date VARCHAR(64))")
        self.__get_covid_info()

    def menu(self):
        exit = False
        while not exit:
            choice = int(input(
                "1. Sort by TotalConfirmed \n2. Sort by NewConfirmed\n3. Sort by country name\n0 Exit\n ===>> "))
            if choice == 1:
                self. __sort_by_total_confirmed()
            elif choice == 2:
                self.__sort_by_new_confirmed()
            elif choice == 3:
                self.__sort_by_country_name()
            elif choice == 0:
                exit = True
                print("Bye!")
            else:
                print("Wrong choice.")

    def __get_covid_info(self):
        response = requests.get(self.__COVID_19)
        self.__covid_data = response.json()

        self.__cursor.execute("TRUNCATE Countries")
        for item in self.__covid_data['Countries']:
            sql = "INSERT INTO Countries (Country, CountryCode, Slug, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered, Date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (item['Country'], item['CountryCode'], item['Slug'], item['NewConfirmed'], item['TotalConfirmed'],
                   item['NewDeaths'], item['TotalDeaths'], item['NewRecovered'], item['TotalRecovered'], item['Date'])
            self.__cursor.execute(sql, val)
        self.__db.commit()

    def __sort_by_total_confirmed(self):

        self.__cursor.execute(
            "SELECT  Country, TotalConfirmed, Date FROM Countries ORDER BY TotalConfirmed ASC")

        result = self.__cursor.fetchall()
        if result != None:
            
            table = PrettyTable()
            table.field_names = ["Country: ", "TotalConfirmed: ", "Date: "]
            
            for item in result:
                table.add_row(item)
            print(table)

      
    def __sort_by_new_confirmed(self):
        self.__cursor.execute(
            "SELECT Country, NewConfirmed, Date FROM Countries ORDER BY NewConfirmed ASC")
        result = self.__cursor.fetchall()
        if result != None:
            
            table = PrettyTable()
            table.field_names = ["Country: ","NewConfirmed: ", "Date: "]
            
            for item in result:
                table.add_row(item)
            print(table)

    def __sort_by_country_name(self):
        self.__cursor.execute(
            "SELECT  Country, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered FROM Countries ORDER BY Country")
        result = self.__cursor.fetchall()
        if result != None:
            table = PrettyTable()
            table.field_names = ["Country:", "NewConfirmed:","TotalConfirmed:", "NewDeaths:", "TotalDeaths:", "NewRecovered:", "TotalRecovered:", ]
            
            for item in result:
                table.add_row(item)
            print(table)


   
