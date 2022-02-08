import Classes

if __name__ == "__main__":
    covid_vaccine = Classes.CleanCSV("Inlämning/vaccin_covid.csv")

    covid_vaccine._add_and_fill_vacc_col()
    covid_vaccine.remove_columns(["vaccines", "daily_vaccinations_raw"])

    covid_vaccine.createDatabase('CovidVacc.db', 'CovidVacc')

    covid_vaccine_db = Classes.DatabaseManagement('CovidVacc.db')
    covid_vaccine_db.create_tables()
    covid_vaccine_db.insert_data_to_tables()
    covid_vaccine_db.drop_tables()

    covid_vacc = Classes.VisualiseData('CovidVacc.db')
    covid_vacc.extract_desc_daily_data()
    #covid_vacc.plot_query()
    covid_vacc.plot_query_2()
    #covid_vacc.vaccine_country()

  