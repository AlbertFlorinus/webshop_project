#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import pandas as pd
from os import path
from inspect import currentframe, getfile
from sqlalchemy import create_engine
from setup_sql import engine, read_txtfile

from collections import Counter

import ast

password, db_name = read_txtfile()
engine = engine(password, db_name)


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
    
    return data


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
    
    else:
        data2 = None
    
    return data2

def get_20_most_popular_sql():
    query = "select products.id, products.brand, products.type, products.subtype, products.color, products.gender,  products.price, products.size from products join orders on products.id = orders.id order by orders.amount desc limit 20"
    data = engine.execute(query).fetchall()
    data = [dict(row) for j, row in enumerate(data)]
    return data

def get_products_ids_sql(ids):
    #generating query
    query = "select * from products where ("
    counter = 0
    for i in ids:
        counter += 1
        query += "id"
        query += " = "
        query += str(i)
        if counter < len(ids):
            query += " or "
        
    query += ")"
    data51 = engine.execute(query).fetchall()

    #converting to legacy utilities output
 
    data51 = [dict(row) for j, row in enumerate(data51)]

    #generating multiplies dict for summing price of type {product_id: amount_ordered} like {1240:4, 12:3} would be 4 items of id 1240 and 3 items of id 12.
    multis = {}
    for index, item in enumerate(ids):
        multis[index] = item

    multis = dict(Counter(multis.values()))

    return data51, multis

def get_categories_sql():
    gender_query = 'select distinct(gender) from products' # Queries the unique genders from DB
    gender_objects = engine.execute(gender_query).fetchall()
    gender_list = [i.values()[0] for i in gender_objects]
    
    product_query = [f"select distinct(type) from products where gender = '{g}'" for g in gender_list]
    product_objects = [engine.execute(i).fetchall() for i in product_query]
    
    result = []
    
    for i, gender in enumerate(gender_list):
        gender_dict = {}
        gender_dict['title'] = gender
        gender_dict['children'] = [{'url': '', 'name': f'{category[0]}'} for category in product_objects[i]]
        result.append(gender_dict)
    return result

def get_subcategories_sql(gender, category):
    query = f"select distinct(subtype) from products where gender = '{gender}' and `type` = '{category}'"
    subtype_objects = engine.execute(query).fetchall()
    subtype_data = [i[0] for i in subtype_objects]
    
    result = [{'gender': gender, 'category': category, 'children': [{'url': '', 'name': subtype} for subtype in subtype_data]}]
    
    return result
    

def write_order_sql(inf):
    query = f"select * from customers"
    data = engine.execute(query).fetchall()
    data = [dict(row) for j, row in enumerate(data)]

    first_name, last_name = inf["name"].split()
    kund  = {"firstname": first_name, "lastname": last_name, "street": inf["address"], "city": inf["town"],  "zipcode": int(inf["zipcode"])}
    kund_inf = [i for i in kund.values()]

    storage = [list(i.values()) for i in data]
    for index, item in enumerate(storage):
        storage[index] = item[1:]

    if kund_inf not in storage:
        query2 = f'insert into customers (firstname, lastname, street, city, zipcode) values ("{kund["firstname"]}", "{kund["lastname"]}", "{kund["street"]}", "{kund["city"]}", {kund["zipcode"]})'
        engine.execute(query2)
        cust_id = len(storage) + 1

    else:
        cust_id = storage.index(kund_inf) + 1
        
    bought = ast.literal_eval(inf["items"])

    multis = {}
    for index, item in enumerate(bought):
        multis[index] = item

    multis = dict(Counter(multis.values()))

    ordernum = engine.execute("select max(orderid) from orders").fetchall()

    ordernum = ordernum[0][0] + 1

    
    for i in multis.keys():
        query9 = f'insert into orders (customer_id, orderid, id, amount) values ({cust_id}, {ordernum}, {i}, {multis[i]})'
        engine.execute(query9)
        


#python3 -m http.server --cgi 8000