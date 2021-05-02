import pandas as pd
from tkinter.filedialog import askopenfilename
from sqlalchemy import create_engine
import time

def timer(func):
    def wrapper(_):
        before = time.time()
        func(_)
        print("Function took:", time.time() - before, "seconds")
    return wrapper

def engine(password, db_name = "webshop_back", port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    return engine

def csv_to_sql(password, db_name = "webshop_back", port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    df = pd.read_csv(askopenfilename())
    df.to_sql('orders', con=engine)

if __name__ == "__main__":
    password = str(input("password: "))
    csv_to_sql(password)

