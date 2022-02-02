import Classes

if __name__ == "__main__":
    covid = Classes.CleanCSV("Inlämning/vaccin_covid.csv")

    covid.add_and_fill_vacc_col()
    covid.new_combined_col()
    covid.remove_columns(["iso_code", "date", "vaccines", "daily_vaccinations_raw"])

    covid.createDatabase('CovidVacc.db', 'CovidVacc')