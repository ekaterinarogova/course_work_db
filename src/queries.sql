create database head_hunter_jobs;

create table employers(
    company_id   serial primary key,
    company_name varchar(50)  not null,
    description  text,
    link         varchar(100) not null,
    industry     varchar(50),
    area         varchar(30),
    vacancies_url varchar(100) not null
);

create table vacancies(
    vacancy_id serial primary key,
    vacancy_title varchar(50) not null,
    salary int,
    link varchar(100) not null,
    company_id int references employers (company_id) not null,
    description text,
    experience varchar(50),
    employment varchar(50)
);

select company_name, count(vacancy_title) as vacancy_number
from employers
join vacancies using (company_id)
group by company_name;

select vacancy_title, company_name, salary, link
from vacancies
join employers using (company_id);

select company_name, avg(salary) as average_salary
from employers
join vacancies using (company_id)
group by company_name;

select *
from vacancies
where salary > (select avg(salary) from vacancies);

select vacancy_title, company_name, salary, vacancies.link, vacancies.description,
experience, employment, published_date
from vacancies
join employers using(company_id)
where lower(vacancy_title) like '%keyword%' or lower(vacancy_title) like '%keyword'
or lower(vacancy_title) like 'keyword%';
