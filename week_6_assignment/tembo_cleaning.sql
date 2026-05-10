CREATE SCHEMA IF NOT EXISTS tembo_hotel;

SET search_path TO tembo_hotel;

SHOW search_path; --confirm working on search path

CREATE TABLE IF NOT EXISTS bookings_staging (
    booking_id          TEXT,  
    guest_name          TEXT,
    guest_phone         TEXT,  
    guest_city          TEXT,
    guest_nationality   TEXT,  
    room_no             TEXT,
    room_type           TEXT,  
    room_rate_per_night TEXT,
    check_in_date       TEXT,  
    check_out_date      TEXT,
    nights_stayed       TEXT,  
    staff_name          TEXT,
    staff_department    TEXT,  
    staff_salary        TEXT,
    payment_method      TEXT,  
    booking_status      TEXT,
    total_amount        TEXT,  
    service_used        TEXT,
    service_price       TEXT,  
    guest_rating        TEXT
);

SELECT * FROM bookings_staging;

SELECT COUNT(*) FROM bookings_staging;

--CLEANING DATA

-- 1. booking_id
	UPDATE bookings_staging SET booking_id = TRIM(booking_id); --remove leading and trailing spaces
	
	--checking duplicates
	SELECT booking_id, COUNT(*) FROM bookings_staging
	GROUP BY booking_id  HAVING COUNT(*) > 1;
	
	--removing duplicates
	DELETE FROM bookings_staging
	WHERE ctid NOT IN (
	  SELECT MIN(ctid)
	  FROM bookings_staging
	  GROUP BY booking_id
	);
	
-- 2. guest_name
	UPDATE bookings_staging SET guest_name = TRIM(guest_name);

	SELECT DISTINCT guest_name FROM bookings_staging ORDER BY guest_name; -- checking guest_name status
	
	--sets column to first letter capitalize
	UPDATE bookings_staging 
	SET guest_name = INITCAP(guest_name);

	SELECT COUNT(*) FROM bookings_staging WHERE guest_name IS NULL OR guest_name = ''; --checking for nulls

-- 3. guest_phone
	UPDATE bookings_staging SET guest_phone = TRIM(guest_phone);
	
	SELECT DISTINCT guest_phone FROM bookings_staging ORDER BY guest_phone;
	
	SELECT guest_name,guest_phone FROM bookings_staging WHERE guest_phone IS NULL OR guest_phone = ''; --checking for nulls

	--removing nulls
	UPDATE bookings_staging
	SET guest_phone = 'not provided'
	WHERE guest_name = 'Patrick Ngugi';

	--getting rid of dash -
	UPDATE bookings_staging 
	SET guest_phone = REPLACE(guest_phone, '-', '') 

	--set the guest phone with 0 as prefix
	UPDATE bookings_staging
	SET guest_phone = CONCAT('0', RIGHT(guest_phone ,9))
	WHERE guest_phone NOT LIKE 'not provided';
	
-- 4. guest_city
	UPDATE bookings_staging SET guest_city = TRIM(guest_city);

	SELECT DISTINCT guest_city FROM bookings_staging ORDER BY guest_city; -- checking guest_city status
	
	--sets column to first letter capitalize
	UPDATE bookings_staging 
	SET guest_city = INITCAP(guest_city);

	--fill null city values
	SELECT * FROM bookings_staging WHERE guest_city IS NULL OR guest_city = '';
	
	UPDATE bookings_staging
		SET guest_city = 'not provided'
	WHERE guest_phone LIKE '078901234%' and guest_name LIKE 'Henry%' RETURNING*;
	
-- 5. guest_nationality
	UPDATE bookings_staging SET guest_nationality = TRIM(guest_nationality);

	SELECT DISTINCT guest_nationality FROM bookings_staging ORDER BY guest_nationality; -- checking guest_nationality status
	
	--sets column to first letter capitalize	
	UPDATE bookings_staging 
	SET guest_nationality = INITCAP(guest_nationality);

-- 6. room_no
	UPDATE bookings_staging SET room_no = TRIM(room_no); --remove leading and trailing spaces
	SELECT DISTINCT room_no FROM bookings_staging ORDER BY room_no; -- checking room_no status

