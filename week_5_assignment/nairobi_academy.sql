-- SECTION A

-- 1. creating the schema
create schema nairobi_academy;

--setting the search path for the session
set search_path = nairobi_academy;

--confirm the search path is applied
show search_path;

-- 2. create students table
create table students (
student_id INT PRIMARY key,
first_name VARCHAR(50) not null,
last_name VARCHAR(50) not null,
gender VARCHAR(1),
date_of_birth DATE,
class VARCHAR(10),
city VARCHAR(50)
);

-- 3. create subjects table
create table subjects (
subject_id INT primary key,
subject_name VARCHAR(100) not null unique,
department VARCHAR(50),
teacher_name VARCHAR(100),
credits INT
);

-- 4. create exam results table
create table exam_results (
result_id INT primary key,
student_id INT not null,
subject_id int not null,
marks int not null,
exam_date DATE,
grade VARCHAR(2)
);

-- 5. Adding phone number column
alter table students
add column
phone_number VARCHAR(20)
;

-- 6. Rename credits column
alter table subjects
rename column credits to credit_hours;

-- 7. Remove phone number column
alter table students
drop column phone_number;

-- SECTION B

-- 8. Insert students into table
insert into students
values
(1,'Amina','Wanjiku','f','2008-03-12','Form 3','Nairobi'),
(2,'Brian','Ochieng','m','2007-07-25','Form 4','Mombasa'),
(3,'Cynthia','Mutua','f','2008-11-05','Form 3','Kisumu'),
(4,'David','Kamau','m','2007-02-18','Form 4','Nairobi'),
(5,'Esther','Akinyi','f','2009-09-30','Form 2','Nakuru'),
(6,'Felix','Otieno','m','2009-09-14','Form 2','Eldoret'),
(7,'Grace','Mwangi','f','2008-01-12','Form 3','Nairobi'),
(8,'Hassan','Abdi','m','2007-07-09','Form 4','Mombasa'),
(9,'Ivy','Chebet','f','2009-12-01','Form 2','Nakuru'),
(10,'James','Kariuki','m','2008-08-17','Form 3','Nairobi');

-- 9. Insert subjects into table
insert into subjects
values
(1,'Mathematics','Sciences','Mr.Njoroge',4),
(2,'English','Languages','Ms.Adhiambo',3),
(3,'Biology','Sciences','Ms.Otieno',4),
(4,'History','Humanities','Mr.Waweru',3),
(5,'Kiswahili','Languages','Ms.Nduta',3),
(6,'Physics','Sciences','Mr.Kamande',4),
(7,'Geography','Humanities','Ms.Chebet',3),
(8,'Chemistry','Sciences','Ms.Muthoni',4),
(9,'Computer Studies','Sciences','Mr.Oduya',3),
(10,'Business Studies','Humanities','Ms.Wangari',3);

-- 10. Insert results into table
insert into exam_results
values
(1,1,1,78,'2024-03-15','B'),
(2,1,2,85,'2024-03-16','A'),
(3,2,1,92,'2024-03-15','A'),
(4,2,3,55,'2024-03-17','C'),
(5,3,2,49,'2024-03-16','D'),
(6,3,4,71,'2024-03-18','B'),
(7,4,1,88,'2024-03-15','A'),
(8,4,6,63,'2024-03-19','C'),
(9,5,5,39,'2024-03-20','F'),
(10,6,9,95,'2024-03-21','A');

-- 11. Select all columns from all three tables
select * from students;
select * from subjects;
select * from exam_results;

-- 12. Akinyi city change to Nairobi from Nakuru
update students
set city = 'Nairobi' where student_id = 5
returning*;

-- 13. update result for id 5
update exam_results
set marks = 59 where result_id = 5
returning*;

-- 14. delete exam result with id 9
delete from exam_results 
where result_id = 9
returning*;

-- SECTION C

-- 15. All Form 4 students
select concat(first_name,' ',last_name) as student,class
from students
where class = 'Form 4';

-- 16. All subjects in Sciences department
select subject_name,department from subjects
where department = 'Sciences';

-- 17. Marks greater than or equal to 70
select result_id,student_id,grade,marks
from exam_results
where marks >= 70;

-- 18. All female students
select concat(first_name,' ',last_name) as student,gender,class
from students
where gender = 'f';

-- 19. Form 3 students from Nairobi
select concat(first_name,' ',last_name) as student,city,class
from students
where class = 'Form 3' and city = 'Nairobi';

-- 20. Form 2 and Form 4 students
select concat(first_name,' ',last_name) as student,class
from students
where class in ('Form 2','Form 4') order by class;

----------------------------------PART 2 ---------------
-- SECTION A
-- 1. Exam results between 50 and 80
select * from exam_results
where marks between 50 and 80;

-- 2. Exams done between 15th March 2024 and 18th March 2024.
select * from exam_results
where exam_date between '2024-03-15' and '2024-03-18';

-- 3. Students living in Nairobi,Mombasa or Kisumu
select concat(first_name,' ',last_name) as student,class,city
from students group by city,class,student
having city in ('Nairobi','Mombasa','Kisumu')  order by city;

-- 4. Students neither in form 3 nor form 2
select concat(first_name,' ',last_name) as student,class
from students group by class,student
having class not in ('form 3','Form 2')  order by class;

-- 5. Students with first name starts with A or E
select concat(first_name,' ',last_name) as student
from students 
where first_name like 'A%' or first_name like 'E%'  ;

-- 6. Subject with *studies* in name
select * from subjects
where subject_name like '%Studies%';

-- SECTION B
-- 7. Number of students in Form 3
select count(student_id) as form_3_students
from students
where class = 'Form 3';

-- 8. Exam results with marks 70 and above
select count(result_id) as marks_above_70
from exam_results
where marks >= 70;

-- SECTION C
-- 9. Label marks as Distinction,Merit or Pass
alter table exam_results 
add column description VARCHAR(30);

update exam_results 
set description = 
case
	when marks >= 80 then 'Distinction'
	when marks >= 60 then 'Merit'
	when marks >= 40 then 'Pass'
	else 'Fail'
END
;

-- 10. Students classification as 'Senior' or 'Junior'
select first_name,last_name,class,
case
	when class in ('Form 3', 'Form 4') then 'Senior'
	else 'Junior'
end as student_level
from students;















































