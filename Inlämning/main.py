import Classes

if __name__ == "__main__":
    covid_vaccine = Classes.CleanCSV("Inlämning/vaccin_covid.csv")

    covid_vaccine.add_and_fill_vacc_col()
    covid_vaccine.remove_columns(["vaccines", "daily_vaccinations_raw"])

    covid_vaccine.createDatabase('CovidVacc.db', 'CovidVacc')