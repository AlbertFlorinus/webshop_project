def get_products_filtered_sql(table, categories, criteria = "and"):
    #generating query
    query = f"select * from {table} where ("
    count = 0
    for i, j in zip(categories.keys(), categories.values()):
        count += 1
        query += i
        query += " = "
        query += f'"{j}"'
        if count < len(categories.keys()):
            query += f" {criteria} "
    query += ")"
    print(query)


#get_products_filtered_sql("hej",{"namn": "hej", "andra": "tva"}, criteria="or")
test = ['jack', 'and', 'jones']

def searcher(table, words, criteria= " or "):
    query = f"select * from {table} where ("
    count = 0
    for i in words:
        count += 1
        query += "brand"
        query += " like "
        query += f'"‰{i}‰"'
        if count < len(words):
            query += f" {criteria} "
    query += ")"
    print(query)
#"%value%"
searcher("products", ["jack", "and", "jones"])
