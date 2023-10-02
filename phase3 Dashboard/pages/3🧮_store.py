from model import *
import streamlit as st
from streamlit_lottie import st_lottie
import json


def set_connection():
    try:
       mysqldb = get_connection()
    except:
        st.error("Make Sure Database is up & Running", icon="🚨")
        st.stop()
    return mysqldb

mysqldb=set_connection()

# lottie_url_flower = "../qwPu6tqAZO.json"
lottie_shop = json.load(open( "bookshop.json"))
col1,col2,col3 = st.columns([1,2,1])
with col2:
    st_lottie(lottie_shop,speed=5, loop=True, quality="medium", width=400,height=200)
st.markdown(f"""
    <h3 style='text-align: center;'>Start your career as a book seller here...</h3>
    """,unsafe_allow_html=True)
st.markdown('You can find best books based on their score,price based on your budget')
budget = st.number_input( "Enter your budget here👇" , min_value=15000, step=1000)
afforadble_books=get_best_books_by_budget(mysqldb,budget)
st.dataframe(afforadble_books)
st.markdown('You can find unique books based on their awards')
unique = st.number_input( "Enter number of books you want here👇" , min_value=1, step=1)
unique_books=get_unique_books(mysqldb,unique)
st.dataframe(unique_books)


