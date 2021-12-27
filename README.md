# CLTV_Prediction
Predicting Customer Lifetime Value using BG/NBD and Gamma Gamma Models

What is CLTV Prediction:
CLTV Prediction is a time-projected probabilistic lifetime value estimation.
For CLTV estimation, two models “BG/NBD” & “GG” can be used.
CLTV = Expected Number of Transaction * Expected Average Profit
CLTV = (BG/NBD Model) * (Gamma Gamma Submodel)

BG/NBD Model Metrics:
1. Recency: # of weeks elapsed since the last purchase for a customer, on a weekly basis.
2. T (Tenure): # of weeks elapsed since the date of a customer’s first purchase from the analysis date. (also called customer’s age on a weekly basis)
3. Frequency: A customer’s total number of transactions/purchases

Gamma Gamma Model Metrics:
1. Monetary: Average spend per transaction by a customer (different from the Monetary metric defined in RFM scores)

Business Problem: An e-commerce website wants a forward projection for customer actions according to the CLTV values of its customers.
Is it possible to identify the customers who can generate the most revenue within the 6-month time period?

Data Set: The Online Retail II data set includes the sales of an online retail store based in the UK between 1/12/2009 and 09/12/2011. The product catalog of this company includes souvenirs. The vast majority of the company's customers are corporate customers.

Variables:

1. InvoiceNo: Invoice number. A unique number for each transaction. If it starts with C which means canceled operations.

2. StockCode: Product code. A unique number for each product.

3. Description: Product name.

4. Quantity: It refers to how many of the products in the invoices have been sold.

5. InvoiceDate: Invoice date.

6. UnitPrice: Product price (pound)

7. CustomerID: Unique customer number.

8. Country: The name of the country where the customer lives.
