from importlib.resources import path
from argparse import ArgumentParser
import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3

class clean_csv:
    def __init__(self):
        path = "/Users/jenny.wade@schibsted.com/Documents/GitHub/python_programmering/Assignment/vaccin_covid.csv"
        self.df = pd.read_csv(path)

    def _split(self):
        #split vaccine column and get a list of unique values

    def _remove(self):
        #Remove columns
        self.df = self.df.drop(["vaccines", "daily_vaccinations_raw"], axis=1, inplace=True)


if __name__ == "__main__":
