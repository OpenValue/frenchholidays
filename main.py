# coding: utf-8
from frenchholidays.data import PublicHolidays, GeneralHolidays
from frenchholidays.utils import HolidayTools


def main():
    publicholiday = PublicHolidays()
    generalholiday = GeneralHolidays()

    holidaytools = HolidayTools(generalholiday.get_general_holiday_as_df(),
                                publicholiday.get_public_holiday_as_df())

    annee_scolaire = holidaytools.get_annee_scolaire()
    print(annee_scolaire)

    composition = holidaytools.get_composition_of_zones()
    print(composition)

    print(holidaytools.get_next_public_holidays())

    print(holidaytools.get_next_general_holidays(zone="Zone A"))


if __name__ == '__main__':
    main()
