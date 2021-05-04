#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from os import path
from inspect import currentframe, getfile
from setup_sql import engine, read_txtfile
from performance_test import timer

password, db_name = read_txtfile()
engine = engine(password)

cmd_folder = path.realpath(
    path.abspath(path.split(getfile(currentframe()))[0])) + '/'

@timer
def get_products_filtered_sql(categories = None):
    if categories is not None:
        #generating query
        query = "select * from products where ("
        count = 0
        for i, j in zip(categories.keys(), categories.values()):
            count += 1
            query += i
            query += " = "
            query += f'"{j}"'
            if count < len(categories.keys()):
                query += " and "
        query += ")"

    else:
        query = "select * from products"

    data = engine.execute(query).fetchall()

    #converting to legacy utilities output
    data = [dict(row) for j, row in enumerate(data)]
    for i in range(len(data)):
        data[i].pop("index")
    
    return data

@timer
def get_products_search_sql(values):
    #get unique brands from mysql, use python to see if contains substring. how to do directly in sql?
    query = "select distinct(brand) from products"
    data = engine.execute(query).fetchall()
    data = [list(row) for j, row in enumerate(data)]
    unique_brands = [j.upper() for i in data for j in i]
    results = []

    for i in unique_brands:
        if any(word.upper() in i for word in values):
            results.append(i)

    if len(results) != 0:
        #check to prevent crash if bad search
        #generating query...
        query2 = "select * from products where ("
        count = 0
        for i in results:
            count += 1
            query2 += "brand"
            query2 += " = "
            query2 += f'"{i}"'
            if count < len(results):
                query2 += " or "
        query2 += ")"

        data2 = engine.execute(query2).fetchall()
        data2 = [dict(row) for j, row in enumerate(data2)]
        for i in range(len(data2)):
            data2[i].pop("index")
    
    else:
        data2 = None
    
    return data2
    



def get_products_ids_sql(ids):
    #generating query
    query = "select * from products where ("
    count = 0
    for i in ids:
        count += 1
        query += "id"
        query += " = "
        query += str(i)
        if count < len(ids):
            query += " or "
    query += ")"
    data = engine.execute(query).fetchall()
    #converting to legacy utilities output
 
    data = [dict(row) for j, row in enumerate(data)]
    for i in range(len(data)):
        data[i].pop("index")

    return data

def get_categories():
    """
    Returdata
    En lista innehållande dictionaries med nycklarna title och children.
    title representerar könet plaggen är gjorda för (t.ex. Dam och Herr).
    children skall hålla en lista utav ytterligare dictionary object, där
    varje dictionary innehåller nycklarna url och name.
    url tilldelar ni en tom sträng (d.v.s. '') och nyckeln name tilldelar
    ni en huvudkategori.

    Exempelvis:
    [{'title': 'Dam', 'children': [{'url': '', 'name': 'Tröjor'},
                                   {'url': '', 'name': 'Byxor'}]},
    {'title': 'Herr', 'children': [{'url': '', 'name': 'Tröjor'},
                                   {'url': '', 'name': 'Väskor'}]}]
    """

    #df = pd.read_csv(cmd_folder + 'data/Products.csv')
    df = pd.read_sql("products", con=engine)
    genders = df['gender'].unique()
    types = [
        df[(df['gender'] == genders[0])]['type'].unique().tolist(),
        df[(df['gender'] == genders[1])]['type'].unique().tolist()
    ]
    children = [[{
        'url': '',
        'name': name
    } for name in types[0]], [{
        'url': '',
        'name': name
    } for name in types[1]]]
    ''' SQL '''

    result = [{
        'title': genders[0],
        'children': children[0]
    }, {
        'title': genders[1],
        'children': children[1]
    }]
    return result


