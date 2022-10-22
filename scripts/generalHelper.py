"""
A script for General helper.
"""

# imports
import os
import logging
import defaults as defs
import geopy
import holidays
import datetime
import pandas as pd


class generalHelper():
    """
    A General helper class.
    """

    def __init__(self, fromThe: str) -> None:
        """
        The General helper initializer

        Parameters
        =--------=
        fromThe: string
            The file importing the General helper

        Returns
        =-----=
        None: nothing
            This will return nothing, it just sets up the distance
            manipulation script.
        """
        try:
            self.nigeria_holiday = holidays.Nigeria()
            # setting up logger
            self.logger = self.setup_logger(defs.log_path +
                                            'general_helper_root.log')
            self.logger.info('\n    #####-->    General helper ' +
                             f'logger for {fromThe}    <--#####\n')
            print('General helper in action')
        except Exception as e:
            print(e)

    def setup_logger(self, log_path: str) -> logging.Logger:
        """
        A function to set up logging

        Parameters
        =--------=
        log_path: string
            The path of the file handler for the logger

        Returns
        =-----=
        logger: logger
            The final logger that has been setup up
        """
        try:
            # Check whether the log path exists or not
            if not os.path.exists(defs.log_path):
                # Create a new log directory if it does not exist
                os.makedirs(defs.log_path)
                print("Storage directory for logs created!")

            # getting the log path
            log_path = log_path

            # adding logger to the script
            logger = logging.getLogger(__name__)
            print(f'--> {logger}')
            # setting the log level to info
            logger.setLevel(logging.DEBUG)
            # setting up file handler
            file_handler = logging.FileHandler(log_path)

            # setting up formatter
            formatter = logging.Formatter(
                "[%(asctime)s] [%(name)s] [%(funcName)s] [%(levelname)s] " +
                "--> [%(message)s]")

            # setting up file handler and formatter
            file_handler.setFormatter(formatter)
            # adding file handler
            logger.addHandler(file_handler)
            print(f'logger {logger} created at path: {log_path}')
        except Exception as e:
            logger.error(e, exec_info=True)
            print(e)
        finally:
            # return the logger object
            return logger

    def distance(self, row):
        """
        A method to calculate distance given a row

        Parameters
        =--------=
        row: string
            The path of the file handler for the logger

        Returns
        =-----=
        logger: logger
            The final logger that has been setup up

        """
        return geopy.distance.distance((row.Trip_Origin_lat,
                                        row.Trip_Origin_lng),
                                       (row.Trip_Destination_lat,
                                        row.Trip_Destination_lon)).km

    def imputeNull(self, x) -> str:
        """
        A method to strip the first nd second element in a list

        Parameters
        =--------=
        x: string or datetime
            The row of the data frame

        Returns
        =-----=
        str: string
            The first element of the string or None if nothing is there
        """
        try:
            return str(x).split(' ')[1]
        except Exception as e:
            self.logger.error(e, exec_info=True)
            print(e)
            return 'None'

    def check_holiday(self, date: str, country: str = 'NG') -> str:
        """
        A method to get dates

        Parameters
        =--------=
        date: string or datetime
            The date to check for
        country: str
            The country to chekc the holiday

        Returns
        =-----=
        str: string
            The holiday or None if there is no holiday
        """
        ng_holidays = holidays.country_holidays('NG')
        try:
            return ng_holidays.get(date)
        except Exception as e:
            self.logger.error(e, exec_info=True)
            print(e)
            return 'None'

    def check_for_holiday(self, order_time: datetime):
        """
        A method to get dates

        Parameters
        =--------=
        date: string or datetime
            The date to check for
        country: str
            The country to check the holiday

        Returns
        =-----=
        str: string
            The holiday or None if there is no holiday
        """
        try:
            return order_time.date() in self.nigeria_holiday
        except Exception as e:
            self.logger.error(e, exec_info=True)
            print(e)
            return 'error'

    def add_holiday_feature(self, df: pd.DataFrame,
                            date_col: str = "Trip Start Date"):
        try:
            df["Holiday"] = df[date_col].apply(
                lambda x: self.check_for_holiday(x))
        except Exception as e:
            self.logger.error(e, exec_info=True)
            print(e)
        finally:
            return df
