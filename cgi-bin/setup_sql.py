import pandas as pd
from tkinter.filedialog import askopenfilename
from sqlalchemy import create_engine
import time

def timer(func):
    def wrapper(*args):
        before = time.time()
        func(*args)
        print("Function took:", time.time() - before, "seconds")
    return wrapper

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

def csv_to_sql(password, db_name = "webshop_back", port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    df = pd.read_csv(askopenfilename())
    df.to_sql('orders', con=engine)

if __name__ == "__main__":
    try:
        password, db_name = read_txtfile()
    except:
        password = str(input("password: "))
        db_name = str(input("name of db: "))
        create_txtfile(password, db_name)