def get_subcategories(gender, category):
    """
    Indata
    Två strängar, gender och category, där gender är könet som det efterfrågas
    kläder för och category är huvudkategorin vars subkategorier vi vill hämta.

    Returdata
    En lista innahållande dictionaries med nycklarna gender, category, och
    children. gender representerar könet plaggen är gjorda för (t.ex. Dam och
    Herr). category är den inkommande kategorin vi hämtar subkategorier för
    children skall hålla en lista utav ytterligare dictionary object, där
    varje dictionary
    innehåller nycklarna url och name.
    url tilldelar ni en tom sträng (d.v.s. '') och nyckeln name tilldelar ni en
    subkategori.

    Exempelvis:
    [{'gender': 'Dam', 'category': 'Tröjor', 'children':
        [{'url': '', 'name': 'T-shirts'}, {'url': '', 'name': 'Linnen'}]}]
    """

    #df = pd.read_csv(cmd_folder + 'data/Products.csv')
    df = pd.read_sql("products", con=engine)
    types = df[(df['gender'] == gender)
               & (df['type'] == category)]['subtype'].unique().tolist()
    children = [{'url': '', 'name': name} for name in types]
    result = [{'gender': gender, 'category': category, 'children': children}]
    ''' SQL '''

    return result


def write_order(order):
    """
    Indata
    order som är en dictionary med nycklarna och dess motsvarande värden:
    town: Kundens stad
    name: Kundens namn
    zipcode: Kundens postkod
    address: Kundens address
    email: Kundens email
    items: En lista av heltal som representerar alla produkters artikelnummer.
        Så många gånger ett heltal finns i listan, så många artiklar av den
        typen har kunden köpt. Exempelvis: [1,2,2,3]. I den listan har kunden
        köpt 1 styck av produkt 1, 2 styck av produkt 2, och 1 styck av
        produkt 3.
    """

    #df_orders = pd.read_csv(cmd_folder + 'data/Orders.csv')
    df_orders = pd.read_sql("orders", con=engine)
    # Get new order ID
    orderID = df_orders['orderid'].max() + 1
    # Grab the products id number and the amount of each product
    item_ids = list(map(int, order['items'].strip('[]').split(',')))
    items = [{
        'id': int(x),
        'amount': item_ids.count(x)
    } for x in list(set(item_ids))]

    # Get the name and so on for the customer.
    try:
        firstname, lastname = order['name'].split()
    except Exception:
        firstname = order['name']
        lastname = ''
    email = order['email']
    address = order['address']
    zipcode = order['zipcode']
    town = order['town']

    # Write the actual order
    df_products = pd.read_sql("products", con=engine)
    for item in items:
        product = df_products[df_products['id'] == item['id']].to_dict(
            'records')[0]
        df_orders.loc[len(df_orders)] = [
            orderID, firstname, lastname, address, town, zipcode,
            product['id'], product['brand'], product['type'],
            product['subtype'], product['color'], product['gender'],
            product['price'], product['size'], item['amount']
        ]
    df_orders.to_csv(cmd_folder + 'data/Orders.csv', index=False, encoding='utf-8')

def get_20_most_popular_sql():
    query = "select products.id, products.brand, products.type, products.subtype, products.color, products.gender,  products.price, products.size from products join orders on products.id = orders.id order by orders.amount desc limit 20"
    data = engine.execute(query).fetchall()
    data = [dict(row) for j, row in enumerate(data)]
    return data

def get_20_most_popular_sql_depr():
    query = "select * from orders order by amount desc"
    data = engine.execute(query).fetchall()

    data = [dict(row) for j, row in enumerate(data)]
    for i in range(len(data)):
        data[i].pop("index")

    data = data[0:20]

    count = 0
    query2 = "select * from products where ("
    for i in data:
        count += 1
        query2 += "id"
        query2 += " = "
        query2 += str(i["id"])
        if count < len(data):
            query2 += " or "
    query2 += ")"

    data2 = engine.execute(query2).fetchall()
    data2 = [dict(row) for j, row in enumerate(data2)]
    for i in range(len(data2)):
        #data2[i].pop("index")
        pass

    return data2


def main():
    #test = get_products_filtered_sql({'type': 'Bags', 'subtype': 'Leather bag', 'color': 'Blue', 'price': 199})
    #test = get_products_filtered({'type': 'Bags', 'subtype': 'Leather bag', 'color': 'Blue', 'price': 199})
    #test = get_products_ids([1,2,4])
    #print(test)
    #test = get_products_ids_sql([1,2,4])
    #print("\n")
    
    #test = get_categories()
    #print(test)
    # test = get_subcategories('Female', 'Bags')
    #test = get_20_most_popular()
   
    #print(test)
    test = get_products_search_sql(["Jack", "and", "Jones"])
    #print(len(test))
    #print(test)

if __name__ == '__main__':
    main()
