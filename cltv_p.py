#Importing libraries & data preparing & data reading 
#!pip install Lifetimes
import datetime as dt
import pandas as pd
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from sqlalchemy import create_engine

df_ = pd.read_excel("/Users/simalgezer/Desktop/VBO/week 3/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.head()

df = df[df["Country"] == "United Kingdom"]
df.dropna(inplace=True)
df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[df["Quantity"] > 0]
df = df[(df['Price'] > 0)]

df.describe().T

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit
    
replace_with_thresholds(df, "Quantity")
replace_with_thresholds(df, "Price")


df["TotalPrice"] = df["Quantity"] * df["Price"]
df.head()

today_date = dt.datetime(2011, 12, 11)

#Preparing CLTV data structure
cltv_df = df.groupby('CustomerID').agg({'InvoiceDate': [lambda date: (date.max() - date.min()).days,
                                                        lambda date: (today_date - date.min()).days],
                                        'Invoice': lambda num: num.nunique(),
                                        'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
cltv_df.columns = cltv_df.columns.droplevel(0)
cltv_df.head()

cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
cltv_df = cltv_df[cltv_df["monetary"] > 0]
cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
cltv_df["recency"] = cltv_df["recency"] / 7
cltv_df["T"] = cltv_df["T"] / 7

cltv_df.head()

#Establishing BG/NBD Model
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T'])

#Establishing Gamma Gamma Model
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
cltv_df["expected_average_profit clv"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                             cltv_df['monetary'])
#Calculating 6-month CLTV Prediction with BG/NBD and GG Models
cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency'],
                                   cltv_df['T'],
                                   cltv_df['monetary'],
                                   time=6,
                                   freq="W",
                                   discount_rate=0.01)


cltv.head()
cltv.shape
cltv = cltv.reset_index()
cltv.head()


cltv.sort_values(by="clv", ascending=False).head(50)
cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left")
cltv_final.sort_values(by="clv", ascending=False)[10:30]

#Standardizing CLTV prediction values
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(cltv_final[["clv"]])
cltv_final["SCALED_CLTV"] = scaler.transform(cltv_final[["clv"]])
cltv_final.sort_values(by="clv", ascending=False)[10:30]
cltv_final.head()

#Segmenting standardized CLTV prediction value
cltv_final["segment"] = pd.qcut(cltv_final["SCALED_CLTV"], 4, labels=["D", "C", "B", "A"])
cltv_final["segment"].value_counts()
cltv_final.head()

#Reviews about some of the segments
#Through segments, I observed that the customers in segment D have the lowest scaled_cltv forecast. 
#Therefore, marketing strategies should be focused on the recovery of this risky customer segment.
#On the other hand, the customers with the highest scaled_cltv predictions are segment A. 
#These customers are the most important to us. Hence, another marketing strategy should be targeted to this segment.

