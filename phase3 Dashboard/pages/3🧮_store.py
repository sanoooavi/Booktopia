from model import *
import streamlit as st
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_icon='🛒',page_title='Book store')
def set_connection():
    try:
       mysqldb = get_connection()
    except:
        st.error("Make Sure Database is up & Running", icon="🚨")
        st.stop()
    return mysqldb

mysqldb=set_connection()

st.markdown(f"""
    <h3 style='text-align: center;'>Start your career as a book seller here...</h3>
    """,unsafe_allow_html=True)
# lottie_url_flower = "../qwPu6tqAZO.json"
lottie_shop = json.load(open( "bookshop.json"))
col1,col2,col3 = st.columns([1,2,1])
with col2:
    st_lottie(lottie_shop,speed=5, loop=True, quality="medium", width=400,height=200)
@st.cache_data
def prepare_df(_mysqldb:MySQLConnection):
    writers_df=get_writer_df(mysqldb)
    # writers_list=writers_df['name'].drop_duplicates().to_list()
    return writers_df

writers_df=prepare_df(mysqldb)


st.markdown('You can find books with the features you want and according to your budget')
budget = st.number_input( "Enter your budget here👇" , min_value=350, step=100)
criteria = st.radio(
    "**What's your purpose**",
    ["***Most profit***", "***Most books***", "***Highest quality books***"],
    captions = ["money money money💸", "fill it up📚", "importance to the subject"],key=10)
if criteria=='***Most profit***':
    afforadble_books=get_most_profitable_books_by_budget(mysqldb,budget)
elif criteria=='***Most books***':
    afforadble_books=get_most_books_by_budget(mysqldb,budget)
else:
    afforadble_books=get_best_books_by_budget(mysqldb,budget)
st.dataframe(afforadble_books)
st.markdown('You can find unique books based on ypur desired feature')
unique = st.number_input( "Enter number of books you want here👇" , min_value=1, step=1)
criteria_unique = st.radio(
    "**What's your purpose**",
    ["***book rewards***", "***book venerations***",],
    captions = ["🏆🏆🏆🏆", "👏👏👏👏"])
if criteria_unique=="***book rewards***":
    unique_books=get_unique_books(mysqldb,unique)
else:
    unique_books=get_most_veneration_book(mysqldb,unique)
st.dataframe(unique_books)

st.markdown('You can find more about a specific writer')
writer_name=st.selectbox('choose the writer',writers_df['name'].drop_duplicates().to_list())
writer_row=writers_df[writers_df['name']==writer_name].iloc[0]
st.write('name : '+str(writer_row['name']))
st.write('about :'+writer_row['about'])

