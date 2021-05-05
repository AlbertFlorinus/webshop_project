import pandas as pd
from tkinter.filedialog import askopenfilename
from sqlalchemy import create_engine

def engine(password, db_name, port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    return engine

def csv_to_sql(password, db_name, tbl_name, port = 3306):
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:{port}/{db_name}")
    df = pd.read_csv(askopenfilename())
    df.to_sql(tbl_name, con=engine)

if __name__ == "__main__":
    password = str(input("password: "))
    db_name = str(input("db: "))
    tbl_name = str("table_name: ")

    engine = engine(password, db_name)
    csv_to_sql(password, db_name, tbl_name)
    
