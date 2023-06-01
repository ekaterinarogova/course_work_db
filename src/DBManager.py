import psycopg2


class DBManager:
    """
    Класс для работы с БД Postgres
    """

    def __init__(self, db_name: str, params: dict) -> None:
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Список всех компаний и количество вакансий у каждой компании
        """
        try:
            conn = psycopg2.connect(dbname=self.db_name, **self.params)
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select company_name, count(vacancy_title) as vacancy_number
                    from employers
                    join vacancies using (company_id)
                    group by company_name
                    """
                )
                data = cur.fetchall()
        except (Exception):
            print('Ошибка при подключении к БД')
        else:
            conn.close()
            return data

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return: Список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                select vacancy_title, company_name, salary, vacancies.link
                from vacancies
                join employers using (company_id)
                """
            )
            data = cur.fetchall()
        conn.close()
        return data

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return: Среднюю зарплату по вакансиям
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                select company_name, avg(salary) as average_salary
                from employers
                join vacancies using (company_id)
                group by company_name
                """
            )
            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: Список всех вакансий, у которых зарплата выше средней
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                select *
                from vacancies
                where salary > (select avg(salary) from vacancies)
                """
            )
            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержится ключевое слово
        :return: Список всех вакансий, в названии которых содержится ключевое слово
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select vacancy_title, company_name, salary, vacancies.link, vacancies.description,
                experience, employment, published_date 
                from vacancies
                join employers using(company_id)
                where lower(vacancy_title) like '%{keyword}%' or lower(vacancy_title) like '%{keyword}'
                or lower(vacancy_title) like '{keyword}%'
                """
            )
            data = cur.fetchall()
        conn.close()
        return data
