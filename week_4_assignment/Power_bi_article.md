# A Comprehensive Guide to Publishing Power Bi Reports

One you have selected your data source in a new session on Power Bi desktop application, load data into power query to transform it.

![Getting data](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/l5jf0h24j5mz7ezl3275.png)

In case of a mutli-sheet workbook in Excel, select sheet(s) you intend to work with. They will eventually be made into tables in Power Bi. Then click on _transform data_.

![Transformdata](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/aejerm7519zjb2s4u3dq.png)

Ensure to check for inconsistent data from column filters. Standardize any inconsistent data as well as blanks and pseudo-blanks. Using the column filter we are able to see categories for each column at a glance. This would help identify blanks, inconsistencies and missing values.

![Column filter](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8cjujcw8zwgrj4fel1ju.png)

Click _close and apply_ to load data into Power Bi.

![Loading to Power Bi](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vyzcvnli5pmgpxoicaxk.png)

Select the sheet from data pane and right click to rename it into something meaningful. Remember to save progress in location of our choice to avoid data loss.

![Rename sheet](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/87ezad6smn00g0899mbr.png)

## 1. Total sales from all products.
Since we already have sales for each individual product, we simply use SUM function to get the total for the _SalesAmount_ column. Click on _New Measure_, give it a descriptive name and enter the function:

![Total sales](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2xy0onx8wbp4syzidwe4.png)

## 2. Profit Margin

Profit margin is calculated by _profit/SalesAmount * 100_. Since we already have the total value for sales amount calculated above, we will use _SUMX_ to calculate the profit. Our new expression will be as shown:

![SumX](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kqr3hvsyevh7ag8dspuj.png)

The _SUMX_ above encloses the profit for each row. It calculates profit for each row and also a sum at the end. For each row, this value is used to calculate the profit margin.

This will allow us to filter by _country_, _product_ in the _report view_.

![Filter](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/v158x35oietvxwnhat4x.png)

## 3. Change currency to USD
Currency is changed to USD from CAD for all columns that have currency using the formula below.

### Shipping cost to USD

![Shipping](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kgqmmm112vfw0xcgu14l.png)

### Sales Amount to USD

![Sales](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/06pe31xg447c5ri5lxii.png)

### Profit to USD

![Profit](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vpbmtu7m37zhvoopttbu.png)

## 4. Missing or incorrect values
Missing data values can be standardized as pseudo blanks for text columns or to be null for numbers.

In addressing missing numeric values, median is the best option as it accounts for skewed data. Mode is recommended for text, categorical or nominal categorical data. Mean is advised for data with normal distributed data.

## 5. Model data
Modelling our data involves creating dimensions tables and a fact table. Click on _Transform data_ in Power Bi to open Power Query. Duplicate the existing table to the number of total tables (_dimension tables and fact tables_) needed.

Except for the fact table, columns not needed in each dimension table are deleted. Columns in the _fact table_ are kept as is to use in the subsequent steps of creating unique identifiers for all _dimension tables_.

Click on _Close & Apply_ to effect the changes and return to Power Bi.

**Tip**: Always keep a copy of the original table/data.

### Date Table
To create a date table, click on the _New Table_ command in Power Bi.

![Date](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2a2wu13hc72w9qlfb0k9.png)

Enter the formula below to create the table:

![Creating date table](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8xavtkda8d2whuontva7.png)

_CALENDARAUTO()_ generate a new date column based on all the dates in our data. To limit the use of possible unnecessary date columns that might exist in our data, eg. _Date of Birth_, we create new variables and determine the range our date should fall in. In this example, the _MinDate_ looks for the earliest date an order was placed and the _MaxDate_ returns the most recent date for delivery.

The filter is then used to give _CALENDARAUTO()_ the date range to filter from based on these two values.

The other Date-related columns are derived from the date column returned by _CALENDARAUTO()_ function.

Here is a view of our tables after the steps.

![Tables](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0h7u5do2etdvcxja6fi6.png)

### Creating unique identifiers
All our dimension tables will need unique identifiers to be linked to the fact table.

#### 1. Create Unique ID in the dimension table
Click _CustomerEmail_ from the customers table and select _Remove Duplicates_ from the drop down.

![Remove duplicates](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wi44jl4pxzyc73jkiclr.png)

Unique email identifiers remain.

From the _Add Column_ tab, click on _Index Column_ and the initiator of choice, in this case, _Custom_.

![Custom](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xm0u108j1qk3g8hbd9w6.png)

Define the desired index format and increment and click _OK_.

![Index](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/l1qgq2zbifs0uf2iceh8.png)

I rename the column to _CustomerID_, this is what we will use to join it in the _fact table_. I also change the type to text. This just as a personal preference for columns that eventually may include a lot of records.

![New column](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d5usev9vsalz6ey0u19o.png)

_**NOTE: REPEAT THIS PROCESS FOR THE OTHER DIMENSION TABLES**_

#### 2. Merge the Fields from the tables
Still in the Power Query editor, click on the _fact table_ and select _Merge Queries_ from the ribbon.

Select _Left Outer Join_ with the _fact table_ as the first table. You see from the image below we get all records matching. Click ok.

![Merge queries](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/z74gle1z5uxn24lmxle1.png)

Click on the expand tables icon.

![Expand table](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zb5wbpiz0kkj87svnhfw.png)

Deselect all column names except the _CustomerID_. Our new fact table will have this column included.

![New id column](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ez7lcqt0vjs9rn6lfs8m.png)

Our _CustomerID_ is now included in the _fact table_.

![New table](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zv6tnufohklywk3w706f.png)

Repeat for the other dimension tables.

The Relationship and view should be as shown

![Relationship](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/s3d3rrqyiasjbpqlumrj.png)

## 6. Report and Dashboard
Go to the report view and select visualization build from the side panel as needed. Add your key overview metrics from the different values. This will from the dashboard as shown.

![Report](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/uga0kbbc92dnhspzyphs.png)

Save your work and click on publish. Log in to a Power Bi account from the Power Bi Service online and select the option to create a workspace.

![Workspace](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8vmg22rsiyndaclp0ohm.png)

Give the workspace a name. Log in to the Power Bi account from your desktop application and click on publish. Choose the same workspace created earlier to publish the report to. You have now published your report.

Create a new page on the Power Bi desktop application and give it a relevant name for specific metrics to be shown.

![Report app](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ao7i4egzxxh9ccw8agka.png)

This will form the individual reports of your work.

![Naming reports](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ncf0z7ue3yv5hxv1fxlx.png)

The published work should reflect on the online Power Bi service.

![Work online](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/elx5tsnahfkqlbqnnyjy.png)

### Embedding

To embed the report in another online document such as a webpage, click on  _File_ then select the _Embed report_ then _Website or portal_.

![Embed](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2lbzwbhjy0b9hwvmazkx.png)

Copy the resulting iFrame for embedding inside a html document.

![Iframe](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vuu3in26sqhpfvt54w0o.png)

![Embed iframe](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/95lu95ej1vnuuc0ui5ki.png)

Your Power Bi Report page will appear on the html document.

![Live document](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dwhagiztrzd0770nxrmz.png)