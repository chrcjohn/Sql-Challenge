# pip install sqlalchemy psycopg2-binary
# SQLAlchemy
from sqlalchemy import create_engine
from config import pg_user, pg_pass

import psycopg2 
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
# Path to SQL database
engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@localhost:5432/sql_challenge')
conn = engine.connect()
Create a histogram to visualize the most common salary ranges for employees.
# Pull salary information from the salary table from the sql_challege database
salary_data = pd.read_sql("SELECT * FROM salaries ", conn)
salary_data.head()
emp_no	salary
0	10001	60117
1	10002	65828
2	10003	40006
3	10004	40054
4	10005	78228
# Plotting histogram of salary 
fig=plt.figure(figsize=(10,8))
plt.hist(salary_data.salary)
plt.xlabel("Employees Salary ($) ", fontsize=15)
plt.ylabel("Number of employees", fontsize=15)
plt.title("Pewlett Hackard's Employees Salary Summary", fontsize=18)
plt.show()

Create a bar chart of average salary by title.
# Pulling information from title table 
title_data = pd.read_sql("SELECT * FROM titles ", conn)
title_data.head()
title_id	title
0	s0001	Staff
1	s0002	Senior Staff
2	e0001	Assistant Engineer
3	e0002	Engineer
4	e0003	Senior Engineer
# Pulling information from employee table
employee_data = pd.read_sql("SELECT * FROM employees ", conn)
employee_data.head()
emp_no	emp_title_id	birth_date	first_name	last_name	sex	hire_date
0	473302	s0001	1953-07-25	Hideyuki	Zallocco	M	1990-04-28
1	475053	e0002	1954-11-18	Byong	Delgrande	F	1991-09-07
2	57444	e0002	1958-01-30	Berry	Babb	F	1992-03-21
3	421786	s0001	1957-09-28	Xiong	Verhoeff	M	1987-11-26
4	282238	e0003	1952-10-28	Abdelkader	Baumann	F	1991-01-18
# Merging the 'employee data' table with 'salary data' table to get the salary info to the dataframe
emp_salary_merge_df = pd.merge(salary_data, employee_data, how='inner', on='emp_no')
emp_salary_merge_df.head()
emp_no	salary	emp_title_id	birth_date	first_name	last_name	sex	hire_date
0	10001	60117	e0003	1953-09-02	Georgi	Facello	M	1986-06-26
1	10002	65828	s0001	1964-06-02	Bezalel	Simmel	F	1985-11-21
2	10003	40006	e0003	1959-12-03	Parto	Bamford	M	1986-08-28
3	10004	40054	e0003	1954-05-01	Chirstian	Koblick	M	1986-12-01
4	10005	78228	s0001	1955-01-21	Kyoichi	Maliniak	M	1989-09-12
# Merging the emp_salary_merge dataframe with 'title_data' table to get all the info we need 
emp_salary_title_df = pd.merge(emp_salary_merge_df, title_data, how='inner', left_on="emp_title_id", right_on='title_id')
emp_salary_title_df.head()
emp_no	salary	emp_title_id	birth_date	first_name	last_name	sex	hire_date	title_id	title
0	10001	60117	e0003	1953-09-02	Georgi	Facello	M	1986-06-26	e0003	Senior Engineer
1	10003	40006	e0003	1959-12-03	Parto	Bamford	M	1986-08-28	e0003	Senior Engineer
2	10004	40054	e0003	1954-05-01	Chirstian	Koblick	M	1986-12-01	e0003	Senior Engineer
3	10006	40000	e0003	1953-04-20	Anneke	Preusig	F	1989-06-02	e0003	Senior Engineer
4	10009	60929	e0003	1952-04-19	Sumant	Peac	F	1985-02-18	e0003	Senior Engineer
# Finding the average salary based on title 
avg_salary_b_title = emp_salary_title_df.groupby("title").mean()['salary']
avg_salary_b_title 
title
Assistant Engineer    48564.434447
Engineer              48535.336511
Manager               51531.041667
Senior Engineer       48506.799871
Senior Staff          58550.172704
Staff                 58465.382850
Technique Leader      48582.896092
Name: salary, dtype: float64
# Plotting the histogram to show the average salary based on title 
avg_salary_b_title_bar  = avg_salary_b_title.plot(kind="bar", figsize=(15,8))
plt.xlabel("Job Title", fontsize =15)
plt.ylabel("Salary ($)", fontsize =15)
plt.title("Average Salary By Title", fontsize =18)
plt.xticks(rotation=0)
plt.ylim(0, 70000)
(0.0, 70000.0)

Evidence in hand, I marched into my boss's office and present the visualization. My boss thanked me for my work. On my way out of the office, I heard the words, "Search your ID number." I looked down at my badge to see that my employee ID number is 499942.

# Looking at my ID: 499942
my_id = employee_data.loc[employee_data['emp_no']== 499942 ]
my_id 
emp_no	emp_title_id	birth_date	first_name	last_name	sex	hire_date
168736	499942	e0004	1963-01-10	April	Foolsday	F	1997-02-10