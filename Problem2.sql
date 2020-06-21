/*
We have separate tables for storing information about the companies and their offices. Some companies
don't have any office, some have many offices.
Write a SQL query that returns name, revenue and number of offices for all companies that have less than 5
offices. Order the result by companies’ number of offices.
*/

select companies.name, companies.revenue, COUNT(offices.name) AS NumberOfOffices from (offices Inner Join companies on offices.company_id=companies.company_id) Group By name having count(offices.name)<5 order by count(offices.name);