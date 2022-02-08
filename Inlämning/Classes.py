from importlib.resources import path
from matplotlib.pyplot import connect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as sql
import altair as alt
import altair_viewer

class CleanCSV:

    def __init__(self, csv_path): 
        #Reads csv provided
        self.df = pd.read_csv(csv_path)

    def _add_and_fill_vacc_col(self): 
        #Adding all unique vaccines found in 'vaccines' col with rows returning boolean value
        self.df["Johnson_and_Johnson"] = self.df["vaccines"].str.contains("Johnson&Johnson") 
        self.df["Oxford_AstraZeneca"] = self.df["vaccines"].str.contains("Oxford/AstraZeneca") 
        self.df["Sinovac"] = self.df["vaccines"].str.contains("Sinovac") 
        self.df["Sputnik_V"] = self.df["vaccines"].str.contains("Sputnik V") 
        self.df["Moderna"] = self.df["vaccines"].str.contains("Moderna") 
        self.df["Sinopharm_Beijing"] = self.df["vaccines"].str.contains("Sinopharm/Beijing") 
        self.df["Covaxin"] = self.df["vaccines"].str.contains("Covaxin") 
        self.df["CanSino"] = self.df["vaccines"].str.contains("CanSino") 
        self.df["Abdala"] = self.df["vaccines"].str.contains("Abdala") 
        self.df["Pfizer_BioNTech"] = self.df["vaccines"].str.contains("Pfizer/BioNTech") 
        self.df["QazVac"] = self.df["vaccines"].str.contains("QazVac") 
        self.df["EpiVacCorona"] = self.df["vaccines"].str.contains("EpiVacCorona") 
        self.df["Soberana02"] = self.df["vaccines"].str.contains("Soberana02") 
        self.df["Sinopharm_HayatVax"] = self.df["vaccines"].str.contains("Sinopharm/HayatVax") 
        self.df["RBD_Dimer"] = self.df["vaccines"].str.contains("RBD-Dimer") 
        self.df["Sinopharm_Wuhan"] = self.df["vaccines"].str.contains("Sinopharm/Wuhan") 

    def remove_columns(self, col_todrop):
        #Remove columns
        self.col_todrop = self.df.drop(col_todrop, axis=1, inplace=True)
        self.df = self.df.fillna(0)

    def createDatabase(self, db, name):
        #Creates our database using name provided
        self.db = db
        self.db = sql.connect(db)
        self.name = name
        self.df.to_sql(self.name, self.db)
      

