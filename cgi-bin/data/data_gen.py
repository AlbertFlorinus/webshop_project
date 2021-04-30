#!/usr/bin/env python

import pandas as pd

# Products

clothes_type_main = ['Shirts', 'Pants', 'Underwear', 'Jackets', 'Bags']
clothes_type_sub = {'Shirts': ['T-shirt', 'Sweatshirt', 'Cardigan', 'Tank Top'], 
					'Pants': ['Shorts', 'Jeans', 'Training pants'], 
					'Underwear': ['Y-front', 'Boxers'], 
					'Jackets': ['Winter jacket', 'Leather jacket', 'Suit', 'Other jacket'], 
					'Bags': ['Leather bag', 'Backpack']}

clothes_colors = ['Red', 'Blue', 'Green', 'Brown', 'Black', 'White']
clothes_price = [199, 299, 499, 799, 999, 1599]
clothes_gender = ['Female', 'Male']
clothes_manufacturer = ['Jack and Jones', 'GANT', 'Vagabond', 'Diesel', 'Nike', 
						'Adidas', 'Abercrombie and Fitch', 'Cheap Monday', 'WESC']
clothes_size = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

product_data = []
i = 0
for cmanufacturer in clothes_manufacturer:
	for ctype in clothes_type_main:
		for csubtype in clothes_type_sub[ctype]:
			for ccolor in clothes_colors:
				for cgender in clothes_gender:
					for cprice in clothes_price:
						if ctype == 'Bags':
							product_data.append([i, cmanufacturer, ctype, csubtype, ccolor, cgender, cprice, '-'])
							i += 1
						else:
							for csize in clothes_size:
								product_data.append([i, cmanufacturer, ctype, csubtype, ccolor, cgender, cprice, csize])
								i += 1

prod_columns = ['id','brand', 'type', 'subtype', 'color', 'gender', 'price', 'size']
products = pd.DataFrame(data=product_data, columns=prod_columns)
products.to_csv('Products.csv', index=False)

# Customers
customer_columns = ['firstname', 'lastname', 'street', 'city', 'zipcode']
customer_data = [['Alice',		'Andersson',	'Testgatan 1',	'Ankeborg',		12312],
		['Oscar',		'Johansson',	'Testgatan 2',	'Ankeborg', 	12312],
		['Nora',		'Hansen',		'Tramsgatan 1',	'Karlskrona',	32132],
		['William',		'Johansen',		'Tramsgatan 2',	'Karlskrona',	32132],
		['Lucia',		'Garcia',		'Bakgatan 1',	'Skogen',		23423],
		['Hugo',		'Fernandez',	'Bakgatan 2',	'Skogen',		23423],
		['Sofia',		'Rossi',		'Slumpgatan 1',	'Stockholm',	43243],
		['Francesco',	'Russo',		'Slumpgatan 2',	'Stockholm',	43243],
		['Olivia', 		'Smith',		'Skogsgatan 1',	'Lund',			56776],
		['Oliver', 		'Jones',		'Skogsgatan 2',	'Lund',			56776]]


customers = pd.DataFrame(data=customer_data, columns=customer_columns)
customers.to_csv('Customers.csv', index=False)

# Orders
order_columns = ['orderid'] + customer_columns + prod_columns + ['amount']
order_data = [[0] + customer_data[0] + product_data[123] + [1],
		[0] + customer_data[0] + product_data[345] + [2],
		[0] + customer_data[0] + product_data[9878] + [1],
		[1] + customer_data[3] + product_data[23] + [1],
		[1] + customer_data[3] + product_data[55] + [1],
		[2] + customer_data[8] + product_data[400] + [3],
		[3] + customer_data[9] + product_data[12] + [2],
		[3] + customer_data[9] + product_data[888] + [1],
		[4] + customer_data[2] + product_data[4123] + [1],
		[4] + customer_data[2] + product_data[9999] + [2],
		[4] + customer_data[2] + product_data[872] + [3],
		[4] + customer_data[2] + product_data[20] + [1],
		[5] + customer_data[0] + product_data[6666] + [1],
		[6] + customer_data[1] + product_data[50010] + [1],
		[7] + customer_data[5] + product_data[12300] + [3],
		[8] + customer_data[7] + product_data[1] + [1],
		[9] + customer_data[9] + product_data[1230] + [20],
		[10] + customer_data[1] + product_data[7880] + [1],
		[11] + customer_data[6] + product_data[300] + [1],
		[11] + customer_data[6] + product_data[25000] + [2],
		[11] + customer_data[6] + product_data[10000] + [5],
		[12] + customer_data[4] + product_data[5000] + [1],
		[12] + customer_data[4] + product_data[15000] + [2],
		[12] + customer_data[4] + product_data[25000] + [1],
		[12] + customer_data[4] + product_data[35000] + [5]]


orders = pd.DataFrame(data=order_data, columns=order_columns)
orders.to_csv('Orders.csv', index=False)
