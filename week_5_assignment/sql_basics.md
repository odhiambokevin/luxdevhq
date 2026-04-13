# A Look into SQL Query Basics

SQL is essential for the modern data professional. It is incorporated into most tools that drive data architectures. As such, it is important to have a solid understanding of the formative fundamentals.

## Data definition language (DDL) VS Data Manipulation Language (DML)
SQL queries have commands and underlying syntax which can be grouped into several categories. Two of these are data definition language and data manipulation language.

Data definition language is used to modify the structure of the objects that hold data. They consist of commands such as _CREATE_, _ALTER_, _DROP_ among others.

Data manipulation language commands are used to change the actual data. These include commands such as _INSERT_, _UPDATE_ or even _DELETE_.

Other categories include:
1. Data query language: used to retrieve data eg. _SELECT_
2. Data control language: manage access and permissions to data eg. _GRANT_, _REVOKE_.

Let us look at brief commands examples that form the foundational structure of SQL. As convention, SQL specific commands are written in uppercase while user defined instructions are written in lowercase. SQL queries should always end with a _semicolon (;)_.

```sql
-- 1. creating the schema
CREATE SCHEMA school_schema;
```
This creates a schema called school. Think of schema as the _folder_ that will contain all related work in one place. In the case of SQL, these include _tables_, _views_, _indexes_ etc. The '--' are comments which are not executed as part of the SQL command.

```sql
--setting the search path for the session
SET search_path = school_schema;
```
This is used in _Postgresql_ to instruct that all the commands we will run should be executed in the schema given.

```sql
--creating a students table
CREATE TABLE students (
student_id INT PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
gender VARCHAR(1),
date_of_birth DATE,
class VARCHAR(10),
city VARCHAR(50)
);
```

```sql
--Add a phone number column
ALTER TABLE students
ADD COLUMN
phone_number VARCHAR(20);
```
Renaming a column
```sql
--Rename credits column
ALTER TABLE subjects
RENAME COLUMN credits TO credit_hours;
```
Deleting a column
```sql
--Remove phone number column
ALTER TABLE students
DROP COLUMN phone_number;
```
Inserting data into a table
```sql
INSERT INTO students
VALUES
(1,'Amina','Wanjiku','f','2008-03-12','Form 3','Nairobi'),
(2,'Brian','Ochieng','m','2007-07-25','Form 4','Mombasa');
```

Updating a column in a record
```sql
UPDATE students
SET city = 'Nairobi' WHERE student_id = 1
RETURNING*;
```
The _returning*_ keyword shows us the result of our query after we execute it. IF we don't explicitly give the *WHERE* clause, all the records will have their _city_ column updated to _Nairobi_. The _WHERE_ clause acts as a guardrail to prevent this.

Deleting a record
```sql
--Delete student with id 2
DELETE FROM students 
WHERE student_id = 2
RETURNING*;
```

## Intermediate commands
```sql
--students neither in form 3 nor form 2
SELECT CONCAT(first_name,' ',last_name) AS student,class
FROM students GROUP BY class,student
HAVING class NOT IN ('form 3','Form 2') ORDER BY class;
```
![sql not in](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bsw2gzbtgzlaoosdfuvy.png)

Case statement to check condition first before assigning a value
```sql
--students classification as 'Senior' or 'Junior'
SELECT first_name,last_name,class,
CASE
	WHEN class IN ('Form 3', 'Form 4') THEN 'Senior'
	ELSE 'Junior'
END AS student_level
FROM students;
```

![Case in sql](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/j1nu9qcqp2cy2w8b9uim.png)