class DatabaseManagement:
    def __init__(self, name):
        #Connect to database and create cursor
        self.db = sql.connect(name)
        self.cur = self.db.cursor()

    def create_tables(self):
        #Creating all new tables for a relational database
        #Also creating 'dummy' table with the data I need for each table
        self.cur.execute("""CREATE TABLE Daily_Vaccine_Data(
                        iso_code text,
                        date text,
                        country text,
                        daily_vaccinations integer,
                        daily_vaccinations_per_million,
                        PRIMARY KEY(iso_code, date)
                        FOREIGN KEY(country) REFERENCES Country_Source(country))""")
        self.cur.execute("""CREATE TABLE Country_Source(
                        country text PRIMARY KEY, 
                        source_name text, 
                        source_website text)""")
        self.cur.execute("""CREATE TABLE Country_Vaccines(
                        country text PRIMARY KEY, Johnson_and_Johnson integer, 
                        Oxford_AstraZeneca integer, Sinovac integer,
                        Sputnik_V integer, Moderna integer, 
                        Sinopharm_Beijing integer, Covaxin integer, 
                        CanSino integer, Abdala integer, 
                        Pfizer_BioNTech integer, QazVac integer, 
                        EpiVacCorona integer, Soberana02 integer, 
                        Sinopharm_HayatVax integer, RBDDimer integer, 
                        Sinopharm_Wuhan integer,
                        FOREIGN KEY(country) REFERENCES Country_Source(country))""")
        self.cur.execute("""CREATE TABLE Country_Total(
                        iso_code text,
                        date text,
                        country text,
                        total_vaccinations integer, 
                        people_vaccinated integer, 
                        people_fully_vaccinated integer,
                        total_vaccinations_per_hundred real, 
                        people_vaccinated_per_hundred real, 
                        people_fully_vaccinated_per_hundred real,
                        PRIMARY KEY (iso_code, date)
                        FOREIGN KEY(country) REFERENCES Country_Source(country))""")
        self.cur.execute("""CREATE TABLE Daily_Vaccine_Data_data AS SELECT
                        iso_code, date, country, daily_vaccinations, daily_vaccinations_per_million
                        FROM CovidVacc""")
        self.cur.execute("""CREATE TABLE Country_Source_data
                        AS SELECT DISTINCT country, source_name, source_website 
                        FROM CovidVacc""")
        self.cur.execute("""CREATE TABLE Country_vaccines_data AS SELECT DISTINCT country, 
                        Johnson_and_Johnson, Oxford_AstraZeneca, Sinovac, Sputnik_V, Moderna, 
                        Sinopharm_Beijing, Covaxin, CanSino, Abdala, Pfizer_BioNTech, QazVac, 
                        EpiVacCorona, Soberana02, Sinopharm_HayatVax, RBD_Dimer, Sinopharm_Wuhan 
                        FROM CovidVacc""")
        self.cur.execute("""CREATE TABLE Country_Total_data AS SELECT DISTINCT iso_code, date, country, total_vaccinations, people_vaccinated,
                        people_fully_vaccinated, total_vaccinations_per_hundred, people_vaccinated_per_hundred,
                        people_fully_vaccinated_per_hundred FROM CovidVacc""")
        self.db.commit()
    
    def insert_data_to_tables(self):
        #Inserting all the data from the 'dummy' tables into my actual ones
        self.cur.execute("""INSERT INTO Country_Source SELECT * FROM Country_Source_data""")
        self.cur.execute("""INSERT INTO Daily_Vaccine_Data SELECT * FROM Daily_Vaccine_Data_data""")
        self.cur.execute("""INSERT INTO Country_Vaccines SELECT * FROM Country_vaccines_data""")
        self.cur.execute("""INSERT INTO Country_Total SELECT * FROM Country_Total_data """)
        self.db.commit()

    def drop_tables(self):
        #Dropping all the 'dummy' tables along with the original table containing all data
        self.cur.execute("DROP TABLE Daily_Vaccine_Data_data")
        self.cur.execute("DROP TABLE Country_Source_data")
        self.cur.execute("DROP TABLE Country_vaccines_data")
        self.cur.execute("DROP TABLE Country_total_data")
        self.cur.execute("DROP TABLE CovidVacc")
        self.db.commit()

class VisualiseData:
    def __init__(self, name):
        #Connect to database
        self.db = sql.connect(name)
        self.cur = self.db.cursor()  
        
    def extract_desc_daily_data(self):
        #Create dataframe from query
        self.results = pd.read_sql_query("""SELECT date, country, daily_vaccinations FROM Daily_Vaccine_Data WHERE Country LIKE 'Sweden' AND date like '2021%'""", self.db)
    
    def plot_query(self):
        #Plot above dataframe
        plt.plot('date', 'daily_vaccinations', data=self.results)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        plt.xticks(np.linspace(0,221,8), months)
        plt.title('Sweden daily vaccinations between Jan-Aug 2021')
        plt.show()

    def plot_query_2(self):
        self.chart = alt.Chart(self.results).mark_line().encode(
        x = 'date',
        y='daily_vaccinations').show()
        
    def vaccine_country(self):
        self.results2 = pd.read_sql_query("""SELECT COUNT (Moderna) FROM Country_Vaccines WHERE Moderna = '1'""", self.db)
        print(self.results2)
    