# coding: utf-8
from frenchholidays.data import PublicHolidays, GeneralHolidays
from frenchholidays.utils import HolidayTools


def main():
    publicholiday = PublicHolidays()
    generalholiday = GeneralHolidays()

    holidaytools = HolidayTools(generalholiday.get_general_holiday_as_df(),
                                publicholiday.get_public_holiday_as_df())

    print(holidaytools.get_list_of_general_holidays_description())

    print(holidaytools.get_list_of_public_holidays_description())


if __name__ == '__main__':
    main()
