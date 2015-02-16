def get_markup_by_size(model_size):
    markup_table = {50: 5.18, 100:10.36, 200:20.70}
    return markup_table.get(model_size, 25.88)
