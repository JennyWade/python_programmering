from importlib.resources import path
import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3

class clean_csv:
    def import_csv(self, db):
        self.db = pd.read_csv(path)

    import_csv("C:/Users/jenny/Documents/GitHub/python_programmering/Assignment/vaccin_covid.csv")