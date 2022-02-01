from importlib.resources import path
from argparse import ArgumentParser
import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3

class CleanCSV:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        
    def _split_to_list(self, column):
        #split vaccine column and get a list of unique values
        self.column = column
        split = self.df[self.column].str.split(",", expand=True)
        vl0 = split[0].str.split(",")
        vl1 = split[1].str.split(",")
        vl2 = split[2].str.split(",")
        vl3 = split[3].str.split(",")
        vl4 = split[4].str.split(",")
        vl5 = split[5].str.split(",")
        vl6 = split[6].str.split(",")
        vl = pd.concat([vl0,vl1,vl2,vl3,vl4,vl5,vl6])
        vl = vl.drop_duplicates()
 
    
    def _add_columns(self):
        self.df["JohnsonAndJohnson"] = self.df["vaccines"].str.contains("Johnson&Johnson") * 1
        self.df["OxfordAstraZeneca"] = self.df["vaccines"].str.contains("Oxford/AstraZeneca") * 1
        self.df["Sinovac"] = self.df["vaccines"].str.contains("Sinovac") * 1
        self.df["SputnikV"] = self.df["vaccines"].str.contains("Sputnik V") * 1
        self.df["Moderna"] = self.df["vaccines"].str.contains("Moderna") * 1
        self.df["SinopharmBeijing"] = self.df["vaccines"].str.contains("Sinopharm/Beijing") * 1
        self.df["Covaxin"] = self.df["vaccines"].str.contains("Covaxin") * 1
        self.df["CanSino"] = self.df["vaccines"].str.contains("CanSino") * 1
        self.df["Abdala"] = self.df["vaccines"].str.contains("Abdala") * 1
        self.df["PfizerBioNTech"] = self.df["vaccines"].str.contains("Pfizer/BioNTech") * 1
        self.df["QazVac"] = self.df["vaccines"].str.contains("QazVac") * 1
        self.df["EpiVacCorona"] = self.df["vaccines"].str.contains("EpiVacCorona") * 1
        self.df["Soberana02"] = self.df["vaccines"].str.contains("Soberana02") * 1
        self.df["SinopharmHayatVax"] = self.df["vaccines"].str.contains("Sinopharm/HayatVax") * 1
        self.df["RBDDimer"] = self.df["vaccines"].str.contains("RBD-Dimer") * 1
        self.df["SinopharmWuhan"] = self.df["vaccines"].str.contains("Sinopharm/Wuhan") * 1

    def _remove(self, col_todrop):
        #Remove columns
        self.col_todrop = self.df.drop(col_todrop, axis=1, inplace=True)

    def _createDatabase(self, db, name):
        self.db = db
        self.db = sqlite3.connect(db)
        self.name = name
        self.df.to_sql(self.name, self.db)
        cur = self.db.cursor()