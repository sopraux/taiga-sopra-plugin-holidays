import datetime, logging

def str_to_date(string):
    try:
        return datetime.datetime.strptime(string, "%d-%m-%Y").date()
    except:
        logging.exception('invalid date')
