from importlib.resources import path
from argparse import ArgumentParser
import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3

class CleanCSV:

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def add_and_fill_vacc_col(self):
        self.df["JohnsonAndJohnson"] = self.df["vaccines"].str.contains("Johnson&Johnson") 
        self.df["OxfordAstraZeneca"] = self.df["vaccines"].str.contains("Oxford/AstraZeneca") 
        self.df["Sinovac"] = self.df["vaccines"].str.contains("Sinovac") 
        self.df["SputnikV"] = self.df["vaccines"].str.contains("Sputnik V") 
        self.df["Moderna"] = self.df["vaccines"].str.contains("Moderna") 
        self.df["SinopharmBeijing"] = self.df["vaccines"].str.contains("Sinopharm/Beijing") 
        self.df["Covaxin"] = self.df["vaccines"].str.contains("Covaxin") 
        self.df["CanSino"] = self.df["vaccines"].str.contains("CanSino") 
        self.df["Abdala"] = self.df["vaccines"].str.contains("Abdala") 
        self.df["PfizerBioNTech"] = self.df["vaccines"].str.contains("Pfizer/BioNTech") 
        self.df["QazVac"] = self.df["vaccines"].str.contains("QazVac") 
        self.df["EpiVacCorona"] = self.df["vaccines"].str.contains("EpiVacCorona") 
        self.df["Soberana02"] = self.df["vaccines"].str.contains("Soberana02") 
        self.df["SinopharmHayatVax"] = self.df["vaccines"].str.contains("Sinopharm/HayatVax") 
        self.df["RBDDimer"] = self.df["vaccines"].str.contains("RBD-Dimer") 
        self.df["SinopharmWuhan"] = self.df["vaccines"].str.contains("Sinopharm/Wuhan") 
                
    def remove_columns(self, col_todrop):
        #Remove columns
        self.col_todrop = self.df.drop(col_todrop, axis=1, inplace=True)
        self.df = self.df.fillna(0)

    def createDatabase(self, db, name):
        self.db = db
        self.db = sqlite3.connect(db)
        self.name = name
        self.df.to_sql(self.name, self.db)
      

class DatabaseManagement:
    def connect_to_db(self, db):
        self.db = db
        self.db = sqlite3.connect(db)
        cur = self.db.cursor()

    def