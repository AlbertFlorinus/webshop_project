#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import pandas as pd
from os import path
from inspect import currentframe, getfile
from sqlalchemy import create_engine
import time

def engine(password, db_name, port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    return engine

def create_txtfile(password, db_name):
    """
    Creates a txt file containing database name and password
    """
    L = [f"{password}\n", f"{db_name}\n"]
    # Writing to file
    with open("pass_name.txt", "w") as f:
        f.writelines(L)

def read_txtfile():
    """
    opens the txt file and returns content
    """
    # Opening file
    with open("pass_name.txt", "r") as f:
        creds = []
        for line in f:
            creds.append(line.strip())

    password = creds[0]
    db_name = creds[1]
    return password, db_name


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

    return data

def get_20_most_popular_sql():
    query = "select products.id, products.brand, products.type, products.subtype, products.color, products.gender,  products.price, products.size from products join orders on products.id = orders.id order by orders.amount desc limit 20"
    data = engine.execute(query).fetchall()
    data = [dict(row) for j, row in enumerate(data)]
    return data

#python3 -m http.server --cgi 8000