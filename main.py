from src.config import config
from src.utils import get_info_hh, create_db, add_info_to_db


def main():
    company_ids = [733]
    db_name = 'head_hunter_jobs'
    params = {"host": "localhost",
              "user": "postgres",
              "password": 451501,
              "port": 5432}

    data = get_info_hh(company_ids)
    create_db(db_name, params)
    add_info_to_db(data, db_name, params)



if __name__ == '__main__':
    main()
