def create_txtfile(password, db_name):
    """
    Creates a txt file containing database name and password
    """
    L = [f"{password}\n", f"{db_name}\n"]
    # Writing to file
    with open("pass_name.txt", "w") as f:
        f.writelines(L)

create_txtfile("this_pass", "webshop")