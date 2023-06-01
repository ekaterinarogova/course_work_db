import psycopg2


class DBManager:
    """
    Класс для работы с БД Postgres
    """
    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Список всех компаний и количество вакансий у каждой компании
        """
        # select company_name, count(vacancy_title) as vacancy_number
        # from employers
        # join vacancies using (company_id)
        # group by company_name
        pass

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return: Список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        # select vacancy_title, company_name, salary, link
        # from vacancies
        # join employers using (company_id)
        pass

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return: Среднюю зарплату по вакансиям
        """
        # select company_name, avg(salary) as average_salary
        # from vacancies
        # join employers using (company_name)
        # group by company_name
        pass

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: Список всех вакансий, у которых зарплата выше средней
        """
        # select *
        # from vacancies
        # where salary > avg(salary)
        pass

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержится ключевое слово
        :return: Список всех вакансий, в названии которых содержится ключевое слово
        """
        # select *
        # from vacancies
        # where lower(vacancy_title) like (%keyword%) or lower(vacancy_title) like (%keyword)
        # or lower(vacancy_title) like (keyword%)
        pass
