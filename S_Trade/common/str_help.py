import datetime


def str_replace_date(in_string='', in_date=datetime.datetime.today()):

    # replace year YYYY
    in_string = in_string.replace('YYYY', in_date.strftime('%Y'))

    # replace Month MON
    in_string = in_string.replace('MON', in_date.strftime('%b').upper())

    # replace Month Mon
    in_string = in_string.replace('Mon', in_date.strftime('%b'))

    # replace date MM
    in_string = in_string.replace('MM', in_date.strftime('%m'))

    # replace date DD
    in_string = in_string.replace('DD', in_date.strftime('%d'))

    return in_string
