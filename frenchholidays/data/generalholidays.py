import requests
import pandas as pd
from pandas.io.json import json_normalize


class GeneralHolidays(object):

    def __init__(self):
        self.url = "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-calendrier-scolaire&rows=10000"
        self.referentiel_geographique_url = "https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-referentiel-geographique&rows=10000"

    def get_general_holiday_as_df(self):
        req = requests.get(self.url)
        holidays_df = pd.DataFrame(req.json()["records"])

        holidays_df = holidays_df.merge(json_normalize(holidays_df.loc[:, "fields"]), left_index=True, right_index=True)
        for col in ["record_timestamp", "start_date", "end_date"]:
            holidays_df.loc[:, col] = pd.to_datetime(holidays_df.loc[:, col])

        holidays_df = holidays_df.drop(["fields", "datasetid", "record_timestamp", "recordid"], axis=1)
        holidays_df.loc[:, "duration"] = (
                holidays_df.loc[:, "end_date"] - holidays_df.loc[:, "start_date"]).dt.days
        holidays_df = holidays_df.sort_values(
            ["zones", "annee_scolaire", "description", "location", "population", "duration"],
            ascending=[1, 1, 1, 1, 1, 0])
        holidays_df = holidays_df.drop_duplicates(
            subset=["zones", "annee_scolaire", "description", "location", "population"], keep="first")

        return holidays_df

    def get_referentiel_geographique_as_df(self, start=None):
        start = 0
        referentiel_geographique_url = self.referentiel_geographique_url + "&start=" + str(start)
        req = requests.get(referentiel_geographique_url)
        current_req_dict = req.json()
        num_records = current_req_dict["nhits"]
        for i in range(num_records / 1000):
            pass
        ref_geo_df = pd.DataFrame(req.json()["records"])

        return ref_geo_df
