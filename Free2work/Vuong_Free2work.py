# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 18:40:17 2024

@author: dangt
"""

import pandas as pd 

# Read given database
customer = pd.read_csv('customer.csv')

orders = pd.read_csv('orders.csv')

products = pd.read_csv('products.csv')

items = pd.read_csv('items.csv')


## 1  What is the average basket by product category?

# Create new table by merge products.csv and items.csv
table1 = pd.merge(products,items,left_on = "product_id",right_on = "product_id")
table1 = table1[["product_category_name","order_item_id"]]

# Count number of order
total_order = table1.groupby('product_category_name').count().reset_index()
total_order.columns = ['product_category_name', 'total_order']

# Count number of units
total_sell = table1.groupby('product_category_name')['order_item_id'].sum().reset_index()
total_sell.columns =  ['product_category_name', 'total_sell']

# Give the average basket number
average_basket = pd.merge(total_order,total_sell,left_on = 'product_category_name',right_on = 'product_category_name')
average_basket['average_basket'] = average_basket['total_sell']/average_basket['total_order']
print(average_basket)

## 2 What are the most popular products ?
# I list top 10 popular products
top_10_popular_products = average_basket.nlargest(10,'total_order')[['product_category_name','total_order']]
print(top_10_popular_products)


# Merge four given table together
table3 = pd.merge(customer,orders,left_on = "customer_id",right_on = "customer_id")
table3 = table3[["order_id","customer_id","customer_unique_id"]]
table3 = pd.merge(table3,items,left_on = "order_id", right_on = "order_id")
table3 = table3[["product_id","order_id","customer_id","customer_unique_id"]]
table3 = pd.merge(table3,products,left_on = "product_id",right_on = "product_id")
table3 = table3[["product_category_name","product_id","order_id","customer_id","customer_unique_id"]]

repeat_customer = table3[["customer_unique_id","customer_id","product_category_name"]]
repeat_customer = repeat_customer.groupby('customer_unique_id').count().reset_index()
repeat_customer.rename(columns={'customer_id': 'repeat_times'}, inplace=True)
repeat_customer["product_category_name"] = table3["product_category_name"]

## 4. How many customers are repeaters ?
print(repeat_customer)
real_repeat_customer = repeat_customer[(repeat_customer['repeat_times'] > 1)]
print(real_repeat_customer)

# There are 11870 customers who are repeater.

## 3. What are repeat customers mostly buying ?
repeat_buy = real_repeat_customer.groupby('product_category_name').count().reset_index()
repeat_buy = repeat_buy[["product_category_name","repeat_times"]]
top_10_repeat_buy_products = repeat_buy.nlargest(10,'repeat_times')[['product_category_name','repeat_times']]

print(top_10_repeat_buy_products)

## Customer segmentation
# We can have a simple customer segmentation by classification based on type of products.
# For example, we should focus on several types such as furniture products, sports products
# technology products and sort others in one type.


## Recommendation
# Based on the data that I have analysed, I would recommend the CEO of E-commercial company 
# strongly focus on advertise products based on category several categories like furniture
# sport, health, technologies stuff which are mostly bought and considered by customers
# Furthermore, customers have a tendency to rebuy these things again from the company. 



