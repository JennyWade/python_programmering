import Classes

if __name__ == "__main__":
    covid = Classes.CleanCSV("Inlämning/vaccin_covid.csv")

    covid._split_to_list('vaccines')

    covid._remove(["vaccines", "daily_vaccinations_raw"])

    covid._createDatabase('covid.db', 'covid.db')