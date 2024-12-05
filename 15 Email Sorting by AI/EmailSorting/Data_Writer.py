from datetime import datetime
from csv import writer
import pandas as pd


def __get_today_date():
    datetime_object = datetime.today()
    today_date = datetime.strftime(datetime_object, "%m/%d/%Y")
    today_date = datetime.strptime(today_date, '%m/%d/%Y').date()
    return today_date


def __is_time_validated():
    now = datetime.now()
    current_time = datetime.strftime(now, "%H:%M:%S")
    current_time = datetime.strptime(current_time, "%H:%M:%S").time()

    time1 = datetime.strptime("12:59:00", "%H:%M:%S").time()
    time2 = datetime.strptime("23:57:00", "%H:%M:%S").time()

    if time1 <= current_time <= time2:
        return True

    return False


def write_csv(last_date, stats_list):
    today_date = __get_today_date()
    if last_date != today_date:
        if __is_time_validated():
            stats_list.append(str(today_date))

            with open('daily_email_stats.csv', 'a') as f_object:
                # Pass this file object to csv.writer()
                # and get a writer object
                writer_object = writer(f_object)

                # Pass the list as an argument into
                # the writerow()
                writer_object.writerow(stats_list)

                # Close the file object
                f_object.close()

            print("Write CSV Data!")
            return True, today_date

    return False, today_date


# datetime_object = datetime.today()
# today_date = datetime.strftime(datetime_object, "%m/%d/%Y")
# today_date = datetime.strptime(today_date, '%m/%d/%Y').date()
# print(str(today_date))



