# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 21:45:22 2023

@author: akis gazepidis
"""

import pandas as pd
import streamlit as st
pd.set_option('float_format', '{:f}'.format)

################## Import Datasets and Make Configurations ######################################
df = pd.read_csv("Assessment exercise dataset - orders.csv")
df['order_id'] = df['order_id'].astype("str")
df['user_id'] = df['user_id'].astype("str")

clustering_df = pd.read_csv("customer_clustering_analysis.csv")


####################### Create df_Breakfast_or_not dataframe for 1st Graph ############################
df_Breakfast_or_not  = pd.DataFrame(df.cuisine.value_counts()/df.shape[0]).reset_index().rename(columns={"index":'cuisine', "cuisine":'customer percentages'})



df_groupedby_user = df.groupby('user_id').agg({'order_id': "count",
                             'amount': 'sum'}).reset_index(drop=False)
                             
df_groupedby_user['amount_per_order'] = df_groupedby_user.amount/df_groupedby_user.order_id

df_groupedby_user.sort_values(['order_id', 'amount'], 
                                ascending= [False, False], 
                                inplace=True)

####################### Create has_ordered_once_breakfast dataframe for 2nd Graph ############################
def has_ordered_once_breakfast(x):
    if x==1:
        return "Yes"
    else:
        return "No"
    
df_breakfast = df[df.cuisine == "Breakfast"]
df_groupedby_breakfast_user = df_breakfast.groupby('user_id').agg({'order_id': "count",
                             'amount': 'sum'}).reset_index(drop=False)
                             
df_groupedby_breakfast_user['amount_per_order'] = df_groupedby_breakfast_user.amount/df_groupedby_breakfast_user.order_id

df_groupedby_breakfast_user.sort_values(['order_id', 'amount'], 
                                ascending= [False, False])

df_groupedby_breakfast_user['has_ordered_once_breakfast'] = df_groupedby_breakfast_user['order_id'].apply(lambda x: has_ordered_once_breakfast(x))

df_has_ordered_once_breakfast  = pd.DataFrame(df_groupedby_breakfast_user.has_ordered_once_breakfast.value_counts()/df_groupedby_breakfast_user.shape[0]).reset_index().rename(columns={"index":'has_ordered_once_breakfast','has_ordered_once_breakfast': 'percentages'})



####################### Create Customer clustering barchart dataframe for 3rd Graph ############################

clustering_names_perc  = (clustering_df.groupby("cluster_name").count()[["user_id"]]/clustering_df.shape[0]).reset_index()
clustering_names_perc = clustering_names_perc.rename(columns={"user_id":"cluster_percentages"})

############################## Efood Dashboard ###############################################
st.markdown("<h1 style='text-align: center; color: red;'>Efood Assesment</h1>", unsafe_allow_html=True)
st.subheader("Customer Segmentation - Breakfast Marketing Campaign")
st.text("-Need to segment existing customers based on their frequency and order value.")
st.text("")
st.text("-Segment that could be a target group for a Marketing campaign about 'Breakfast'?")
st.text("")
st.text("")

st.markdown("<h2 style='text-align: center; color: white;'>Orders per Cuisine</h2>", unsafe_allow_html=True)
st.bar_chart(data=df_Breakfast_or_not, x="cuisine", y="customer percentages", width=0, height=0, use_container_width=True)
st.text("")
st.subheader("We can see that 40% of the customers are ordering from Breakfast Cuisine.")

st.markdown("<h2 style='text-align: center; color: white;'>Customers orders one or more</h2>", unsafe_allow_html=True)
st.bar_chart(data=df_has_ordered_once_breakfast, x="has_ordered_once_breakfast", y="percentages", width=0, height=0, use_container_width=True)
st.text("")
st.subheader("We can see that over 40% of the Breakfast cuisine customers have ordered only one time Breakfast.")
st.subheader("Based on the above graph there is a potential growth on Breakfast cuisine market.")
st.text("")

st.markdown("<h2 style='text-align: center; color: white;'>Customer Clusters Allocation</h2>", unsafe_allow_html=True)
st.bar_chart(data=clustering_names_perc, x="cluster_name", y="cluster_percentages", width=0, height=0, use_container_width=True)
st.text("")

st.subheader("After conducting a clustering analysis 3 cluster of customers created based on their chqaracteristics.")
st.subheader("- Low spend customers")
st.text("Order counts mean: 2.324")
st.text("Cluster amount mean: 18.944")
st.text("Cluster amount_per_order mean: 9.542")
st.text("")

st.subheader("- Average type customers")
st.text("Order counts mean: 8.498")
st.text("Cluster amount mean: 73.743")
st.text("Cluster amount_per_order mean: 11.156")
st.text("")

st.subheader("- VIP customers")
st.text("Order counts mean: 20.631")
st.text("Cluster amount mean: 185.017")
st.text("Cluster amount_per_order mean: 11.062")
st.text("")

st.subheader("Over 70% of customers are Low spender customers.")
st.subheader("A marketing campaign totaly focused to these type customers is expected to raise the revenue in breakfast cuisine.")