-- 7. room_type
	UPDATE bookings_staging SET room_type = TRIM(room_type);

	SELECT DISTINCT room_type FROM bookings_staging ORDER BY room_type; -- checking room_type status

	--sets column to first letter capitalize
	UPDATE bookings_staging 
	SET room_type = INITCAP(room_type);

	-- change room type
	UPDATE bookings_staging
	SET room_type = CASE
						WHEN room_type = 'Dlx' THEN 'Deluxe'
						WHEN room_type = 'Std' THEN 'Standard'
						ELSE room_type
					END;
		
-- 8. room_rate_per_night
	UPDATE bookings_staging SET room_rate_per_night = TRIM(room_rate_per_night); --remove leading and trailing spaces
	SELECT DISTINCT room_rate_per_night FROM bookings_staging ORDER BY room_rate_per_night; --checking room_rate_per_night status

-- 9. check_in_date
	UPDATE bookings_staging SET check_in_date = TRIM(check_in_date); --remove leading and trailing spaces
	SELECT DISTINCT check_in_date FROM bookings_staging ORDER BY check_in_date; -- checking check_in_date status

	--format date like '06/08/2024' to '2024/08/06'
	BEGIN;
		UPDATE bookings_staging
		SET check_in_date = TO_CHAR(
		    TO_DATE(check_in_date, 'DD/MM/YYYY'),
		    'YYYY-MM-DD')
		WHERE check_in_date ~ '^\d{2}/\d{2}/\d{4}$';
		
	--format date like '27-02-24' to '2024/02/27'
		UPDATE bookings_staging
		SET check_in_date = TO_CHAR(
		    TO_DATE(check_in_date, 'DD-MM-YY'),
		    'YYYY-MM-DD')
		WHERE check_in_date ~ '^\d{2}-\d{2}-\d{2}$';
	
	--format date like '15-11-2024' to '2024-11-15'
	BEGIN;
	UPDATE bookings_staging
	SET check_in_date = TO_CHAR(
	    TO_DATE(check_in_date, 'DD-MM-YYYY'),
	    'YYYY-MM-DD')
	WHERE check_in_date ~ '^\d{2}-\d{2}-\d{4}$';
	SELECT booking_id,check_in_date,check_out_date from bookings_staging where booking_id = 'BK9005';
	ROLLBACK;

-- 10. check_out_date
	UPDATE bookings_staging SET check_out_date = TRIM(check_out_date); --remove leading and trailing spaces
	SELECT DISTINCT check_out_date FROM bookings_staging ORDER BY check_out_date; -- checking check_out_date status

	--format date like '06/08/2024' to '2024/08/06'
	UPDATE bookings_staging
	SET check_out_date = TO_CHAR(
		TO_DATE(check_out_date, 'DD/MM/YYYY'),
		'YYYY-MM-DD')
	WHERE check_out_date ~ '^\d{2}/\d{2}/\d{4}$';

	--format date like '27-02-24' to '2024/02/27'
	UPDATE bookings_staging
	SET check_out_date = TO_CHAR(
		TO_DATE(check_out_date, 'DD-MM-YY'),
		'YYYY-MM-DD')
	WHERE check_out_date ~ '^\d{2}-\d{2}-\d{2}$';
	ROLLBACK;
	
-- 11. nights_stayed
	UPDATE bookings_staging SET nights_stayed = TRIM(nights_stayed); --remove leading and trailing spaces
	SELECT DISTINCT nights_stayed FROM bookings_staging ORDER BY nights_stayed; -- checking nights_stayed status

	--make text value absolute when changing to integer
	UPDATE bookings_staging 
	SET nights_stayed = REPLACE(nights_stayed, '-', '') ;

-- 12. staff_name
	SELECT DISTINCT staff_name FROM bookings_staging ORDER BY staff_name; -- checking staff_name status

	--sets column to first letter capitalize
	UPDATE bookings_staging
	SET staff_name = INITCAP(TRIM(staff_name));

-- 13. staff_department
	UPDATE bookings_staging SET staff_department = TRIM(staff_department); --remove leading and trailing spaces
	SELECT DISTINCT staff_department FROM bookings_staging ORDER BY staff_department; -- checking staff_department status

-- 14. staff_salary
	UPDATE bookings_staging SET staff_salary = TRIM(staff_salary); --remove leading and trailing spaces
	
	SELECT DISTINCT staff_salary FROM bookings_staging ORDER BY staff_salary; -- checking staff_salary status

	--set null values
	UPDATE bookings_staging
	SET staff_salary = NULL WHERE staff_salary LIKE ',';
	
	--remove 'KES ' from staff salary
	UPDATE bookings_staging 
	SET staff_salary = REPLACE(staff_salary, 'KES ', '') 
	WHERE staff_salary LIKE 'K%';
	
	--remove any commas ',' from staff salary
	UPDATE bookings_staging 
	SET staff_salary = REPLACE(staff_salary, ',', '') 
	WHERE staff_salary LIKE '%,%';

