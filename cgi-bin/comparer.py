from utilities import get_products_filtered, get_products_search, get_products_ids
from utilities_new import get_products_filtered_sql, get_products_search_sql, get_products_ids_sql

from os import path
from inspect import currentframe, getfile

cmd_folder = path.realpath(
    path.abspath(path.split(getfile(currentframe()))[0])) + '/'

test1 = {'type': 'Bags', 'subtype': 'Leather bag', 'color': 'Blue', 'price': 199}
test2 = [1,2,3]
a = get_products_filtered_sql(test1)
b = get_products_filtered(test1)

c = get_products_search_sql(test2)
d = get_products_search(test2)

if c == d:
    print("yes")
