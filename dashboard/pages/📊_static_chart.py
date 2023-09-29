import streamlit as st
from model import *
from matplotlib import pyplot as plt
import numpy as np
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

st.set_page_config(page_icon='📊',page_title='static analysis',layout='wide')
st.title('📊static charts')
set_font()
try:
    mysqldb = get_connection()
except:
    st.error("Make Sure Database is up & Running", icon="🚨")
    st.stop()

st.markdown(
    f"""
    <h3 style='text-align: center;'>Books category by their tags</h3>
    """,
    unsafe_allow_html=True
)
book_tags_df=get_books_by_tags(mysqldb)
_1_book_tags_df=book_tags_df.iloc[:100]
fig1 = px.treemap(_1_book_tags_df, path = ["name"], values = "count",hover_data = ["count"],title='100 most tags used')
fig1.update_layout(width = 800, height = 650)
fig1.update_traces(root_color="lightgrey")
st.plotly_chart(fig1, use_container_width=True)

_2_book_tags_df=book_tags_df.iloc[-100:]
fig2 = px.treemap(_2_book_tags_df, path = ["name"], values = "count",hover_data = ["count"],title='100 least tags used')
fig2.update_layout(width = 800, height = 650)
fig2.update_traces(root_color="lightgrey")
st.plotly_chart(fig2, use_container_width=True)

fig3=px.pie(book_tags_df.iloc[:30],names='name',values='count',title='top 50 categories')
st.plotly_chart(fig3,use_container_width=True)
#q2
st.markdown(
    f"""
    <h3 style='text-align: center;'>Top 10 publishers by number of books</h3>
    """,
    unsafe_allow_html=True
)
cl1, cl2 = st.columns((2))
publisher_book_df=get_publisher_book_count(mysqldb)
# st.subheader("Top 10 publishers by number of books")
with cl2:   
    fig = px.pie(publisher_book_df, values = "books_count", names = "name", hole = 0.3,title='top 10 publishers')
    st.plotly_chart(fig,use_container_width=True)

with cl1:
    fig=px.bar(publisher_book_df,x='name',y='books_count',color='books_count',
               title='top 10 publishers',text='books_count', text_auto='.2s')
    fig.update_layout(
    xaxis_title='نام ناشر',  # Change the x axis name
    yaxis_title='تعداد کتاب منتشر شده'  # Change the y axis name
    )
    st.plotly_chart(fig,use_container_width=True)

#q3
st.markdown(
    f"""
    <h3 style='text-align: center;'>Books by year of publication</h3>
    """,
    unsafe_allow_html=True
)
books_by_solar_year=get_count_book_year_solar(mysqldb)
st.line_chart(books_by_solar_year,x='solar_publication_year',y='books_count',color='#ffaa0088')

st.markdown(
    f"""
    <h3 style='text-align: center;'>Books by year of publication</h3>
    """,
    unsafe_allow_html=True
)
books_by_ad_year=get_count_book_year_ad(mysqldb)
st.line_chart(books_by_ad_year,x='ad_publication_year',y='books_count',color='#ffaa0088')

#q4

st.markdown(f"""
    <h3 style='text-align: center;'>Top 10 writers by number of book</h3>
    """,unsafe_allow_html=True)
top_10_writer_by_book_count=get_top_10_writers(mysqldb)
col_w1,col_w2=st.columns((2))
with col_w1:
    fig5=px.bar(top_10_writer_by_book_count,x='count_book',y='name',orientation='h',
                color_discrete_sequence=["#0083B8"] * len(top_10_writer_by_book_count),text='count_book')
    fig5.update_layout(
        xaxis_title='تعداد کتاب نوشته شده',
        yaxis_title='نام نویسنده'
    )
    st.plotly_chart(fig5,use_container_width=True)
with col_w2:
    fig6=px.pie(top_10_writer_by_book_count,names='name',values='count_book',hole=0.5)
    st.plotly_chart(fig6,use_container_width=True)


#q5

st.markdown(f"""
    <h3 style='text-align: center;'>Top 10 translators by number of book</h3>
    """,unsafe_allow_html=True)
top_10_translator_by_book_count=get_top_10_translators(mysqldb)
col_t1,col_t2=st.columns((2))
with col_t1:
    fig7=px.bar(top_10_translator_by_book_count,x='count_book',y='name',orientation='h',\
                color_discrete_sequence=["#0083B8"] * len(top_10_translator_by_book_count),text='count_book')
    fig7.update_layout(
    xaxis_title='تعداد کتاب ترجمه شده',
    yaxis_title='نام مترجم' 
    )
    st.plotly_chart(fig7,use_container_width=True)
with col_t2:
    fig8=px.pie(top_10_translator_by_book_count,names='name',values='count_book',hole=0.5)
    st.plotly_chart(fig8,use_container_width=True)