from Inlämning.Classes import CleanCSV

if __name__ == "__main__":
    covid = CleanCSV("vaccin_covid.csv")

    covid._split_to_list('vaccines')

    covid._remove(["vaccines", "daily_vaccinations_raw"])

    covid._createDatabase('covid', 'Covid.db')
    