-- 15. payment_method
	SELECT DISTINCT payment_method FROM bookings_staging ORDER BY payment_method; -- checking payment_method status
	
	UPDATE bookings_staging --sets column to first letter capitalize
	SET payment_method = INITCAP(TRIM(payment_method));

	-- standardize payment method column
	UPDATE bookings_staging
	SET payment_method = 'M-Pesa'
		WHERE payment_method = 'Mpesa';

-- 16. booking_status
	SELECT DISTINCT booking_status FROM bookings_staging ORDER BY booking_status; -- checking booking_status status
	UPDATE bookings_staging SET booking_status = INITCAP(TRIM(booking_status)); --standadize the booking status

-- 17. total_amount
	UPDATE bookings_staging SET total_amount = TRIM(total_amount); --remove leading and trailing spaces
	SELECT DISTINCT total_amount FROM bookings_staging ORDER BY total_amount; -- checking total_amount status

	--set null values
	UPDATE bookings_staging
	SET total_amount = NULL WHERE total_amount LIKE ',';
	
	--remove 'KES ' from total amount
	UPDATE bookings_staging 
	SET total_amount = REPLACE(total_amount, 'KES ', '') 
	WHERE total_amount LIKE 'K%';
	
	--remove any commas ',' from total amount
	UPDATE bookings_staging 
	SET total_amount = REPLACE(total_amount, ',', '') 
	WHERE total_amount LIKE '%,%';

-- 18. service_used
	UPDATE bookings_staging SET service_used = TRIM(service_used); --remove leading and trailing spaces
	SELECT DISTINCT service_used FROM bookings_staging ORDER BY service_used; -- checking service_used status
	SELECT service_used FROM bookings_staging WHERE service_used IS NULL OR service_used = ''; --checking null values

-- 19. service_price
	UPDATE bookings_staging SET service_price = TRIM(service_price); --remove leading and trailing spaces
	SELECT DISTINCT service_price FROM bookings_staging ORDER BY service_price; -- checking service_price status
		 
-- 20. guest_rating
	UPDATE bookings_staging SET guest_rating = TRIM(guest_rating); --remove leading and trailing spaces
	SELECT DISTINCT guest_rating FROM bookings_staging ORDER BY guest_rating; -- checking guest_rating status
	SELECT guest_name,guest_rating FROM bookings_staging WHERE guest_rating IS NULL OR guest_rating IN ('0','6',''); --checking null values
	
	UPDATE bookings_staging
	SET guest_rating = CASE
							WHEN guest_rating = '6' THEN '5'
							WHEN guest_rating = '0' OR guest_rating IS NULL THEN '1'
							ELSE guest_rating
						END;

--bookings_table
	CREATE TABLE IF NOT EXISTS bookings (
	booking_id VARCHAR(10) PRIMARY KEY,
	guest_name VARCHAR(100),
	guest_phone VARCHAR(15),
	guest_city VARCHAR(60),
	guest_nationality VARCHAR(60),
	room_no VARCHAR(5),
	room_type VARCHAR(20),
	room_rate_per_night NUMERIC(10,2),
	check_in_date DATE,
	check_out_date DATE,
	nights_stayed INTEGER,
	staff_name VARCHAR(100),
	staff_department VARCHAR(50),
	staff_salary NUMERIC(10,2),
	payment_method VARCHAR(20),
	booking_status VARCHAR(20),
	total_amount NUMERIC(12,2),
	service_used VARCHAR(60),
	service_price NUMERIC(10,2),
	guest_rating INTEGER
	);



select * from bookings_staging;
--Inserting data into table
	INSERT INTO bookings
	SELECT
		booking_id,
		guest_name,
		guest_phone,
		guest_city,
		guest_nationality,
		room_no,
		room_type,
		room_rate_per_night::numeric,
		check_in_date::date,
		check_out_date::date,
		nights_stayed::int,
		staff_name,
		staff_department,
		staff_salary::numeric,
		payment_method,
		booking_status,
		total_amount::numeric,
		service_used,
		service_price::numeric,
		guest_rating::int	
	FROM bookings_staging;










	
