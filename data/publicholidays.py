# coding: utf-8
from datetime import date
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


class PublicHolidays(object):
    def __init__(self, include_alsace=False, start_year=None, end_year=None):

        self.include_alsace = include_alsace
        if start_year is None:
            now = datetime.now().date()
            start_year = (now - relativedelta(years=5)).year

        if end_year is None:
            now = datetime.now().date()
            end_year = (now + relativedelta(years=5)).year

        self.range = list(range(start_year, end_year + 1))

    def get_public_holiday_as_df(self):
        res_dict = {}
        for year in self.range:
            res_dict[year] = self.get_public_holiday_for_year(year)
        df = pd.DataFrame(res_dict).reset_index().rename(columns={"index": "description"})
        df = pd.melt(df, id_vars=['description'], value_vars=self.range).rename(
            columns={"variable": "year", "value": "start_date"})
        df.loc[:, "start_date"] = pd.to_datetime(df.loc[:, "start_date"])
        df.loc[:, "year"] = df.loc[:, "year"].astype(int)
        df.loc[:, "is_alsace_specific"] = df.loc[:, "description"].map(
            lambda x: 1 if x in ["Saint Étienne", "Vendredi Saint"] else 0)

        return df

    def get_public_holiday_for_year(self, year):
        res = {
            "Jour de l'an": self.__jour_de_lan(year),
            "Fête du travail": self.__fete_du_travail(year),
            "Victoire des alliés": self.__victoire_des_allies(year),
            "Fête Nationale": self.__fete_nationale(year),
            "Assomption": self.__assomption(year),
            "Toussaint": self.__toussaint(year),
            "Armistice": self.__armistice(year),
            "Noël": self.__noel(year),
            "Lundi de Pâques": self.__lundi_de_paques(year),
            "Ascension": self.__ascension(year),
            "Lundi de Pentecôte": self.__lundi_de_pentecote(year),
        }

        if self.include_alsace:
            res["Vendredi Saint"] = self.__vendredi_saint(year)
            res["Saint Étienne"] = self.__saint_etienne(year)

        return res

    def __paques(self, year):
        a = year % 19
        b = year // 100
        c = year % 100
        d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
        e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
        f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
        month = f // 31
        day = f % 31 + 1

        return date(year, month, day)

    def __lundi_de_paques(self, year):
        delta = timedelta(days=1)
        return self.__paques(year) + delta

    def __vendredi_saint(self, year):
        delta = timedelta(days=2)
        return self.__paques(year) - delta

    def __ascension(self, year):
        delta = timedelta(days=39)
        return self.__paques(year) + delta

    def __lundi_de_pentecote(self, year):
        delta = timedelta(days=50)
        return self.__paques(year) + delta

    def __jour_de_lan(self, year):
        return date(year, 1, 1)

    def __fete_du_travail(self, year):
        return date(year, 5, 1)

    def __victoire_des_allies(self, year):
        return date(year, 5, 8)

    def __fete_nationale(self, year):
        return date(year, 7, 14)

    def __toussaint(self, year):
        return date(year, 11, 1)

    def __assomption(self, year):
        return date(year, 8, 15)

    def __armistice(self, year):
        return date(year, 11, 11)

    def __noel(self, year):
        return date(year, 12, 25)

    def __saint_etienne(self, year):
        return date(year, 12, 26)
