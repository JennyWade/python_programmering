import Classes

if __name__ == "__main__":
    covid_vaccine = Classes.CleanCSV("Inlämning/vaccin_covid.csv")

    covid_vaccine.add_and_fill_vacc_col()
    covid_vaccine.remove_columns(["vaccines", "daily_vaccinations_raw"])

    covid_vaccine.createDatabase('CovidVacc.db', 'CovidVacc')

    covid_vaccine_db = Classes.DatabaseManagement('CovidVacc.db')
    covid_vaccine_db.create_tables()
    covid_vaccine_db.insert_data_to_tables()
    covid_vaccine_db.drop_tables()