#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgitb
import sys
from cgi import FieldStorage
from codecs import getwriter
from inspect import currentframe, getfile
from os import path

from jinja2 import Environment, FileSystemLoader

# Import our utilitiy functions
from utilities import (get_20_most_popular, get_categories,
                       get_products_filtered, get_products_ids,
                       get_products_search, get_subcategories, write_order)

sys.stdout = getwriter("utf-8")(sys.stdout.detach())
cgitb.enable()  # Enable debugging

print("Content-Type: text/html; charset=UTF-8\n")

cmd_folder = path.realpath(
    path.abspath(path.split(getfile(currentframe()))[0]))
env = Environment(loader=FileSystemLoader(path.join(cmd_folder, 'templates')))
env.globals = {'path': '../' if 'cgi-bin' in cmd_folder else ''}


def products(limits, filters=None):
    template = env.get_template('products.html')
    if filters is None:
        data = get_20_most_popular()
    else:
        data = get_products_filtered(filters)
    # Limit the length of the output to 20, otherwise its horrendous.
    if len(data) > 20:
        data = data[:20]
    try:
        # print(template.render(title='BestBuy', products=[
        #    {'brand': 'brand', 'name': 'Name', 'size': 'XXXL', 'price': 2323, 'color': "red"},
        #    {'brand': 'brand', 'name': 'Name', 'size': 'XL', 'price': 2323, 'color': "red"},
        # ]))
        print(template.render(
            title='BestBuy',
            products=data,
        ))
    except Exception as e:
        print(e)


def categories(limits):
    template = env.get_template('categories.html')
    data = get_categories()

    try:
        # print(template.render(title='BestBuy', categories=[
        #    {'title': 'Heasasdasdasdasdrr', 'children': [
        #        {'url': '', 'name': 'Herr kalsong'},
        #        {'url': '', 'name': 'Herr Troja'}
        #    ]},
        #    {'title': 'Dam', 'children': [
        #        {'url': '', 'name': 'Dam vaska'},
        #        {'url': '', 'name': 'Dam troja'}
        #    ]}
        # ]))
        print(template.render(
            title='BestBuy',
            categories=data,
        ))
    except Exception as e:
        print(e)


# Need to do same thing as above but for subcategories. call the get_subcategories()
# function with gender and main category as parameters
def subcategories(limits, gender, category):
    template = env.get_template('subcategories.html')
    data = get_subcategories(gender, category)

    try:
        print(template.render(
            title='BestBuy',
            categories=data,
        ))
    except Exception as e:
        print(e)


def cart():
    from os import environ
    cart = []
    try:
        if 'HTTP_COOKIE' in environ:
            cart_data = {
                i[0]: '='.join(i[1:])
                for i in [
                    cookie.split('=')
                    for cookie in environ['HTTP_COOKIE'].split('; ')
                ]
            }.get('cart')
            if cart_data:
                value = map(int, cart_data.strip("[]").split("%2C"))
                cart = get_products_ids(value)
        template = env.get_template('cart.html')
        print(template.render(
            title='BestBuy (cart)',
            cart=cart,
            price=23,
        ))
        """print(template.render(title='BestBuy (cart)', cart=[
            {'brand': 'brand', 'name': 'Name', 'size': 'XXXL', 'price': 2323, 'color': "red"},
            {'brand': 'brand', 'name': 'Name', 'size': 'XL', 'price': 2323, 'color': "red"},
        ]))"""
    except Exception as e:
        print(e)


def checkout():
    try:
        order = {
            'email': form.getvalue('email'),
            'name': form.getvalue('name'),
            'address': form.getvalue('address'),
            'zipcode': form.getvalue('zipcode'),
            'town': form.getvalue('town'),
            'items': form.getvalue('items')
        }
        write_order(order)

        template = env.get_template('checkout.html')
        print(
            template.render(
                title='BestBuy',
                address=form.getvalue('address'),
            ))
    except Exception as e:
        print(e)


def search(words):
    try:
        template = env.get_template('products.html')
        data = get_products_search(words)
        print(template.render(
            title='BestBuy',
            products=data,
        ))
    except Exception as e:
        print(e)


# Create instance of FieldStorage
form = FieldStorage()
action = form.getvalue('action')

if action == 'category':
    categories("")
elif action == 'cart':
    cart()
elif action == 'checkout':
    checkout()
elif action == 'subcategory':
    gender = form.getvalue('gender')
    category = form.getvalue('category')
    subcategories("", gender, category)
elif action == 'filtered_products':
    filters = {
        'gender': form.getvalue('gender'),
        'type': form.getvalue('category'),
        'subtype': form.getvalue('subcategory')
    }
    products("", filters)
elif action == 'search':  # Not done. Not even started actually :)
    words = form.getvalue('search').split()
    search(words)
else:
    products("")
