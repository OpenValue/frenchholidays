import pandas as pd


class HolidayTools(object):
    def __init__(self, general_holidays_df, public_holidays_df):
        self.general_holidays_df = general_holidays_df
        self.public_holidays_df = public_holidays_df

    def get_list_of_academies(self):
        return sorted(self.general_holidays_df.loc[:, "location"].unique().tolist())

    def get_list_of_zones(self):
        return sorted(self.general_holidays_df.loc[:, "zones"].unique().tolist())

    def get_max_annee_scolaire(self, zones=None):

        return

    def __get_annee_scolaire_from_date_range(self, input_date, current_start_date, current_end_date,
                                             current_annee_scolaire, next_start_date, next_annee_scolaire):
        if (input_date >= current_start_date) & (input_date <= current_end_date):
            return current_annee_scolaire
        elif (input_date > current_end_date) & (input_date < next_start_date):
            return next_annee_scolaire

    def get_annee_scolaire(self, input_date_str=None):
        input_date = pd.to_datetime(input_date_str) if input_date_str is not None else pd.Timestamp.now()

        dates_per_annee_scolaire = self.general_holidays_df \
            .groupby("annee_scolaire", as_index=False) \
            .agg({"start_date": "min", "end_date": "max"}) \
            .sort_values("start_date")

        dates_per_annee_scolaire.loc[:, "next_annee_scolaire"] = dates_per_annee_scolaire.loc[:, "annee_scolaire"] \
            .shift(-1)
        dates_per_annee_scolaire.loc[:, "next_start_date"] = dates_per_annee_scolaire.loc[:, "start_date"] \
            .shift(-1)

        dates_per_annee_scolaire.loc[:, "input_date_annee_scolaire"] = dates_per_annee_scolaire \
            .apply(lambda x: self.__get_annee_scolaire_from_date_range(input_date, x["start_date"], x["end_date"],
                                                                       x["annee_scolaire"], x["next_start_date"],
                                                                       x["next_annee_scolaire"]),
                   axis=1)

        annee_scolaire = dates_per_annee_scolaire[~dates_per_annee_scolaire["input_date_annee_scolaire"].isnull()]
        return annee_scolaire.loc[:, "input_date_annee_scolaire"].values[0]

    def get_composition_of_zones(self, annee_scolaire=None, zone=None):
        if annee_scolaire is None:
            annee_scolaire = self.get_annee_scolaire()

        composition = self.general_holidays_df[self.general_holidays_df["annee_scolaire"] == annee_scolaire]. \
            groupby("zones")["location"].agg(lambda x: sorted(list(set(x)))).to_dict()

        if zone is None:
            return composition
        else:
            return {zone: composition[zone]}

    def get_list_of_general_holidays_description(self):
        return self.__get_list_of_description(self.general_holidays_df)

    def get_list_of_public_holidays_description(self):
        return self.__get_list_of_description(self.public_holidays_df)

    def __get_list_of_description(self, df):
        if df is not None:
            df_list = sorted(df.loc[:, "description"].unique().tolist())
        else:
            df_list = None

        return df_list

    def is_general_holidays(self, input_date_str=None, input_zone=None):
        input_date = pd.to_datetime(input_date_str) if input_date_str is not None else pd.Timestamp.now()
        mask = (self.general_holidays_df["start_date"] <= input_date) \
               & (self.general_holidays_df["end_date"] >= input_date)

        if input_zone is not None:
            mask = mask & (self.general_holidays_df["zones"] == input_zone)

        return self.general_holidays_df[mask].to_dict()

    def is_public_holidays(self, input_date_str=None):
        input_date = pd.to_datetime(input_date_str) if input_date_str is not None else pd.Timestamp.now()
        mask = (self.public_holidays_df["start_date"] == input_date)

        return self.public_holidays_df[mask].to_dict()

    def __get_next_event_from_date_and_df(self, df, event_name, date_field="start_date", input_date_str=None):
        input_date = pd.to_datetime(input_date_str) if input_date_str is not None else pd.Timestamp.now()
        mask = (df[date_field] >= input_date)

        next_event = df[mask] \
            .sort_values(date_field).head(1) \
            .to_dict(orient="records")[0]

        next_event["time_to_next_" + event_name] = (next_event[date_field] - input_date).days

        return next_event

    def __get_last_event_from_date_and_df(self, df, event_name, date_field="start_date", input_date_str=None):
        input_date = pd.to_datetime(input_date_str) if input_date_str is not None else pd.Timestamp.now()
        mask = (df[date_field] <= input_date)

        last_event = df[mask] \
            .sort_values(date_field, ascending=False).head(1) \
            .to_dict(orient="records")[0]

        last_event["time_to_next_" + event_name] = -(last_event[date_field] - input_date).days

        return last_event

    def get_next_public_holidays(self, input_date_str=None):
        next_public_holidays = self.__get_next_event_from_date_and_df(df=self.public_holidays_df,
                                                                      event_name="public_holidays",
                                                                      date_field="start_date",
                                                                      input_date_str=input_date_str)

        return next_public_holidays

    def get_last_public_holidays(self, input_date_str=None):
        last_public_holidays = self.__get_last_event_from_date_and_df(df=self.public_holidays_df,
                                                                      event_name="public_holidays",
                                                                      date_field="start_date",
                                                                      input_date_str=input_date_str)

        return last_public_holidays

    def get_next_general_holidays(self, input_date_str=None, zone=None):
        next_general_holidays = self.__get_next_event_from_date_and_df(
            df=self.general_holidays_df[self.general_holidays_df["zones"] == zone],
            event_name="general_holidays",
            date_field="start_date",
            input_date_str=input_date_str)

        return next_general_holidays

    def get_last_general_holidays(self, input_date_str=None, zone=None):
        last_general_holidays = self.__get_last_event_from_date_and_df(
            df=self.general_holidays_df[self.general_holidays_df["zones"] == zone],
            event_name="general_holidays",
            date_field="end_date",
            input_date_str=input_date_str)

        return last_general_holidays
