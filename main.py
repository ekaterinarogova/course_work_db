from src.utils import get_info_hh, create_db, add_info_to_db
from src.DBManager import DBManager
from src.config import config


def main():
    company_ids = [733,  # Ланек
                   8582,  # Леруа Мерлен
                   1473866,  # СберСервис
                   78638,  # Тинькофф
                   3785152,  # Eqvanta
                   84585,  # Avito
                   1532045,  # CarPrice
                   2381,  # Softline
                   4305039,  # Outlines Technologies
                   1375441,  # Okko
                   ]
    db_name = 'head_hunter_jobs'
    params = config()

    data = get_info_hh(company_ids)  # получаем информацию с сайта hh.ru
    create_db(db_name, params)  # создает базу данных
    add_info_to_db(data, db_name, params)  # добавляем полученную информацию в базу данных
    db_manager = DBManager(db_name, params)  # создаем экземпляр класса DBManager для работы с базой данных
    for i in db_manager.get_companies_and_vacancies_count():
        print(i)


if __name__ == '__main__':
    main()
