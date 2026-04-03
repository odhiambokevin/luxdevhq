#A comprehensive guide to publishing and embedding power bi reports on the web wit iframes
This

Successful transformation of data in power query

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ro1jopjdud831qdchb41.png)

The data opens in power bi


Total Sales


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zd956ym6s0wbdvo5uay8.png)

Profit margin rounded

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4y58c233lrh97p5g0e7n.png)


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7snzwcl7wzrelonew9yt.png)

profit margin by product and country

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7235o5p1jpem05r1n3qz.png)

convert currency to usd

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yi05jok9sxl12jhwd1qj.png)

changing currency to USD

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ajhosyflaq638yqdp7eh.png)


Missing or incorrect values
Missing data values can be standardized as pseudo blanks to be null or not provided for numbers and text respectively in power query.

For missing numeric values, median is the best as it accounts for skewed data. Mode is recommended for text, categorical or nominal categorical data.

Mean is advised for data with normal distributed data.

Duplicating and deleting rows


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/empg4ftw5vahx7nn36tj.png)

add new null column

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0p1zb6tuzw3732f7idm3.png)

change columnn type

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kdy30gthg68lp57yvycv.png)

filter values

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kpsiicotu8azeye1bsdk.png)

Adding customer ID, work around 
Go to transform then group by select a unique identifier column eg. Customeremail, select count distinct

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9byaiezksv57u4vq84jm.png)

Then create new index and then rename and delete the previous CustomerID


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/t7mcf1dtbpn82hr62ra8.png)




click add index then give start from 1

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8dg5tfdlsr4bvicpwqlx.png)

then click expand double side arrow icon from the CustomerID email


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7cqfxtjuex5nwzigooa5.png)


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q33tzvvbl955iv998i9q.png)

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/77c6isbdh1nfhfpauwuz.png)

rename column

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p5x6aeqp22k0l5npnh4t.png)
