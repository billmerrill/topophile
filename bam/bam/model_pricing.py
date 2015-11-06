import datetime


def get_markup_by_size(model_size):
    markup_table = {50: 5.18, 100: 10.36, 200: 20.70}
    return markup_table.get(model_size, 25.88)


def get_model_service_markup():
    # going on sale, half off april 11
    # return 20.73
    # return 10.37
    # return time_based_sale_price()
    return 3.50


def time_based_sale_price():
    rn = datetime.datetime.now()
    no_dollar_deadline = datetime.datetime(2015, 4, 26, 14, 27, 30, 972067)

    if rn < no_dollar_deadline:
        return 0.0
    else:
        return 3.50
