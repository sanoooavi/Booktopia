import streamlit as st
from model import *
from matplotlib import pyplot as plt
import json
from streamlit_lottie import st_lottie
import plotly.express as px


def set_font():
    st.markdown(
        """
        <style>
        * {
            font-family: 'Tahoma', 'Times New Romans', sans-serif !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def set_connection():
    try:
        mysqldb = get_connection()
    except:
        st.error("Make Sure Database is up & Running", icon="🚨")
        st.stop()
    return mysqldb


@st.cache_data
def prepare_data(_mysqldb: MySQLConnection):
    book_tags_df = get_books_by_tags(mysqldb)
    publisher_book_df = get_publisher_book_count(mysqldb)
    books_by_solar_year = get_count_book_year_solar(mysqldb)
    books_by_ad_year = get_count_book_year_ad(mysqldb)
    top_10_writer_by_book_count = get_top_10_writers(mysqldb)
    top_10_translator_by_book_count = get_top_10_translators(mysqldb)
    return book_tags_df, publisher_book_df, books_by_solar_year, books_by_ad_year, top_10_writer_by_book_count, top_10_translator_by_book_count


st.set_page_config(page_icon='📊', page_title='statistical analysis', layout='wide')
st.markdown("<h1 style='text-align: center;'>📊 Statistical analysis</h1>", unsafe_allow_html=True)

set_font()
mysqldb = set_connection()
book_tags_df, publisher_book_df, books_by_solar_year, \
    books_by_ad_year, top_10_writer_by_book_count, top_10_translator_by_book_count = prepare_data(mysqldb)

lottie_chart = json.load(open("analysis1.json"))
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st_lottie(lottie_chart, speed=1, loop=True, quality="medium", width=700, height=200)
# q1

st.markdown(
    f"""
    <h4 style='text-align: center;'>Books category treemap plot</h4>
    """,
    unsafe_allow_html=True
)
_1_book_tags_df = book_tags_df.iloc[:100]
fig1 = px.treemap(_1_book_tags_df, path=["name"], values="number_of_books", title='100 most tags used')
fig1.update_layout(width=800, height=650)
fig1.update_traces(root_color="lightgrey")
st.plotly_chart(fig1, use_container_width=True)

_2_book_tags_df = book_tags_df.iloc[-100:]
fig2 = px.treemap(_2_book_tags_df, path=["name"], values="number_of_books", title='100 least tags used')
fig2.update_layout(width=800, height=650)
fig2.update_traces(root_color="lightgrey")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.pie(book_tags_df.iloc[:30], names='name', values='number_of_books', title='top 30 categories')
st.plotly_chart(fig3, use_container_width=True)

# q2
st.markdown(
    f"""
    <h4 style='text-align: center;'>Top 10 publishers based on number of books plot</h4>
    """,
    unsafe_allow_html=True
)
cl1, cl2 = st.columns((2))

with cl2:
    fig = px.pie(publisher_book_df, values="number_of_books", names="publisher", hole=0.3, title='top 10 publishers')
    st.plotly_chart(fig, use_container_width=True)

with cl1:
    fig = px.bar(publisher_book_df, x='publisher', y='number_of_books', color='number_of_books',
                 color_continuous_scale=['yellow', 'green'],
                 title='top 10 publishers', text='number_of_books', text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)

# q3
st.markdown(
    f"""
    <h4 style='text-align: center;'>Line plot of Books based on year of publication</h4>
    """,
    unsafe_allow_html=True
)

st.line_chart(books_by_solar_year, x='solar_publication_year', y='number_of_books', color='#cc0000')

st.line_chart(books_by_ad_year, x='ad_publication_year', y='number_of_books', color='#ff0000')

# q4

st.markdown(f"""
    <h4 style='text-align: center;'>Top 10 writers by number of book</h4>
    """, unsafe_allow_html=True)

col_w1, col_w2 = st.columns((2))
with col_w1:
    fig5 = px.bar(top_10_writer_by_book_count, x='number_of_books', y='name', orientation='h',
                  color='number_of_books', color_continuous_scale=['yellow', 'green'], text='number_of_books')
    st.plotly_chart(fig5, use_container_width=True)
with col_w2:
    fig6 = px.pie(top_10_writer_by_book_count, names='name', values='number_of_books', hole=0.5)
    st.plotly_chart(fig6, use_container_width=True)

# q5

st.markdown(f"""
    <h4 style='text-align: center;'>Top 10 translators by number of book</h4>
    """, unsafe_allow_html=True)
col_t1, col_t2 = st.columns((2))
with col_t1:
    fig7 = px.bar(top_10_translator_by_book_count, x='number_of_books', y='name', orientation='h', \
                  color='number_of_books', color_continuous_scale=['yellow', 'green'], text='number_of_books')
    st.plotly_chart(fig7, use_container_width=True)
with col_t2:
    fig8 = px.pie(top_10_translator_by_book_count, names='name', values='number_of_books', hole=0.5)
    st.plotly_chart(fig8, use_container_width=True)
