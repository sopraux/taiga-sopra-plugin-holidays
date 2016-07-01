import datetime, logging

def str_to_date(string):
    try:
        return datetime.datetime.strptime(string, "%d-%m-%Y").date()
    except:
        logging.exception('invalid date')


def prepare_dates(array_date):
    dates = map(str_to_date, array_date)
    return filter(None, dates)
