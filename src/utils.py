import requests
import psycopg2


def get_info_hh(company_ids: list) -> list[dict]:
    """
    Получает информацию о компаниях-работодателях и их вакансиях c сайта headhunter.ru
    :param company_ids: список id компаний на сайте hh.ru
    :return: список с данными о компании и ее вакансиях
    """
    data = []
    for company_id in company_ids:
        url = f'https://api.hh.ru/employers/{company_id}'
        company_data = requests.get(url).json()

        vacancy_data = requests.get(company_data['vacancies_url']).json()
        data.append({'company': company_data,
                     'vacancies': vacancy_data['items']})
    return data


def create_db(db_name: str, params: dict) -> None:
    """
    Создает базу данных и таблицы для сохранения данных о компаниях и их вакансиях
    :param db_name: название базы данных
    :param params: данные для подключения к базе данных
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"drop database {db_name}")
        cur.execute(f"create database {db_name}")
    conn.close()

    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("create table employers("
                        "company_id serial primary key,"
                        "company_name varchar(50)  not null,"
                        "description  text,"
                        "link         varchar(100) not null,"
                        "industry     varchar(50),"
                        "area         varchar(30),"
                        "vacancies_url varchar(100) not null)")
            cur.execute("create table vacancies("
                        "vacancy_id serial primary key,"
                        "company_id int references employers (company_id) not null,"
                        "vacancy_title varchar(100) not null,"
                        "salary int,"
                        "link varchar(100) not null,"
                        "description text,"
                        "experience varchar(50),"
                        "employment varchar(50),"
                        "published_date date)")
    conn.close()


def add_info_to_db(info: list[dict], db_name: str, params: dict) -> None:
    """
    Сохраняет данные в базу данных
    :param info: данные в виде списка словарей для сохранения в базу данных
    :param db_name: название базы данных
    :param params: данные для подключения к базе данных
    :return:
    """
    conn = psycopg2.connect(database=db_name, **params)
    with conn.cursor() as cur:
        for i in info:
            cur.execute("insert into employers (company_name, description, link, industry, area, vacancies_url)"
                        "values (%s, %s, %s, %s, %s, %s)"
                        "returning company_id",
                        (i['company'].get('name'), convert_string(i['company'].get('description')), i['company'].get('alternate_url'),
                         i['company']['industries'][0].get('name'), i['company']['area'].get('name'),
                         i['company'].get('vacancies_url')))
            company_id = cur.fetchone()[0]
            vacancy_data = i['vacancies']
            for vacancy in vacancy_data:
                salary = salary_processing(vacancy['salary'])
                cur.execute(
                    """
                    insert into vacancies (vacancy_title, salary, link, company_id, description,
                    experience, employment, published_date)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['name'], salary, vacancy['alternate_url'], company_id,
                     vacancy['snippet'].get('responsibility'), vacancy['experience'].get('name'),
                     vacancy['employment'].get('name'), vacancy['published_at']))

    conn.commit()
    conn.close()


def salary_processing(salary):
    """
    Обрабатывает данные по зарплате, приводя их к единой форме
    :param salary: данные по зарплате компании. Может быть словарь или None
    :return: численное значение по зарплате или None
    """
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return round((salary['from'] + salary['to']) / 2)
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None


def convert_string(string: str) -> str:
    """
    Обрабатывает входящую строку и удаляет лишние символы
    :param string: исходный текст
    :return: строку без лишных символов
    """
    symbols = ['\n', '<strong>', '\r', '</strong>', '</p>', '<p>', '</li>', '<li>',
               '<b>', '</b>', '<ul>', '<li>', '</li>', '<br />', '</ul>']
    for symb in symbols:
        string = string.replace(symb, " ")
    return string
