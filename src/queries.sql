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
