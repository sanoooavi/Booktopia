from model import *
import streamlit as st
from streamlit_lottie import st_lottie
import json
import plotly.express as px
from pyvis.network import Network

st.set_page_config(page_icon='📊', page_title='Further Analysis', layout='wide')
st.markdown("<h1 style='text-align: center;'>📊 Further Analysis</h1>", unsafe_allow_html=True)


def set_connection():
    try:
        mysqldb = get_connection()
    except:
        st.error("Make Sure Database is up & Running", icon="🚨")
        st.stop()
    return mysqldb


mysqldb = set_connection()

st.markdown(f"""
    <h2 style='text-align: left;'>Lets have a closer look on the Data...</h2>
    """, unsafe_allow_html=True)


@st.cache_data
def prepare_data(_mysqldb: MySQLConnection):
    publisher_translator = get_publisher_translator(_mysqldb)
    publisher_genres = get_publisher_genres(_mysqldb)
    return publisher_translator, publisher_genres


publisher_translator, publisher_genres = prepare_data(mysqldb)

st.markdown(f"""<h4 style='text-align: Left;'>Price scatter chart based on book score</h4>
    """, unsafe_allow_html=True)

fig1 = px.bar(publisher_translator, x='publisher_name', y='book_count',
              hover_data=['translator_name'], color='book_count',
              labels={'book_count': 'Book Count', 'publisher_name': 'Publisher Name'},
              title="Publisher Translator Book Count")
st.plotly_chart(fig1, use_container_width=True)
st.markdown(
    "As you can see, this plot shows the most translations by the publications which demonstrates "
    "that how much did the publications preferred to translate good books except of creating them.", unsafe_allow_html=True)

fig2 = px.bar(publisher_genres, x='genre_name', y='max_book_count',
              hover_data=['best_publisher_name'], color='max_book_count',
              labels={'max_book_count': 'Max Book Count', 'genre_name': 'Genre Name'},
              title="Publisher Genres Max Book Count")
st.plotly_chart(fig2)
st.markdown(
    "As you can see, this plot shows the most common genres which are printed by the publications which absolutely "
    "shows the demand of the buyers.",
    unsafe_allow_html=True)
st.markdown("<h6 style='text-align: left;'><strong>Publisher's Same Books Correlation</strong></h6>",
            unsafe_allow_html=True)
df = get_number_of_books_published_by_pubs(mysqldb)

net = Network()
actors1 = list(df['publisher1'])
nodes = set(list(df['publisher1']) + list(df['publisher2']))
title = 'publisher\'s same books correlation'
net.add_nodes(nodes)
for index, row in df.iterrows():
    net.add_edge(row['publisher1'], row['publisher2'], value=row['book_count'], title=row['book_count'])
net.save_graph('network.html')
with open("network.html", "r") as f:
    network_html = f.read()
st.components.v1.html(network_html, width=800, height=600)
st.markdown(
    "As you can see, this graph shows the correlations between different publications. The correlation depends on the thickness of the edges between the nodes; the thicker the edge, the stronger the correlation. For instance, the \"Neyestan\" publication has a strong correlation with the \"Bonyad NahjolBalagheh\" publication, as they are both considered Persian Islamic religious publications.",
    unsafe_allow_html=True)
