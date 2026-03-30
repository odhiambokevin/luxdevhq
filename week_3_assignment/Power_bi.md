# Understanding Data Modeling in Power BI: Joins, Relationships, and Schemas Explained
Many times while working with relational data, the need to get context information from other data tables and sources will arise. Understanding how to perform modelling when working with such situations is essential. Let us look at some data modelling concepts when working in Power Bi.

### Joins
In Power Bi, joins are called _Merge queries_. This is when two tables are joined together depending on matching values from columns. At least once column in the two tables must have matching values eg. an _id_ appearing both in _users table_ and a similar matching _id_ value appearing in _subscriptions table_. The names of the two columns do not need to be same, but the underlying values must match.

In most cases, this involves a _primary key_ from one table and a _foreign key_ in the other table. To perform joins in Power Bi, we select _Merge queries_ command from the home tab.

![Merge queries command](https://learn.microsoft.com/en-us/power-query/media/merge-queries-overview/merge-icons.png)
######Image from _learn.microsoft.com_

Several types of joins are available in Power Bi:
1. **inner join:** returns only matching rows from both the left and right tables
![inner join](https://learn.microsoft.com/en-us/power-query/media/merge-queries-inner/inner-join-operation.png)
######Image from _learn.microsoft.com_

2. **left outer join:** returns all the rows from left table but only the rows from the right table that have a match
![left outer join](https://learn.microsoft.com/en-us/power-query/media/merge-queries-left-outer/left-outer-join-operation.png)
######Image from _learn.microsoft.com_
3. **right outer join:** returns all the rows from right table but only the rows from the left table that have a match
![right outer join](https://learn.microsoft.com/en-us/power-query/media/merge-queries-right-outer/right-outer-join-operation.png)
######Image from _learn.microsoft.com_

4. **full outer join:** returns all the rows from both the left and right tables
![full outer join](https://learn.microsoft.com/en-us/power-query/media/merge-queries-full-outer/full-outer-join-operation.png)
######Image from _learn.microsoft.com_

5. **left anti join:** returns only records from left table that do not have matching rows in the right table
![left anti join](https://learn.microsoft.com/en-us/power-query/media/merge-queries-left-anti/left-anti-join-operation.png)
###### Image from _learn.microsoft.com_

6. **right anti join:** returns only records from right table that do not have matching rows in the left table
![right anti join](https://learn.microsoft.com/en-us/power-query/media/merge-queries-right-anti/right-anti-join-operation.png)
###### Image from _learn.microsoft.com_

7. **fuzzy merge:** this is only supported over text columns. It aims to provide a more standardadized way of representing text data in a columns eg. where distinct names are misspelled eg Vollvo instead of Volvo. It it preceded by another join type, typically, left outer join. 
![fuzzy match](https://learn.microsoft.com/en-us/power-query/media/merge-queries-fuzzy-match/sample-output-table-2.png)
###### Sample goal of fuzzy join from _learn.microsoft.com_

8. **cross join:** results in a Cartesian-like result from the two tables
you first select a table of interest then click on _custom column_ command from the _Add column_ tab on the ribbon.
![custom cross join](https://learn.microsoft.com/en-us/power-query/media/cross-join/add-column-icon.png)
#### image from _learn.microsoft.com_
Enter any name for the new custom column in the dialogue window that appears. In the _Custom column formula*_ enter the name of the other table or query. Here it is called _Colors_
![custom column](https://learn.microsoft.com/en-us/power-query/media/cross-join/add-column-window.png)
###### Image from _learn.microsoft.com_

Select _ok_ and also _expand the new column_ and click _ok_ again to view final result.
![cross join](https://learn.microsoft.com/en-us/power-query/media/cross-join/cross-join-final-table-2.png)
###### Image from _learn.microsoft.com_

### Relationships
There are 4 main types of relationships called **_cardinality_**
_1. Many to one(*:1):_ It is the default. A column can have many instances of a value and only have one instance of the same value in the other table, known as a lookup table.
_2. One to one(1:1):_ A columns can have only one instance of a value and also only one instance of the value in the other table.
_3. One to many(1:*):_ A columns has only one instance of a value but can have many instances in the other table
_4. Many to many(*:*):_ There are no unique constraints on values in the tables.

_**Active relationships**_ in Power Bi are shown by solid continuous lines while inactive relationships are shown by dotted lines. Only one active path exists between tables and this is used to filter data for visuals.

######Joins vs relationships
From the foregoing, we can see that joins physically merge tables while relationships only show linkages between tables.

### Schemas
In Power Bi, schemas describe how your data is organized and structured. A well designed data model improves the performance of your queries as well as usability of in DAX.

A few concepts are worth noting when dealing with schemas in Power Bi:
1. _Dimension tables_: These tables describe the things being modeled such as products or places.
2. _Fact tables_: They store observations or events and contain dimension key columns.

#### 1. Star schema
Tables are classified either as dimension of fact tables.
![star schema](https://radacad.com/wp-content/uploads/2019/05/2019-05-13_15h19_32.png)
###### star schema from _radacad.com_

_Normalizing tables_ in star schema involves storing data in fact tables by avoiding repetition.

#### 2. Snowflake
It is some sort of a normalized version of star schema. Dimension tables are broken down further into sub-dimensions and end up forming branch-like structure.
![snowflake schema](https://www.mssqltips.com/wp-content/images-tips/7617_what-is-a-snowflake-schema.002.png)
###### Image from _mmsqltips.com_

#### 3. Flat Table (DLAT)
Data is entered and consolidated into one single table. The table is usually very wide and has no relationship with other tables.
![flat table](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*qLEcxmT366PPUcmuaoy3Lg.png)
###### Image by _Firat_ on _medium.com_

It is called DLAT(denormalized large aggregation table)

### Role playing dimensions
These occur when a single dimension table can be used to filter a fact table. A fact table of sales, for instance, can be filtered based on the dates, such as _order_date_, _shipping_date_ to show these specific analysis for dates.

### Common modelling issues in Power Bi
Some common issues you might run into when working with Power Bi include the following:
1. Overloading the model: Trying to load everything instead of just what is needed from the slow. This might result in slow query processes. Reduce the number of columns used and remove any unnecessary field to improve the model.
2. Overusing the calculation to create new columns instead of just creating a new measure can lead to excessive use of RAM. It is recommended to use measures for aggregation and only use calculated columns when necessary.
3. Ignoring data types: Data should always be in the correct types to improve on the model. It is advisable to first transform the data in Power Query before loading.
4. Misconfiguring the table relationships can lead to circular dependencies or broken relationships. Particularly, using many-to-many relationships inaccurately can lead to double counts and eventual inaccurate data.

