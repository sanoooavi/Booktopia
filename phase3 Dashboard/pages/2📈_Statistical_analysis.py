import streamlit as st
from model import *
import plotly.express as px
import json
from streamlit_lottie import st_lottie

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
def prepare_data(_mysqldb:MySQLConnection):
    page_publication_rel=get_page_num_rel_publication_year(mysqldb)
    price_publication_rel=get_price_rel_publication_year(mysqldb)
    price_score_rel=get_price_rel_score(mysqldb)
    books_by_format=get_num_book_based_format(mysqldb)
    return page_publication_rel,price_publication_rel,price_score_rel,books_by_format


st.set_page_config(page_icon='📈',page_title='statistical analysis',layout='wide')
st.markdown("<h1 style='text-align: center;'>📈 Statistical analysis</h1>", unsafe_allow_html=True)
mysqldb=set_connection()
page_publication_rel,price_publication_rel,price_score_rel,books_by_format=prepare_data(mysqldb)
set_font()

lottie_chart = json.load(open( "analysis2.json"))
col1,col2,col3 = st.columns([1,2,1])
with col2:
    st_lottie(lottie_chart,speed=1, loop=True, quality="medium", width=700,height=200)

#q6
st.markdown(f"""
    <h3 style='text-align: center;'>Number of pages scatter chart based on book publication year</h3>
    """,unsafe_allow_html=True)

st.line_chart(page_publication_rel,x='solar_publication_year',y='page_number',color='#e5567f')

fig9=px.scatter(page_publication_rel,x='solar_publication_year',y='page_number',color='solar_publication_year',color_continuous_scale=['#e5567f','#f500bd',' #00f5e2 '])
st.plotly_chart(fig9,use_container_width=True)

#q7
st.markdown(f"""
    <h4 style='text-align: center;'>Price scatter chart based on book publication year</h4>
    """,unsafe_allow_html=True)
st.line_chart(price_publication_rel,x='solar_publication_year',y='price',color='#00ffff')

fig10=px.scatter(price_publication_rel,x='solar_publication_year',y='price',color='solar_publication_year',color_continuous_scale=['aqua','green','yellow'])
st.plotly_chart(fig10,use_container_width=True)

#q8

st.markdown(f"""
    <h4 style='text-align: center;'>Price scatter chart based on book score</h4>
    """,unsafe_allow_html=True)

st.line_chart(price_score_rel,x='score',y=['price','after_discount'],color=["#db4727", "#fcff49"])

fig12=px.scatter(price_score_rel,x='score',y='price',color='score',color_continuous_scale=['white','yellow','red'],hover_data=['Persian_title','date'],title='main price')
fig13=px.scatter(price_score_rel,x='score',y='after_discount',color='score',color_continuous_scale=['#00dbf5','#00f521','#ff00ff'],hover_data=['Persian_title','date'],title='after_discount')
st.plotly_chart(fig12,use_container_width=True)
st.plotly_chart(fig13,use_container_width=True)

#q9

st.markdown("""
    <h4 >The number of Books based on Size</h4>
""", unsafe_allow_html=True)

col_f1,col_f2=st.columns((2))
with col_f1:
    fig13=px.bar(books_by_format,x='number_of_books',y='format',orientation='h',\
            text='number_of_books',color_continuous_scale=['yellow','#00ffff'],color='number_of_books')
    st.plotly_chart(fig13,use_container_width=True)
with col_f2:
    fig14=px.pie(books_by_format,names='format',values='number_of_books',hole=0.5)
    st.plotly_chart(fig14,use_container_width=True)